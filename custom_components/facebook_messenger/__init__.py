from homeassistant.core import HomeAssistant, ServiceCall
import logging

from .notify import FacebookNotificationService

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Facebook Messenger component."""
    notify_services = hass.services.async_services().get("notify", {})
    service = notify_services.get("messenger")

    if not service:
        _LOGGER.warning("Notify service 'messenger' chưa được cấu hình.")
        return True

    async def handle_send_test(call: ServiceCall):
        target = call.data.get("target")
        message = call.data.get("message", "")
        media = call.data.get("media")
        media_type = call.data.get("media_type", "image/jpeg")
        buttons = call.data.get("buttons")
        quick_replies = call.data.get("quick_replies")

        data = {}
        if media:
            data["media"] = media
            data["media_type"] = media_type
        if buttons:
            data["buttons"] = buttons
        if quick_replies:
            data["quick_replies"] = quick_replies

        service.send_message(message=message, target=[target], data=data)

    hass.services.async_register(
        domain="facebook_messenger",
        service="send_test",
        service_func=handle_send_test,
    )

    return True
