import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS, CONF_SID


class FacebookMessengerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Facebook Messenger."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        existing_targets = self.config_entry.options.get(CONF_TARGETS) or self.config_entry.data.get(CONF_TARGETS) or ""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_PAGE_ACCESS_TOKEN, default=self.config_entry.data.get(CONF_PAGE_ACCESS_TOKEN)): str,
                vol.Optional(CONF_NAME, default=self.config_entry.data.get(CONF_NAME, "messenger")): str,
                vol.Optional(CONF_TARGETS, default=existing_targets): str,
            })
        )
