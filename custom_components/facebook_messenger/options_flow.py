from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

def parse_targets(text: str) -> dict:
    result = {}
    for pair in text.split(","):
        if ":" in pair:
            sid, name = pair.strip().split(":", 1)
            result[sid.strip()] = name.strip()
    return result

def format_targets(targets_dict: dict) -> str:
    return ", ".join(f"{sid}:{name}" for sid, name in targets_dict.items())

class FacebookMessengerOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        current = self.config_entry.options or {}

        errors = {}
        if user_input is not None:
            try:
                targets_dict = parse_targets(user_input["targets"])
                return self.async_create_entry(
                    title="Edit Facebook Messenger",
                    data={
                        "page_access_token": user_input["page_access_token"],
                        "targets": targets_dict
                    }
                )
            except Exception:
                errors["base"] = "invalid_targets"

        schema = vol.Schema({
            vol.Required("page_access_token", default=current.get("page_access_token", "")): str,
            vol.Required("targets", default=format_targets(current.get("targets", {}))): str
        })

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
