"""Facebook platform for notify component."""
import os
import json
import logging
from http import HTTPStatus

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

BASE_URL = "https://graph.facebook.com/v2.6/me/messages"
BASE_URL_MEDIA = "https://graph.facebook.com/v14.0/me/messages"
KEY_MEDIA = "media"
KEY_MEDIA_TYPE = "media_type"

TARGET_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
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
    """Implementation of a notification service for the Facebook service."""

    def __init__(self, access_token, targets):
        """Initialize the service."""
        self.page_access_token = access_token
        self.targets_map = {}
        if targets:
            self.make_targets_map(targets)

    def make_targets_map(self, targets):
        for item in targets:
            self.targets_map[item[CONF_NAME]] = item[CONF_SID]

    def send_message(self, message="", **kwargs):
        """Send a message to one or more targets."""
        payload = {"access_token": self.page_access_token}
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA)

        media = None
        media_type = "image/jpeg"

        # Default body message
        body_message = {"text": message}

        # Handle data with media or buttons
        if data is not None:
            if KEY_MEDIA in data:
                media = data[KEY_MEDIA]
                if not os.path.exists(media):
                    _LOGGER.error(f"Media file not found: [{media}]")
                    media = None
                else:
                    media_type = data.get(KEY_MEDIA_TYPE, "image/jpeg")

            elif "buttons" in data and "text" in data:
                # Build button template message
                body_message = {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": data["text"],
                            "buttons": data["buttons"],
                        },
                    }
                }
            else:
                # Append other data if no special template
                body_message.update(data)
                if "attachment" in body_message:
                    body_message.pop("text", None)

        if not targets:
            _LOGGER.error("At least 1 target is required")
            return

        for target in targets:
            # Resolve target name to SID if applicable
            if target in self.targets_map:
                target = self.targets_map[target]

            # Determine recipient format
            recipient = {"phone_number": target} if target.startswith("+") else {"id": target}

            if media:
                try:
                    with open(media, "rb") as file_data:
                        resp = requests.post(
                            url=BASE_URL_MEDIA,
                            data={
                                "access_token": self.page_access_token,
                                "recipient": json.dumps(recipient),
                                "message": json.dumps(
                                    {
                                        "attachment": {
                                            "type": "image",
                                            "payload": {"is_reusable": False},
                                        }
                                    }
                                ),
                            },
                            files={"filedata": ("media.jpg", file_data, media_type)},
                            timeout=10,
                        )
                except Exception as e:
                    _LOGGER.error("Error opening media file: %s", e)
                    continue
            else:
                body = {
                    "recipient": recipient,
                    "message": body_message,
                    "messaging_type": "MESSAGE_TAG",
                    "tag": "ACCOUNT_UPDATE",
                }
                try:
                    resp = requests.post(
                        BASE_URL,
                        data=json.dumps(body),
                        params=payload,
                        headers={"Content-Type": CONTENT_TYPE_JSON},
                        timeout=10,
                    )
                except Exception as e:
                    _LOGGER.error("Error sending message: %s", e)
                    continue

            if resp.status_code != HTTPStatus.OK:
                log_error(resp)


def log_error(response):
    """Log error response from Facebook API."""
    try:
        obj = response.json()
        error_message = obj.get("error", {}).get("message", "Unknown error")
        error_code = obj.get("error", {}).get("code", "Unknown code")
        _LOGGER.error(
            "Facebook API error %s: %s (Code %s)",
            response.status_code,
            error_message,
            error_code,
        )
    except Exception as e:
        _LOGGER.error("Failed to parse error response: %s", e)
