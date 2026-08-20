import json

def keyboard(options):
    return json.dumps({"one_time":False,"inline":False,"buttons":[[{"action":{"type":"text","label":label,"payload":json.dumps({"value":value},ensure_ascii=False)},"color":"primary"}] for label,value in options]},ensure_ascii=False)

def start_keyboard(): return keyboard([("🏆 Подобрать спорт","start")])
def stop_keyboard(): return keyboard([("⛔ Остановить","stop")])
def restart_keyboard(): return keyboard([("🔄 Пройти заново","restart")])
