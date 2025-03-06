import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("SERVER_PORT", 8085))
    app.logger.info(f"Запуск сервиса обработки вебхуков Bitrix24 на порту {port}")
    app.run(host='0.0.0.0', port=port)