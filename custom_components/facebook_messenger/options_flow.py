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

def format_sender_ids(data: dict) -> str:
    return ", ".join(f"{k}:{v}" for k, v in data.items())

class FacebookMessengerOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        current_data = self.config_entry.data
        sender_name_map = current_data.get("sender_name_map", {})

        if user_input is not None:
            try:
                parsed = parse_sender_ids(user_input["allowed_sender_ids"])
                return self.async_create_entry(
                    title="Facebook Messenger Options",
                    data={"allowed_sender_ids": user_input["allowed_sender_ids"], "sender_name_map": parsed},
                )
            except Exception:
                errors["base"] = "invalid_sender_ids"

        schema = vol.Schema({
            vol.Required(
                "allowed_sender_ids",
                default=format_sender_ids(sender_name_map)
            ): str
        })

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
