import os
import json
import logging
import requests
from http import HTTPStatus
from homeassistant.components.notify import (
    BaseNotificationService,
)
from homeassistant.const import CONTENT_TYPE_JSON
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS

_LOGGER = logging.getLogger(__name__)

def parse_targets(target_str):
    mapping = {}
    parts = [t.strip() for t in target_str.split(",") if ":" in t]
    for part in parts:
        sid, name = part.split(":", 1)
        mapping[name.strip()] = sid.strip()
    return mapping

async def async_get_service(hass, config_entry, discovery_info=None):
    config = hass.data[DOMAIN][config_entry.entry_id]
    access_token = config[CONF_PAGE_ACCESS_TOKEN]
    targets_raw = config.get(CONF_TARGETS, "")
    targets_map = parse_targets(targets_raw)
    return FacebookNotificationService(access_token, targets_map)

class FacebookNotificationService(BaseNotificationService):
    def __init__(self, access_token, targets_map):
        self.page_access_token = access_token
        self.targets_map = targets_map

    def send_message(self, message="", **kwargs):
        payload = {"access_token": self.page_access_token}
        targets = kwargs.get("target")
        data = kwargs.get("data") or {}

        media = data.get("media")
        media_type = data.get("media_type", "image/jpeg")

        body_message = {"text": message}

        if media and os.path.exists(media):
            pass
        elif "buttons" in data:
            body_message = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message,
                        "buttons": data["buttons"],
                    },
                }
            }
        elif "quick_replies" in data:
            body_message = {
                "text": message,
                "quick_replies": data["quick_replies"]
            }

        if not targets:
            _LOGGER.error("No targets provided")
            return

        for target in targets:
            if target in self.targets_map:
                target = self.targets_map[target]

            recipient = {"id": target}

            if media and os.path.exists(media):
                try:
                    with open(media, "rb") as file_data:
                        resp = requests.post(
                            url="https://graph.facebook.com/v14.0/me/messages",
                            data={
                                "access_token": self.page_access_token,
                                "recipient": json.dumps(recipient),
                                "message": json.dumps({
                                    "attachment": {
                                        "type": "image",
                                        "payload": {"is_reusable": False}
                                    }
                                }),
                            },
                            files={"filedata": ("media.jpg", file_data, media_type)},
                            timeout=10,
                        )
                except Exception as e:
                    _LOGGER.error("Error sending media: %s", e)
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
                        "https://graph.facebook.com/v2.6/me/messages",
                        data=json.dumps(body),
                        params=payload,
                        headers={"Content-Type": CONTENT_TYPE_JSON},
                        timeout=10,
                    )
                except Exception as e:
                    _LOGGER.error("Error sending message: %s", e)
                    continue

            if resp.status_code != HTTPStatus.OK:
                try:
                    obj = resp.json()
                    error_msg = obj.get("error", {}).get("message", "Unknown error")
                    _LOGGER.error("Facebook API error %s: %s", resp.status_code, error_msg)
                except Exception:
                    _LOGGER.error("Non-JSON error from Facebook")
