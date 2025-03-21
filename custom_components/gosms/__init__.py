from typing import Optional
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import translation
import re
import voluptuous as vol
from .const import DOMAIN, SERVICE_SEND_MESSAGE

def get_error_message(hass: HomeAssistant, error_key: str, language: str = 'en') -> str:
    """Get error message in specified language."""
    return translation.async_get_cached_translation(
        hass, language, "service", "errors", error_key
    )

def validate_phone_number(phone: str, hass: HomeAssistant, language: str = 'en') -> str:
    """Validate and format phone number."""
    # Удаляем все нецифровые символы
    phone = re.sub(r'\D', '', phone)
    
    # Проверяем длину номера (от 10 до 15 цифр согласно E.164)
    if len(phone) < 10 or len(phone) > 15:
        raise ValueError(get_error_message(hass, 'invalid_phone', language))
    
    # Если номер начинается с 0, заменяем его на код страны
    if phone.startswith('0'):
        phone = phone[1:]
    
    return phone

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the GOSMS.RU component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigType) -> bool:
    """Настройка интеграции через Config Flow."""
    # Сохраняем API ключ в hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api_key"] = entry.data["api_key"]
    hass.data[DOMAIN]["language"] = entry.data.get("language", "en")

    # Регистрация кастомного сервиса
    async def send_message_service(call: ServiceCall) -> None:
        """Handle the send_message service call."""
        message = call.data.get("message")
        phone = call.data.get("phone")
        device_id = call.data.get("device_id")
        language = hass.data[DOMAIN].get("language", "en")

        try:
            # Валидация и форматирование номера телефона
            phone = validate_phone_number(phone, hass, language)
        except ValueError as e:
            raise ValueError(get_error_message(hass, 'invalid_format', language).format(str(e)))

        try:
            # Логика отправки SMS
            await hass.async_add_executor_job(
                send_sms, hass.data[DOMAIN]["api_key"], phone, message, device_id, hass, language
            )
        except Exception as e:
            raise Exception(get_error_message(hass, 'api_error', language).format(str(e)))

    # Схема для валидации данных сервиса
    service_schema = vol.Schema({
        vol.Required("message"): cv.string,
        vol.Required("phone"): cv.string,
        vol.Optional("device_id"): cv.string,
    })

    # Регистрация сервиса
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_MESSAGE, send_message_service, schema=service_schema
    )

    return True

def send_sms(api_key: str, phone: str, message: str, device_id: Optional[str] = None, hass: Optional[HomeAssistant] = None, language: str = 'en') -> None:
    """Send SMS using GOSMS.RU API."""
    import requests

    api_url = "https://api.gosms.ru/v1/sms/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": message,
        "phone_number": phone,
    }
    if device_id:
        payload["device_id"] = device_id

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Проверяем наличие id в ответе
        if "id" not in data:
            raise Exception(get_error_message(hass, 'no_message_id', language))

        return data["id"]
    except requests.exceptions.RequestException as ex:
        raise Exception(get_error_message(hass, 'api_error', language).format(str(ex)))

async def async_unload_entry(hass: HomeAssistant, entry: ConfigType) -> bool:
    """Выгрузка интеграции."""
    return True
