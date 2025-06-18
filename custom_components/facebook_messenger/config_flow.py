# config_flow.py
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_PAGE_ACCESS_TOKEN, CONF_TARGETS, CONF_SID

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Facebook Messenger config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            # You might want to add some basic validation here,
            # e.g., checking if the token is not empty.
            if not user_input[CONF_PAGE_ACCESS_TOKEN]:
                errors["base"] = "invalid_token"
            
            if not errors:
                return self.async_create_entry(
                    title="Facebook Messenger", 
                    data=user_input
                )

        data_schema = vol.Schema({
            vol.Required(CONF_PAGE_ACCESS_TOKEN): str,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )

    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return FacebookMessengerOptionsFlowHandler(config_entry)

class FacebookMessengerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        targets_data = self.config_entry.options.get(CONF_TARGETS, [])
        targets_schema = {}
        for i, target in enumerate(targets_data):
            targets_schema[vol.Optional(f"{CONF_NAME}_{i}", default=target[CONF_NAME])] = str
            targets_schema[vol.Optional(f"{CONF_SID}_{i}", default=target[CONF_SID])] = str

        data_schema = vol.Schema({
            vol.Optional(CONF_TARGETS, default=""): str, # This will be handled as a string for now, needs custom UI for list of targets
        })

        # A more robust way to handle dynamic lists in options flow would involve
        # multiple steps or a custom front-end component. For simplicity,
        # we'll use a placeholder for targets.
        # You would typically have an "Add Target" button and then a sub-flow
        # for adding each target.

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            description_placeholders={
                "current_targets": ", ".join([f"{t[CONF_NAME]} ({t[CONF_SID]})" for t in targets_data])
            }
        )
