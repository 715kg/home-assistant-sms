# GOSMS.RU Integration for Home Assistant

[English](#english) | [Русский](#russian)

## English

### Overview
This custom integration allows you to send SMS messages through the GOSMS.RU service directly from Home Assistant. It provides a simple service that can be called from automations, scripts, or other integrations.

### Features
- Send SMS messages to any phone number
- Support for international phone numbers
- Multi-language error messages (English, Russian, Chinese)
- Optional device ID support for message routing
- Simple service-based API

### Installation

#### Method 1: HACS (Recommended)
1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Add this repository as a custom integration in HACS
3. Search for "GOSMS.RU" in HACS
4. Click "Download"
5. Restart Home Assistant

#### Method 2: Manual Installation
1. Download the latest release
2. Copy the `gosms` folder to your `custom_components` directory
3. Restart Home Assistant

### Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "GOSMS.RU"
4. Enter your API key from GOSMS.RU
5. (Optional) Enter your Device ID from the GOSMS.RU panel
6. Click "Submit"

To get your API key:
1. Log in to your GOSMS.RU account
2. Go to "API Integration" section
3. Create a new API key
4. Make sure to enable "Can send messages" permission

### Usage

#### Service Call
You can send SMS messages using the following service:

```yaml
service: gosms.send_message
data:
  message: "Your message here"
  phone: "+1234567890"
  device_id: "optional-device-id"  # Optional
```

#### Example in Automation
```yaml
automation:
  - alias: "Send SMS on Door Open"
    trigger:
      platform: state
      entity_id: binary_sensor.door
      to: "on"
    action:
      service: gosms.send_message
      data:
        message: "Door has been opened!"
        phone: "+1234567890"
```

### Phone Number Format
- Phone numbers should be in international format
- Can include or exclude '+' symbol
- Must be between 10 and 15 digits
- Examples:
  - +1234567890
  - 1234567890
  - +79123456789

### Troubleshooting
1. Make sure your API key is valid and has "Can send messages" permission
2. Check if the phone number is in the correct format
3. Verify your internet connection
4. Check Home Assistant logs for detailed error messages

## Russian

### Обзор
Это пользовательская интеграция позволяет отправлять SMS-сообщения через сервис GOSMS.RU непосредственно из Home Assistant. Она предоставляет простой сервис, который можно вызывать из автоматизаций, скриптов или других интеграций.

### Возможности
- Отправка SMS-сообщений на любой номер телефона
- Поддержка международных номеров
- Многоязычные сообщения об ошибках (английский, русский, китайский)
- Опциональная поддержка ID устройства для маршрутизации сообщений
- Простой API на основе сервисов

### Установка

#### Способ 1: HACS (Рекомендуется)
1. Установите [HACS](https://hacs.xyz/), если еще не установлен
2. Добавьте этот репозиторий как пользовательскую интеграцию в HACS
3. Найдите "GOSMS.RU" в HACS
4. Нажмите "Download"
5. Перезапустите Home Assistant

#### Способ 2: Ручная установка
1. Скачайте последний релиз
2. Скопируйте папку `gosms` в директорию `custom_components`
3. Перезапустите Home Assistant

### Настройка

1. Перейдите в Настройки → Устройства и сервисы
2. Нажмите "Добавить интеграцию"
3. Найдите "GOSMS.RU"
4. Введите ваш API-ключ от GOSMS.RU
5. (Опционально) Введите ID устройства из панели GOSMS.RU
6. Нажмите "Отправить"

Чтобы получить API-ключ:
1. Войдите в свой аккаунт GOSMS.RU
2. Перейдите в раздел "API Интеграция"
3. Создайте новый API-ключ
4. Убедитесь, что включено разрешение "Может отправлять сообщения"

### Использование

#### Вызов сервиса
Вы можете отправлять SMS-сообщения используя следующий сервис:

```yaml
service: gosms.send_message
data:
  message: "Ваше сообщение"
  phone: "+1234567890"
  device_id: "опциональный-id-устройства"  # Опционально
```

#### Пример в автоматизации
```yaml
automation:
  - alias: "Отправка SMS при открытии двери"
    trigger:
      platform: state
      entity_id: binary_sensor.door
      to: "on"
    action:
      service: gosms.send_message
      data:
        message: "Дверь была открыта!"
        phone: "+1234567890"
```

### Формат номера телефона
- Номера телефонов должны быть в международном формате
- Можно использовать или не использовать символ '+'
- Должно быть от 10 до 15 цифр
- Примеры:
  - +1234567890
  - 1234567890
  - +79123456789

### Устранение неполадок
1. Убедитесь, что ваш API-ключ действителен и имеет разрешение "Может отправлять сообщения"
2. Проверьте правильность формата номера телефона
3. Проверьте подключение к интернету
4. Проверьте логи Home Assistant для получения подробных сообщений об ошибках
