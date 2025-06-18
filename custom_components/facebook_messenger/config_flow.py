import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS, CONF_SID, CONF_NAME


class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Facebook Messenger", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
            vol.Optional(CONF_TARGETS, default=[]): list
        })
        return self.async_show_form(step_id="user", data_schema=schema)


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        from .options_flow import FacebookMessengerOptionsFlowHandler
        return FacebookMessengerOptionsFlowHandler(config_entry)
