from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class FacebookMessengerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        options = dict(self.config_entry.options)
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required("page_access_token", default=options.get("page_access_token", "")): str,
            vol.Optional("allowed_sender_ids", default=options.get("allowed_sender_ids", "")): str,
        })

        return self.async_show_form(step_id="init", data_schema=schema)
