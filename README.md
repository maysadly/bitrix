# Bitrix24 Webhook Integration Service

Сервис для обработки вебхуков Bitrix24 и синхронизации сделок между двумя экземплярами CRM.

## Описание

Данное приложение принимает вебхуки от первой CRM Bitrix24 при создании новой сделки и автоматически создает аналогичную сделку во второй CRM.

## Установка и настройка

### Требования

- Python 3.9+
- pip
- Docker и Docker Compose (для запуска в контейнере)

### Локальная установка

1. Клонируйте репозиторий:
   ```bash
   git clone <url-репозитория>
   cd bitrix