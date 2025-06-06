"""Facebook platform for notify component."""
from http import HTTPStatus
import json
import logging
import os
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONTENT_TYPE_JSON
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PAGE_ACCESS_TOKEN = "page_access_token"
CONF_TARGETS = "targets"
CONF_NAME = "name"
CONF_SID = "sid"
BASE_URL = "https://graph.facebook.com/v18.0/me/messages"
KEY_MEDIA = "media"
KEY_MEDIA_TYPE = "media_type"

TARGET_SCHEMA = vol.Schema(
    {vol.Required(CONF_SID): cv.string, vol.Required(CONF_NAME): cv.string}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PAGE_ACCESS_TOKEN): cv.string,
        vol.Optional(CONF_TARGETS): vol.All(cv.ensure_list, [TARGET_SCHEMA]),
    }
)

def get_service(hass, config, discovery_info=None):
    """Get the Facebook notification service."""
    return FacebookNotificationService(
        config[CONF_PAGE_ACCESS_TOKEN], config.get(CONF_TARGETS)
    )

class FacebookNotificationService(BaseNotificationService):
    """Implementation of Facebook Messenger notification service."""

    def __init__(self, access_token, targets):
        self.page_access_token = access_token
        self.targets_map = {}
        if targets:
            for item in targets:
                self.targets_map[item[CONF_NAME]] = item[CONF_SID]

    def send_message(self, message="", **kwargs):
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA, {})

        if not targets:
            _LOGGER.error("At least one target is required.")
            return

        # Extract optional data
        image_path = data.get("media")
        media_type = data.get("media_type", "image/jpeg")
        buttons = data.get("buttons")
        quick_replies = data.get("quick_replies")

        for target in targets:
            if target in self.targets_map:
                target = self.targets_map[target]

            recipient = {"id": target} if not target.startswith("+") else {"phone_number": target}

            try:
                if image_path and os.path.exists(image_path):
                    response = requests.post(
                        url=BASE_URL,
                        params={"access_token": self.page_access_token},
                        files={"filedata": ("image.jpg", open(image_path, "rb"), media_type)},
                        data={
                            "recipient": json.dumps(recipient),
                            "message": json.dumps({
                                "attachment": {
                                    "type": "image",
                                    "payload": {"is_reusable": True}
                                }
                            })
                        },
                        timeout=10,
                    )

                elif buttons:
                    if len(buttons) > 3:
                        buttons = buttons[:3]
                        _LOGGER.warning("Facebook only supports max 3 buttons. Truncated.")
                    body = {
                        "recipient": recipient,
                        "message": {
                            "attachment": {
                                "type": "template",
                                "payload": {
                                    "template_type": "button",
                                    "text": message,
                                    "buttons": buttons,
                                },
                            }
                        },
                        "messaging_type": "MESSAGE_TAG",
                        "tag": "ACCOUNT_UPDATE",
                    }
                    response = requests.post(
                        url=BASE_URL,
                        params={"access_token": self.page_access_token},
                        headers={"Content-Type": CONTENT_TYPE_JSON},
                        data=json.dumps(body),
                        timeout=10,
                    )

                elif quick_replies:
                    if len(quick_replies) > 13:
                        quick_replies = quick_replies[:13]
                        _LOGGER.warning("Facebook supports max 13 quick replies.")
                    body = {
                        "recipient": recipient,
                        "message": {
                            "text": message,
                            "quick_replies": quick_replies,
                        },
                        "messaging_type": "MESSAGE_TAG",
                        "tag": "ACCOUNT_UPDATE",
                    }
                    response = requests.post(
                        url=BASE_URL,
                        params={"access_token": self.page_access_token},
                        headers={"Content-Type": CONTENT_TYPE_JSON},
                        data=json.dumps(body),
                        timeout=10,
                    )

                else:
                    body = {
                        "recipient": recipient,
                        "message": {"text": message},
                        "messaging_type": "MESSAGE_TAG",
                        "tag": "ACCOUNT_UPDATE",
                    }
                    response = requests.post(
                        url=BASE_URL,
                        params={"access_token": self.page_access_token},
                        headers={"Content-Type": CONTENT_TYPE_JSON},
                        data=json.dumps(body),
                        timeout=10,
                    )

                if response.status_code != HTTPStatus.OK:
                    log_error(response)
                else:
                    _LOGGER.info("✅ Sent message to %s", target)

            except Exception as e:
                _LOGGER.exception("Exception sending to %s: %s", target, str(e))

def log_error(response):
    try:
        obj = response.json()
        error_message = obj.get("error", {}).get("message")
        error_code = obj.get("error", {}).get("code")
        _LOGGER.error("❌ Error %s: %s (Code %s)", response.status_code, error_message, error_code)
    except Exception:
        _LOGGER.error("❌ Unknown error: %s", response.text)
