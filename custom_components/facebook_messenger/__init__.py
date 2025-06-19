from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "facebook_messenger"

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    await hass.async_forward_entry_setup(entry, "notify")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.async_forward_entry_unload(entry, "notify")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
