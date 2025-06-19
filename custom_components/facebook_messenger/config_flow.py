import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Facebook Messenger",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
            vol.Required(CONF_TARGETS, default=""): str,  # Ex: 1234:nguyen,5678:mai
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
