"""GOSMS.RU notify component."""
import logging
from typing import Any, List, Optional

from aiohttp.hdrs import AUTHORIZATION, CONTENT_TYPE
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_API_KEY, CONTENT_TYPE_JSON
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

BASE_API_URL = "https://api.gosms.ru/v1"
TIMEOUT = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
    }
)

def get_service(hass, config, discovery_info=None):
    """Get the GOSMS.RU notification service."""
    return GosmsNotificationService(config)

class GosmsNotificationService(BaseNotificationService):
    """Implementation of a notification service for the GOSMS.RU service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config[CONF_API_KEY]

    def send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send SMS to specified target user cell."""
        targets: List[str] = kwargs.get(ATTR_TARGET, [])
        device_id: Optional[str] = kwargs.get("device_id")

        if not targets:
            _LOGGER.error("At least 1 target is required")
            return

        api_url = f"{BASE_API_URL}/sms/send"
        headers = {
            AUTHORIZATION: f"Bearer {self.api_key}",
            CONTENT_TYPE: CONTENT_TYPE_JSON,
        }

        for target in targets:
            payload = {
                "message": message,
                "phone_number": target,
            }

            # Добавляем device_id в payload, если он указан
            if device_id:
                payload["device_id"] = device_id

            try:
                response = requests.post(
                    api_url, headers=headers, json=payload, timeout=TIMEOUT
                )
                response.raise_for_status()  # Проверка на ошибки HTTP
                data = response.json()

                if data.get("status") != "success":
                    _LOGGER.error(
                        "Failed to send SMS to %s: %s",
                        target,
                        data.get("message", "Unknown error"),
                    )
                else:
                    _LOGGER.info("SMS sent successfully to %s", target)

            except requests.exceptions.RequestException as ex:
                _LOGGER.error("Failed to send SMS to %s: %s", target, ex)