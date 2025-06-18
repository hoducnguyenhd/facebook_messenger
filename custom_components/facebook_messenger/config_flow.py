import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Facebook Messenger", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
                vol.Optional(CONF_TARGETS): str  # Có thể làm nâng cao hơn (multi-field)
            }),
            errors=errors
        )
