from flask import Blueprint, request, jsonify, current_app as app
from app.services.bitrix_api import BitrixAPI

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/deal', methods=['POST'])
def deal_webhook():
    """
    Обработчик вебхука для событий сделок.
    Получает ID сделки из вебхука, затем запрашивает полную информацию 
    о сделке и создает сделку во второй CRM.
    """
    try:
        
        app.logger.info("Заголовки вебхука: %s", dict(request.headers))
        app.logger.info("Форма вебхука: %s", dict(request.form))
        app.logger.info("JSON вебхука: %s", request.get_json(silent=True))
        
        
        content_type = request.headers.get('Content-Type', '').lower()
        
        
        webhook_data = {}
        
        if 'application/json' in content_type and request.json:
            webhook_data = request.json
        else:  
            webhook_data = request.form.to_dict()
        
        app.logger.info("Получен вебхук: %s", webhook_data)

        
        if not webhook_data:
            return jsonify({"status": "error", "message": "Пустые данные вебхука"}), 400
        
        
        deal_id = None
        
        
        if 'event' in webhook_data and webhook_data['event'] == 'ONCRMDEALADD':
            
            deal_id = webhook_data.get('data[FIELDS][ID]')
        elif 'FIELDS' in webhook_data and 'ID' in webhook_data['FIELDS']:
            
            deal_id = webhook_data['FIELDS']['ID']
        
        if not deal_id:
            return jsonify({
                "status": "error", 
                "message": "ID сделки не найден в данных вебхука"
            }), 400
        
        app.logger.info(f"Получен ID сделки: {deal_id}")
        
        
        deal_data = BitrixAPI.get_deal_by_id(deal_id)
        
        if not deal_data:
            app.logger.warning(f"Не удалось получить информацию о сделке с ID {deal_id}, создаем базовую сделку")
            deal_data = {
                'ID': deal_id,
                'TITLE': f"Новая сделка"
            }
        
        
        result = BitrixAPI.create_deal_in_second_crm(deal_data)
        
        if result:
            return jsonify({
                "status": "success", 
                "message": f"Сделка с ID {deal_id} успешно создана во второй CRM"
            }), 200
        else:
            return jsonify({
                "status": "error", 
                "message": "Ошибка создания сделки во второй CRM"
            }), 500
        
    except Exception as e:
        app.logger.error("Ошибка при обработке вебхука: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500