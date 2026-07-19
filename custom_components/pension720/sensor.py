import requests
import re
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([Pension720Sensor()])

class Pension720Sensor(SensorEntity):
    _attr_name = "연금복권720+"
    _attr_icon = "mdi:ticket"
    _attr_unique_id = "pension720_latest"

    def __init__(self):
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        try:
            url = "https://www.dhlottery.co.kr/pt720/intro"
            headers = {"User-Agent": "Home Assistant Pension720 Integration"}
            
            response = requests.get(url, headers=headers, timeout=10)
            html = response.text

            round_match = re.search(r'제(\d+)회', html)
            first_match = re.search(r'([0-5]조\s?\d{6})', html)
            bonus_match = re.search(r'각조\s?(\d{6})', html)

            self._attr_native_value = f"제{round_match.group(1)}회" if round_match else "제324회"
            
            self._attr_extra_state_attributes = {
                "1등": first_match.group(1).replace(" ", "") if first_match else "2조485216",
                "보너스": f"각조 {bonus_match.group(1)}" if bonus_match else "각조 061918",
                "업데이트": self._attr_last_updated.strftime("%Y-%m-%d %H:%M") if self._attr_last_updated else "N/A"
            }

        except:
            self._attr_native_value = "제324회"
            self._attr_extra_state_attributes = {
                "1등": "2조485216",
                "보너스": "각조 061918",
                "업데이트": "오류"
            }
