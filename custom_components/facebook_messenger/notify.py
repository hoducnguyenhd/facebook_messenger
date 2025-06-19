from homeassistant.components.notify import BaseNotificationService
from homeassistant.const import CONTENT_TYPE_JSON
import requests
import logging

_LOGGER = logging.getLogger(__name__)

async def async_get_service(hass, config_entry):
    data = config_entry.data
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

        for name in target_names:
            sid = None
            # name-based or sid-based
            if name in self.targets.values():
                sid = next((k for k, v in self.targets.items() if v == name), None)
            elif name in self.targets:
                sid = name

            if not sid:
                _LOGGER.warning("Unknown target: %s", name)
                continue

            payload = {
                "messaging_type": "RESPONSE",
                "recipient": {"id": sid},
                "message": {"text": message},
            }

            url = f"https://graph.facebook.com/v18.0/me/messages?access_token={self.token}"
            response = requests.post(url, json=payload, headers={"Content-Type": CONTENT_TYPE_JSON})
            if response.status_code != 200:
                _LOGGER.error("Failed to send to %s (%s): %s", name, sid, response.text)
