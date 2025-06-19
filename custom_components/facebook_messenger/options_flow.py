import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS

class FacebookMessengerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_PAGE_ACCESS_TOKEN, default=self.config_entry.data.get(CONF_PAGE_ACCESS_TOKEN)): str,
            vol.Required(CONF_TARGETS, default=self.config_entry.data.get(CONF_TARGETS, "")): str,
        })

        return self.async_show_form(step_id="init", data_schema=schema)

def async_get_options_flow(config_entry):
    return FacebookMessengerOptionsFlow(config_entry)
