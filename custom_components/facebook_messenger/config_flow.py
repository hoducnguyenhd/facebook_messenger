import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS


class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Facebook Messenger",
                data={
                    CONF_PAGE_ACCESS_TOKEN: user_input[CONF_PAGE_ACCESS_TOKEN],
                    CONF_TARGETS: [x.strip() for x in user_input.get(CONF_TARGETS, "").split(",") if x.strip()]
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
                vol.Optional(CONF_TARGETS, default=""): str  # comma-separated list
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        from .options_flow import FacebookMessengerOptionsFlow
        return FacebookMessengerOptionsFlow(config_entry)
