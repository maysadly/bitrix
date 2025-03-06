import requests
from flask import current_app as app

class BitrixAPI:
    """Класс для работы с API Битрикс24"""
    
    @staticmethod
    def get_deal_by_id(deal_id):
        """
        Получает информацию о сделке по её ID из первой CRM
        
        Параметры:
        - deal_id: ID сделки
        """
        try:
            url = f"{app.config['FIRST_CRM_URL']}/crm.deal.get.json"
            
            app.logger.info(f"Запрос информации о сделке с URL: {url}")
            
            params = {
                'id': deal_id,
            }
            
            response = requests.post(url, json=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'result' in data:
                app.logger.debug(f"Получены данные о сделке: {data['result']}")
                return data['result']
            else:
                app.logger.error("Некорректный ответ при получении сделки: %s", data)
                return {}
                
        except Exception as e:
            app.logger.error("Ошибка при получении данных о сделке: %s", e)
            return {}
    
    @staticmethod
    def create_deal_in_second_crm(deal_data):
        """
        Создает сделку во второй CRM.
        Принимает полные данные сделки из первой CRM.
        """
        
        title = deal_data.get('TITLE', 'Без названия')
        contact_id = deal_data.get('CONTACT_ID')
        contact_data = None  
        
        
        if contact_id:
            contact_url = f"{app.config['FIRST_CRM_URL']}/crm.contact.get.json"
            try:
                response = requests.post(contact_url, json={"id": contact_id}, timeout=30)
                response.raise_for_status()
                contact_data = response.json().get("result")
                if contact_data:
                    app.logger.debug("Получены данные контакта: %s", contact_data)
                else:
                    app.logger.warning("Контакт не найден по ID: %s", contact_id)
                    contact_data = None  
            except requests.exceptions.RequestException as e:
                app.logger.error("Ошибка сети при получении контакта: %s", e)
                contact_data = None
            except Exception as e:
                app.logger.error("Ошибка при получении контакта: %s", e)
                contact_data = None
        
        if contact_data:
            
            contact_add_url = f"{app.config['SECOND_CRM_URL']}/crm.contact.add.json"
            
            
            
            new_contact_data = {
                "fields": {
                    "NAME": contact_data.get('NAME', 'Без имени'),
                    "LAST_NAME": contact_data.get('LAST_NAME', 'Без фамилии'),
                    "PHONE": contact_data.get('PHONE', ''),
                }
            }
            
            try:
                response = requests.post(contact_add_url, json=new_contact_data, timeout=30)
                response.raise_for_status()
                contact_result = response.json().get("result")
                if contact_result:
                    contact_id = contact_result  
                    app.logger.info("Создан контакт во второй CRM. Новый ID: %s", contact_id)
                else:
                    app.logger.warning("Создание контакта вернуло неожиданный результат: %s", response.json())
            except requests.exceptions.RequestException as e:
                app.logger.error("Ошибка сети при создании контакта: %s", e)
                
            except Exception as e:
                app.logger.error("Ошибка создания контакта во второй CRM: %s", e)
                
        
        
        new_deal_data = {
            "fields": {
                "TITLE": title,
                "STAGE_ID": deal_data.get('STAGE_ID', ''),
                "OPPORTUNITY": deal_data.get('OPPORTUNITY', ''),
                "CURRENCY_ID": deal_data.get('CURRENCY_ID', ''),
                "CATEGORY_ID": '0',
            }
        }
        
        
        if contact_id:
            new_deal_data["fields"]["CONTACT_ID"] = contact_id  
        
        add_url = f"{app.config['SECOND_CRM_URL']}/crm.deal.add.json"
        
        try:
            response = requests.post(add_url, json=new_deal_data, timeout=30)
            response.raise_for_status()
            result = response.json()
            deal_id = result.get("result")
            if deal_id:
                app.logger.info("Создана сделка во второй CRM. Новый ID: %s", deal_id)
            else:
                app.logger.warning("Создание сделки вернуло неожиданный результат: %s", result)
            return result
        except requests.exceptions.RequestException as e:
            app.logger.error("Ошибка сети при создании сделки: %s", e)
            return None
        except Exception as e:
            app.logger.error("Ошибка создания сделки во второй CRM: %s", e)
            return None