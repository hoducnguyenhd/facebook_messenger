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
    return FacebookMessengerNotificationService(
        page_access_token=data["page_access_token"],
        targets=data.get("targets", {})
    )

class FacebookMessengerNotificationService(BaseNotificationService):
    def __init__(self, page_access_token, targets):
        self.token = page_access_token
        self.targets = targets  # dict: sid => name

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

            message_payload = self._build_message_payload(message, buttons, quick_replies, data)
            self._send_payload(sid, message_payload)

    def _resolve_sid(self, name_or_sid):
        if name_or_sid in self.targets.values():
            return next((k for k, v in self.targets.items() if v == name_or_sid), None)
        elif name_or_sid in self.targets:
            return name_or_sid
        return None

    def _send_payload(self, sid, payload):
        url = f"{BASE_URL}?access_token={self.token}"
        body = {
            "recipient": {"id": sid},
            "message": payload,
            "messaging_type": "RESPONSE"
        }

        try:
            response = requests.post(url, json=body, headers={"Content-Type": CONTENT_TYPE_JSON}, timeout=10)
            if response.status_code != 200:
                _LOGGER.error("Facebook error: %s - %s", response.status_code, response.text)
        except Exception as e:
            _LOGGER.error("Failed to send payload: %s", e)

    def _send_media(self, sid, media_path, media_type):
        url = f"{BASE_URL}?access_token={self.token}"
        try:
            with open(media_path, "rb") as file_data:
                files = {
                    "filedata": (os.path.basename(media_path), file_data, media_type)
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

                response = requests.post(url, data=data, files=files, timeout=10)
                if response.status_code != 200:
                    _LOGGER.error("Failed to send media: %s - %s", response.status_code, response.text)
        except Exception as e:
            _LOGGER.error("Error opening media file %s: %s", media_path, e)

    def _build_message_payload(self, message, buttons, quick_replies, raw_data):
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
            payload.update(raw_data)  # append other fields if needed
            return payload
