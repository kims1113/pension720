import logging
from datetime import timedelta
import async_timeout
from bs4 import BeautifulSoup

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "pension720"
SCAN_INTERVAL = timedelta(hours=6)

# 동행복권 차단을 우회하기 위한 브라우저 헤더 설정
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://m.dhlottery.co.kr/"
}

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Config Entry(UI)를 통해 센서를 등록합니다."""
    session = async_get_clientsession(hass)
    
    sensors = [
        PensionSensor(session, "round", "연금복권 회차", "mdi:numeric"),
        PensionSensor(session, "group", "연금복권 1등 조", "mdi:ticket-confirmation"),
        PensionSensor(session, "number", "연금복권 1등 번호", "mdi:clover"),
        PensionSensor(session, "bonus", "연금복권 보너스 번호", "mdi:gift"),
    ]
    
    async_add_entities(sensors, True)


class PensionSensor(SensorEntity):
    """연금복권 데이터 센서 클래스"""

    def __init__(self, session, sensor_type, name, icon):
        self._session = session
        self._type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"pension720_{sensor_type}"
        self._state = None
        self._available = False

    @property
    def state(self):
        return self._state

    @property
    def available(self):
        return self._available

    async def async_update(self):
        """동행복권 모바일 웹페이지 파싱"""
        url = "https://m.dhlottery.co.kr/gameResult.do?method=pension720Result"
        try:
            with async_timeout.timeout(15):
                # HEADERS를 함께 전송하여 일반 브라우저의 요청인 것처럼 속입니다.
                response = await self._session.get(url, headers=HEADERS)
                
                if response.status != 200:
                    _LOGGER.error("동행복권 서버 응답 에러 (코드: %s)", response.status)
                    self._available = False
                    return
                
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                if self._type == "round":
                    round_element = soup.select_one(".num_key strong")
                    if round_element:
                        self._state = round_element.text.replace("회", "").strip()
                        self._available = True

                elif self._type == "group":
                    group_element = soup.select_one(".win720_num .band_group span")
                    if group_element:
                        self._state = group_element.text.replace("조", "").strip()
                        self._available = True

                elif self._type == "number":
                    num_element = soup.select_one(".win720_num .band_num")
                    if num_element:
                        numbers = num_element.text.split()
                        self._state = "".join(numbers)
                        self._available = True

                elif self._type == "bonus":
                    bonus_element = soup.select_one(".bonus_num .band_num")
                    if bonus_element:
                        numbers = bonus_element.text.split()
                        self._state = "".join(numbers)
                        self._available = True

        except Exception as ex:
            _LOGGER.error("연금복권 데이터를 업데이트하는 중 에러 발생: %s", ex)
            self._available = False
