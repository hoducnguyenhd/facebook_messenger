import os
import json
import logging
from http import HTTPStatus
import requests

from homeassistant.components.notify import BaseNotificationService
from homeassistant.const import CONTENT_TYPE_JSON

from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS, CONF_NAME, CONF_SID

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://graph.facebook.com/v2.6/me/messages"
BASE_URL_MEDIA = "https://graph.facebook.com/v14.0/me/messages"

async def async_get_service(hass, config, discovery_info=None):
    entry_id = discovery_info["entry_id"]
    data = hass.data[DOMAIN][entry_id]
    return FacebookNotificationService(data[CONF_PAGE_ACCESS_TOKEN], data.get(CONF_TARGETS))

class FacebookNotificationService(BaseNotificationService):
    def __init__(self, access_token, targets):
        self.page_access_token = access_token
        self.targets_map = {}
        if targets:
            for t in targets:
                self.targets_map[t[CONF_NAME]] = t[CONF_SID]

    def send_message(self, message="", **kwargs):
        targets = kwargs.get("target")
        data = kwargs.get("data") or {}
        media = data.get("media")
        media_type = data.get("media_type", "image/jpeg")

        body_message = {"text": message}

        if media:
            if not os.path.exists(media):
                _LOGGER.error(f"Media not found: {media}")
                return
        elif "buttons" in data:
            body_message = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message,
                        "buttons": data["buttons"]
                    }
                }
            }
        elif "quick_replies" in data:
            body_message = {
                "text": message,
                "quick_replies": data["quick_replies"]
            }
        elif "attachment" in data:
            body_message = data

        for target in targets:
            sid = self.targets_map.get(target, target)
            recipient = {"id": sid} if not sid.startswith("+") else {"phone_number": sid}

            if media:
                with open(media, "rb") as f:
                    files = {"filedata": ("media.jpg", f, media_type)}
                    payload = {
                        "access_token": self.page_access_token,
                        "recipient": json.dumps(recipient),
                        "message": json.dumps({
                            "attachment": {
                                "type": "image",
                                "payload": {"is_reusable": False}
                            }
                        })
                    }
                    resp = requests.post(BASE_URL_MEDIA, data=payload, files=files, timeout=10)
            else:
                body = {
                    "recipient": recipient,
                    "message": body_message,
                    "messaging_type": "MESSAGE_TAG",
                    "tag": "ACCOUNT_UPDATE"
                }
                resp = requests.post(BASE_URL, params={"access_token": self.page_access_token},
                                     data=json.dumps(body), headers={"Content-Type": CONTENT_TYPE_JSON}, timeout=10)

            if resp.status_code != HTTPStatus.OK:
                _LOGGER.error("Facebook error: %s", resp.text)
