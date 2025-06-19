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

class FacebookMessengerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                targets_dict = parse_targets(user_input["targets"])
                return self.async_create_entry(
                    title="Facebook Messenger",
                    data={
                        "page_access_token": user_input["page_access_token"],
                        "targets": targets_dict
                    },
                )
            except Exception:
                errors["base"] = "invalid_targets"

        schema = vol.Schema({
            vol.Required("page_access_token"): str,
            vol.Required("targets"): str  # format: sid1:name1, sid2:name2
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
