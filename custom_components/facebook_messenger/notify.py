from homeassistant.components.notify import BaseNotificationService
from homeassistant.const import CONTENT_TYPE_JSON
import requests
import logging
import os
import json

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://graph.facebook.com/v18.0/me/messages"

async def async_get_service(hass, config_entry):
    data = config_entry.options if config_entry.options else config_entry.data
    token = data.get("page_access_token")
    targets_raw = data.get("allowed_sender_ids", "")
    targets = {}

    for item in targets_raw.split(","):
        parts = item.strip().split(":")
        if len(parts) == 2:
            sid, name = parts
            targets[sid.strip()] = name.strip()

    return FacebookMessengerNotificationService(token, targets)

class FacebookMessengerNotificationService(BaseNotificationService):
    def __init__(self, token, targets):
        self.token = token
        self.targets = targets  # dict {sid: name}

    def send_message(self, message="", **kwargs):
        target_names = kwargs.get("target")
        if isinstance(target_names, str):
            target_names = [target_names]

        data = kwargs.get("data") or {}
        media_path = data.get("media")
        media_type = data.get("media_type", "image/jpeg")
        buttons = data.get("buttons")
        quick_replies = data.get("quick_replies")

        for name in target_names:
            sid = self._resolve_sid(name)
            if not sid:
                _LOGGER.warning("Unknown target: %s", name)
                continue

            if media_path and os.path.isfile(media_path):
                self._send_media(sid, media_path, media_type)
                continue

            payload = self._build_message_payload(message, buttons, quick_replies, data)
            self._send_payload(sid, payload)

    def _resolve_sid(self, name_or_sid):
        for sid, name in self.targets.items():
            if name_or_sid == sid or name_or_sid == name:
                return sid
        return None

    def _send_payload(self, sid, payload):
        url = f"{BASE_URL}?access_token={self.token}"
        body = {
            "recipient": {"id": sid},
            "message": payload,
            "messaging_type": "RESPONSE"
        }

        try:
            resp = requests.post(url, json=body, headers={"Content-Type": CONTENT_TYPE_JSON}, timeout=10)
            if resp.status_code != 200:
                _LOGGER.error("Facebook error: %s - %s", resp.status_code, resp.text)
        except Exception as e:
            _LOGGER.error("Exception sending message: %s", e)

    def _send_media(self, sid, media_path, media_type):
        url = f"{BASE_URL}?access_token={self.token}"
        try:
            with open(media_path, "rb") as f:
                files = {
                    "filedata": (os.path.basename(media_path), f, media_type)
                }
                data = {
                    "recipient": json.dumps({"id": sid}),
                    "message": json.dumps({
                        "attachment": {
                            "type": "image",
                            "payload": {"is_reusable": True}
                        }
                    }),
                    "access_token": self.token
                }
                resp = requests.post(url, data=data, files=files, timeout=10)
                if resp.status_code != 200:
                    _LOGGER.error("Error sending media: %s - %s", resp.status_code, resp.text)
        except Exception as e:
            _LOGGER.error("Error opening media file: %s", e)

    def _build_message_payload(self, message, buttons, quick_replies, data):
        if buttons:
            return {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message,
                        "buttons": buttons
                    }
                }
            }
        elif quick_replies:
            return {
                "text": message,
                "quick_replies": quick_replies
            }
        else:
            payload = {"text": message}
            payload.update(data)
            return payload
