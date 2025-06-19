DOMAIN = "facebook_messenger"

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "notify")
    )
    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "notify")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
