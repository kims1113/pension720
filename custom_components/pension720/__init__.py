"""pension720 integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
DOMAIN = "pension720"
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """(레거시) configuration.yaml 기반 설정을 지원하기 위한 빈 함수입니다."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """UI(Config Entry)를 통해 기기가 추가되었을 때 호출됩니다."""
    hass.data.setdefault(DOMAIN, {})
    
    # sensor.py 파일의 엔티티들을 등록하라고 홈어시스턴트에 요청합니다.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """통합구성요소를 삭제하거나 비활성화할 때 호출되어 리소스를 해제합니다."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
