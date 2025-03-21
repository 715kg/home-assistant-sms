from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
import uuid

from .const import DOMAIN

class GosmsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow for GOSMS.RU."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Проверка, является ли строка JWT
            if not self._is_jwt(user_input["api_key"]):
                errors["api_key"] = "invalid_jwt"
            # Проверка, является ли строка UUID (если device_id задан)
            if user_input.get("device_id"):
                if not self._is_uuid(user_input["device_id"]):
                    errors["device_id"] = "invalid_uuid"
            # Если ошибок нет, сохраняем данные
            if not errors:
                # Сохраняем данные и завершаем настройку
                return self.async_create_entry(
                    title="API - GOSMS.RU",
                    data=user_input,
                )

        # Форма для ввода данных
        data_schema = vol.Schema({
            vol.Required("api_key"): str,
            vol.Optional("device_id"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    def _is_jwt(token: str) -> bool:
        """Check if the string is a valid JWT."""
        parts = token.split(".")
        return len(parts) == 3 and all(part for part in parts)

    @staticmethod
    def _is_uuid(uuid_string: str) -> bool:
        """Check if the string is a valid UUID."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False