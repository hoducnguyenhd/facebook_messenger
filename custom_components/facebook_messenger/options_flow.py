import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS


class FacebookMessengerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Facebook Messenger Options",
                data={
                    CONF_PAGE_ACCESS_TOKEN: user_input[CONF_PAGE_ACCESS_TOKEN],
                    CONF_TARGETS: [x.strip() for x in user_input.get(CONF_TARGETS, "").split(",") if x.strip()]
                }
            )

        current_targets = self.config_entry.options.get(CONF_TARGETS) or self.config_entry.data.get(CONF_TARGETS, [])
        targets_str = ", ".join(current_targets) if isinstance(current_targets, list) else ""

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_PAGE_ACCESS_TOKEN, default=self.config_entry.options.get(
                    CONF_PAGE_ACCESS_TOKEN, self.config_entry.data.get(CONF_PAGE_ACCESS_TOKEN))): str,
                vol.Optional(CONF_TARGETS, default=targets_str): str
            })
        )
