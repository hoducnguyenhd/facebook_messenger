import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

def parse_sender_ids(value):
    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if ":" in pair:
            id_part, name_part = pair.split(":", 1)
            result[id_part.strip()] = name_part.strip()
    return result

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                parsed = parse_sender_ids(user_input["allowed_sender_ids"])
                user_input["sender_name_map"] = parsed
                return self.async_create_entry(title="Facebook Messenger", data=user_input)
            except Exception:
                errors["base"] = "invalid_sender_ids"

        schema = vol.Schema({
            vol.Required("allowed_sender_ids"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
