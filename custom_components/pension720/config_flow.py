"""Config flow for pension720 integration."""
import logging
from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "pension720"

_LOGGER = logging.getLogger(__name__)

class Pension720ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """연금복권 720+ UI 설정 흐름을 제어합니다."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """사용자가 추가 버튼을 눌렀을 때 첫 번째로 실행되는 단계입니다."""
        # 1. 중복 생성 방지: 이미 이 컴포넌트가 등록되어 있다면 에러를 내며 차단합니다.
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        # 2. 사용자가 팝업창에서 '확인(제출)'을 누른 경우 엔티티 인스턴스를 생성합니다.
        if user_input is not None:
            return self.async_create_entry(title="연금복권 720+", data={})

        # 3. 사용자에게 보여줄 빈 양식(UI 팝업창)을 띄웁니다. (입력받을 변수가 없으므로 스키마는 비어있음)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
