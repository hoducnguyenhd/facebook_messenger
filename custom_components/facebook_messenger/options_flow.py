from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN


class FacebookMessengerOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("verify_token", default=self.config_entry.options.get("verify_token", "")): str,
                vol.Required("page_access_token", default=self.config_entry.options.get("page_access_token", "")): str,
                vol.Optional("target_ids", default=", ".join(self.config_entry.options.get("target_ids", []))): str,
                vol.Optional("default_media_type", default=self.config_entry.options.get("default_media_type", "image/jpeg")): str,
            }),
        )


@callback
def async_get_options_flow(config_entry):
    return FacebookMessengerOptionsFlowHandler(config_entry)
