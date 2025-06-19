from homeassistant import config_entries
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            return self.async_create_entry(title="Facebook Messenger", data=user_input)

        schema = vol.Schema({
            vol.Required("page_access_token"): str,
            vol.Optional("allowed_sender_ids", default=""): str,  # ex: 12345:nguyen,67890:mai
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
