"""GOSMS.RU notify component."""
import json
import logging

from aiohttp.hdrs import CONTENT_TYPE, AUTHORIZATION
import requests
import voluptuous as vol

from homeassistant.components.notify import ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService
from homeassistant.const import (
    CONF_API_KEY,
    CONF_SENDER,
    CONTENT_TYPE_JSON,
)
from http import HTTPStatus
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

BASE_API_URL = "https://api.gosms.ru/v1"
DEFAULT_SENDER = "hass"
TIMEOUT = 5

PLATFORM_SCHEMA = vol.Schema(
    vol.All(
        PLATFORM_SCHEMA.extend(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_SENDER, default=DEFAULT_SENDER): cv.string,
            }
        )
    )
)

def get_service(hass, config, discovery_info=None):
    """Get the GOSMS.RU notification service."""
    return GosmsNotificationService(config)

class GosmsNotificationService(BaseNotificationService):
    """Implementation of a notification service for the GOSMS.RU service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config[CONF_API_KEY]
        self.sender = config[CONF_SENDER]

    def send_message(self, message="", **kwargs):
        """Send SMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)

        api_url = f"{BASE_API_URL}/sms/send"

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        headers = {
            AUTHORIZATION: f"Bearer {self.api_key}",
            CONTENT_TYPE: CONTENT_TYPE_JSON,
        }

        for target in targets:
            payload = {
                "message": message,
                "phone_number": target,
            }

            resp = requests.post(api_url, headers=headers, json=payload, timeout=TIMEOUT)

            if resp.status_code != HTTPStatus.OK:
                _LOGGER.error("Error %s", resp.status_code)
            else:
                data = resp.json()
                if data.get('status') != 'success':
                    _LOGGER.error(
                        "Error %s", data.get('message', 'Unknown error')
                    )
