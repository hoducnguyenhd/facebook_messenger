
import logging
import requests

from homeassistant.components.notify import BaseNotificationService

_LOGGER = logging.getLogger(__name__)

def get_service(hass, config, discovery_info=None):
    return FacebookMessengerNotificationService(config.get("page_access_token"))

class FacebookMessengerNotificationService(BaseNotificationService):
    def __init__(self, page_access_token):
        self._token = page_access_token
        self._url = "https://graph.facebook.com/v18.0/me/messages"

    def send_message(self, message="", **kwargs):
        targets = kwargs.get("target", [])
        data = kwargs.get("data", {})
        image_url = data.get("image_url")
        buttons = data.get("buttons")
        quick_replies = data.get("quick_replies")

        for target in targets:
            if buttons:
                payload = {
                    "recipient": {"id": target},
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
                }
            elif quick_replies:
                payload = {
                    "recipient": {"id": target},
                    "message": {
                        "text": message,
                        "quick_replies": quick_replies,
                    },
                }
            elif image_url:
                payload = {
                    "recipient": {"id": target},
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {"url": image_url, "is_reusable": True},
                        }
                    },
                }
            else:
                payload = {
                    "recipient": {"id": target},
                    "message": {"text": message},
                }

            response = requests.post(
                self._url,
                params={"access_token": self._token},
                json=payload,
            )

            if response.status_code != 200:
                _LOGGER.error(
                    "Error sending message to %s: %s", target, response.text
                )
            else:
                _LOGGER.info("Message sent to %s: %s", target, message)
