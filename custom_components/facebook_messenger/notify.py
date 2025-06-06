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
            try:
                if buttons:
                    # Facebook chỉ hỗ trợ tối đa 3 button
                    if len(buttons) > 3:
                        _LOGGER.warning("⚠️ Chỉ tối đa 3 button được phép, đang có %d", len(buttons))
                        buttons = buttons[:3]
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
                    # Facebook hỗ trợ tối đa 13 quick replies
                    if len(quick_replies) > 13:
                        _LOGGER.warning("⚠️ Chỉ tối đa 13 quick replies được phép, đang có %d", len(quick_replies))
                        quick_replies = quick_replies[:13]
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
                    timeout=10,
                )

                if response.status_code != 200:
                    _LOGGER.error(
                        "❌ Lỗi gửi message đến %s: %s | Payload: %s",
                        target, response.text, payload
                    )
                else:
                    _LOGGER.info("✅ Đã gửi message đến %s", target)

            except Exception as e:
                _LOGGER.exception("❌ Exception khi gửi message đến %s: %s", target, str(e))
