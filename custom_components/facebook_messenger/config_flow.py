import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS, CONF_NAME, CONF_SID

class FacebookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Facebook Messenger", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
            vol.Optional(CONF_TARGETS): vol.All([{
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_SID): str
            }])
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

from homeassistant import config_entries
from .const import DOMAIN

class FacebookOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        schema = vol.Schema({
            vol.Required("page_access_token", default=data.get("page_access_token")): str,
            vol.Optional("targets", default=data.get("targets", [])): vol.All([{
                vol.Required("name"): str,
                vol.Required("sid"): str
            }])
        })

        return self.async_show_form(step_id="init", data_schema=schema)
