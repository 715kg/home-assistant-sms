# О плагине
Плагин для отправки сообщений из Home Assistant через сервис GOSMS.RU

# Установка и настройка
Для установки необходимо поместить папку gosms-ru в /usr/share/hassio/homeassistant/custom_components и прописать в конфигурацию Home Assistant:

```yaml
notify:
  - name: gosms-ru
    platform: gosms-ru
    from_number: HASS
    api_key: key
```

Для получения ключа API необходимо [зарегистрироваться](http://cravs.sms.ru/) в сервисе GOSMS.RU и в меню (API и интеграции) Создать API приложение с разрешением на отправку SMS.

# Использование
Вы можете использовать сервис notify.gosms-ru для отправления SMS сообщений.

```yaml
service: notify.gosms-ru
  message: 'Привет как дела'
  target: 
    - '+79920000001'
    - '+79950000002'
```
