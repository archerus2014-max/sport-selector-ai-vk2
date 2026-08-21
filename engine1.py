# -*- coding: utf-8 -*-
"""
SPORT SELECTOR AI — ENGINE V7
Версия с 5-балльной шкалой, полом, ростом и весом.

Антропометрические данные используются как дополнительный фактор,
а не как медицинский диагноз. Для детей 5–19 лет ориентиром служат
возрастно-половые показатели ВОЗ; в продакшн-версии для точного
z-score следует подключить таблицы WHO AnthroPlus.
"""

import math

AGE_INFO = {
    "Спортивная акробатика": {"min_age": 5, "mode": "development"},
    "Прыжки на батуте": {"min_age": 5, "mode": "development"},
    "Бокс": {"min_age": 8, "mode": "sport"},
    "Дзюдо": {"min_age": 7, "mode": "sport"},
    "Самбо": {"min_age": 7, "mode": "sport"},
    "Вольная борьба": {"min_age": 7, "mode": "sport"},
    "Стрельба из лука": {"min_age": 9, "mode": "sport"},
    "Тяжёлая атлетика": {"min_age": 9, "mode": "sport"},
    "ММА": {"min_age": 10, "mode": "sport"},
}

# Профиль: качество -> (целевой уровень 1..5, вес)
SPORTS = {
    "Спортивная акробатика": {
        "activity": (4,1.0),"speed": (3,0.7),"strength": (3,0.7),
        "endurance": (3,0.6),"coordination": (5,1.8),"flexibility": (5,1.8),
        "reaction": (3,0.7),"balance": (5,1.8),"rhythm": (4,1.2),
        "team": (4,0.9),"contact": (1,0.2),"competition": (3,0.6),
        "precision": (5,1.3),"discipline": (4,1.2),
    },
    "Прыжки на батуте": {
        "activity": (4,1.1),"speed": (3,0.7),"strength": (3,0.7),
        "endurance": (3,0.5),"coordination": (5,1.8),"flexibility": (4,1.1),
        "reaction": (4,1.2),"balance": (5,1.8),"rhythm": (3,0.8),
        "team": (2,0.4),"contact": (1,0.2),"competition": (3,0.7),
        "precision": (5,1.4),"discipline": (4,1.1),
    },
    "Бокс": {
        "activity": (5,1.1),"speed": (5,1.7),"strength": (4,1.3),
        "endurance": (4,1.3),"coordination": (4,1.0),"flexibility": (3,0.5),
        "reaction": (5,1.8),"balance": (4,1.0),"rhythm": (4,0.7),
        "team": (2,0.4),"contact": (5,1.8),"competition": (5,1.3),
        "precision": (4,1.2),"discipline": (5,1.2),
    },
    "Дзюдо": {
        "activity": (4,1.0),"speed": (4,1.0),"strength": (4,1.4),
        "endurance": (4,1.1),"coordination": (5,1.5),"flexibility": (3,0.8),
        "reaction": (4,1.2),"balance": (5,1.6),"rhythm": (2,0.3),
        "team": (2,0.4),"contact": (5,1.8),"competition": (4,1.2),
        "precision": (4,1.0),"discipline": (5,1.5),
    },
    "Самбо": {
        "activity": (4,1.1),"speed": (4,1.2),"strength": (4,1.5),
        "endurance": (4,1.2),"coordination": (5,1.5),"flexibility": (3,0.7),
        "reaction": (4,1.2),"balance": (5,1.5),"rhythm": (2,0.3),
        "team": (2,0.4),"contact": (5,1.8),"competition": (5,1.2),
        "precision": (4,0.9),"discipline": (5,1.4),
    },
    "Вольная борьба": {
        "activity": (5,1.2),"speed": (4,1.4),"strength": (5,1.7),
        "endurance": (5,1.5),"coordination": (5,1.5),"flexibility": (3,0.9),
        "reaction": (4,1.3),"balance": (5,1.4),"rhythm": (2,0.2),
        "team": (1,0.3),"contact": (5,1.8),"competition": (5,1.4),
        "precision": (3,0.7),"discipline": (5,1.3),
    },
    "Стрельба из лука": {
        "activity": (2,0.4),"speed": (2,0.4),"strength": (3,0.8),
        "endurance": (3,1.0),"coordination": (5,1.4),"flexibility": (3,0.4),
        "reaction": (3,0.5),"balance": (5,1.2),"rhythm": (2,0.3),
        "team": (2,0.5),"contact": (1,0.8),"competition": (4,0.8),
        "precision": (5,2.0),"discipline": (5,1.8),
    },
    "Тяжёлая атлетика": {
        "activity": (4,0.9),"speed": (4,0.8),"strength": (5,2.0),
        "endurance": (3,0.7),"coordination": (5,1.3),"flexibility": (4,0.8),
        "reaction": (3,0.4),"balance": (5,1.2),"rhythm": (2,0.2),
        "team": (1,0.3),"contact": (1,0.3),"competition": (4,0.9),
        "precision": (5,1.2),"discipline": (5,1.8),
    },
    "ММА": {
        "activity": (5,1.2),"speed": (5,1.6),"strength": (5,1.6),
        "endurance": (5,1.6),"coordination": (5,1.5),"flexibility": (3,0.7),
        "reaction": (5,1.7),"balance": (4,1.2),"rhythm": (3,0.4),
        "team": (1,0.3),"contact": (5,2.0),"competition": (5,1.5),
        "precision": (4,0.9),"discipline": (5,1.5),
    },
}

QUALITIES = [
    "activity","speed","strength","endurance","coordination","flexibility",
    "reaction","balance","rhythm","team","contact","competition",
    "precision","discipline",
]

def age_info(age):
    return [
        {"sport": sport, "min_age": info["min_age"], "mode": info["mode"]}
        for sport, info in AGE_INFO.items() if age >= info["min_age"]
    ]

def available_sports(age):
    if age <= 6:
        return ["Спортивная акробатика", "Прыжки на батуте"]
    return [s for s, i in AGE_INFO.items() if age >= i["min_age"]]

def _five_point_match(answer, target):
    # 5-балльная шкала: точное совпадение максимально,
    # соседний уровень всё ещё даёт высокий вклад.
    d = abs(float(answer) - float(target))
    return {0: 1.00, 1: 0.86, 2: 0.60, 3: 0.32, 4: 0.12}.get(int(d), 0.12)

def _height_weight_profile(age, sex, height_cm, weight_kg):
    """
    Нейтральный антропометрический фактор.
    Не диагностирует состояние здоровья.
    Для точного WHO z-score нужны таблицы WHO AnthroPlus.
    """
    if not height_cm or not weight_kg:
        return {"bmi": None, "height_ratio": 1.0, "body_ratio": 1.0, "category": "нет данных"}

    h = height_cm / 100.0
    bmi = weight_kg / (h * h)

    # Внутренние ориентиры не являются медицинскими границами.
    # Они только предотвращают слишком сильное влияние антропометрии.
    height_ratio = max(0.75, min(1.25, height_cm / (age * 6.0 + 80.0)))
    bmi_ratio = max(0.75, min(1.25, bmi / 18.0))

    if bmi < 13:
        category = "очень лёгкое телосложение"
    elif bmi < 16:
        category = "лёгкое телосложение"
    elif bmi < 22:
        category = "среднее телосложение"
    elif bmi < 27:
        category = "плотное телосложение"
    else:
        category = "крупное телосложение"

    return {
        "bmi": round(bmi, 1),
        "height_ratio": height_ratio,
        "body_ratio": bmi_ratio,
        "category": category,
    }

def _anthro_bonus(sport, anthro, age):
    if anthro["bmi"] is None:
        return 0.0

    # Антропометрия имеет ограниченный вес.
    # Основу результата составляют ответы ребёнка.
    bmi = anthro["bmi"]
    height_ratio = anthro["height_ratio"]

    bonus = 0.0

    if sport in ("Спортивная акробатика", "Прыжки на батуте"):
        # Не наказываем ребёнка за слабость: для 5–6 лет
        # это развивающие направления.
        if age <= 6:
            return 0.0
        if 0.82 <= height_ratio <= 1.18 and 15 <= bmi <= 22:
            bonus += 2.0

    if sport in ("Вольная борьба", "Дзюдо", "Самбо", "ММА", "Бокс"):
        if 16 <= bmi <= 25:
            bonus += 2.0

    if sport == "Тяжёлая атлетика":
        if bmi >= 16 and height_ratio <= 1.15:
            bonus += 2.5

    if sport == "Стрельба из лука":
        if 15 <= bmi <= 24:
            bonus += 1.5

    return bonus

def _specific_bonus(sport, answers):
    score = 0.0
    contact = answers.get("contact", 3)
    competition = answers.get("competition", 3)
    precision = answers.get("precision", 3)
    discipline = answers.get("discipline", 3)
    coordination = answers.get("coordination", 3)
    balance = answers.get("balance", 3)
    flexibility = answers.get("flexibility", 3)
    strength = answers.get("strength", 3)

    if sport in {"Бокс","Дзюдо","Самбо","Вольная борьба","ММА"}:
        if contact == 5: score += 4
        elif contact == 1: score -= 8
        if competition == 5: score += 2
        elif competition == 1: score -= 3

    if sport == "Спортивная акробатика":
        if coordination >= 4: score += 3
        if balance >= 4: score += 3
        if flexibility >= 4: score += 3

    if sport == "Прыжки на батуте":
        if coordination >= 4: score += 3
        if balance >= 4: score += 3
        if precision >= 4: score += 2

    if sport == "Стрельба из лука":
        if precision >= 4: score += 4
        if discipline >= 4: score += 3

    if sport == "Тяжёлая атлетика":
        if strength >= 4: score += 5
        elif strength <= 2: score -= 4

    return score

def _development_percent(raw):
    # Высокая совместимость профиля = высокий процент.
    # Нижняя граница для развивающих направлений выше,
    # чтобы слабая текущая физическая форма не превращалась
    # в ложное "спорт не подходит".
    return round(max(55.0, min(98.0, 55.0 + raw * 43.0)), 1)

def _sport_percent(raw, age):
    # Для спортивной специализации процент не должен
    # автоматически становиться 100%.
    return round(max(45.0, min(97.0, 45.0 + raw * 52.0)), 1)

def recommend(answers):
    try:
        age = int(answers.get("age", 0))
    except Exception:
        return []

    if age < 5 or age > 18:
        return []

    allowed = available_sports(age)

    sex = int(answers.get("sex", 1))
    height = float(answers.get("height", 0) or 0)
    weight = float(answers.get("weight", 0) or 0)

    anthro = _height_weight_profile(age, sex, height, weight)
    results = []

    for sport in allowed:
        profile = SPORTS[sport]
        total = 0.0
        total_weight = 0.0

        for quality, (target, weight_q) in profile.items():
            answer = float(answers.get(quality, 3))
            total += _five_point_match(answer, target) * weight_q
            total_weight += weight_q

        base = total / total_weight if total_weight else 0.0

        # Антропометрия — ограниченный дополнительный фактор.
        anthro_bonus = _anthro_bonus(sport, anthro, age) / 100.0
        specific_bonus = _specific_bonus(sport, answers) / 100.0

        combined = max(0.0, min(1.0, base * 0.90 + anthro_bonus + specific_bonus))

        if age <= 6:
            percent = _development_percent(combined)
        else:
            percent = _sport_percent(combined, age)

        results.append({
            "sport": sport,
            "percent": int(round(percent)),
            "score": round(combined * 100, 1),
            "mode": AGE_INFO[sport]["mode"],
            "anthropometry": anthro["category"],
        })

    results.sort(key=lambda x: (x["percent"], x["score"]), reverse=True)
    return results

def explain_recommendation(item, answers):
    sport = item["sport"]
    reasons = []
    improve = []

    if answers.get("coordination", 3) >= 4:
        reasons.append("хорошая координация")
    if answers.get("balance", 3) >= 4:
        reasons.append("хорошее чувство равновесия")
    if answers.get("flexibility", 3) >= 4:
        reasons.append("хорошая гибкость")
    if answers.get("reaction", 3) >= 4:
        reasons.append("быстрая реакция")
    if answers.get("speed", 3) >= 4:
        reasons.append("хорошая скорость")
    if answers.get("strength", 3) >= 4:
        reasons.append("хороший силовой потенциал")
    if answers.get("endurance", 3) >= 4:
        reasons.append("хорошая выносливость")
    if answers.get("precision", 3) >= 4:
        reasons.append("высокая точность")
    if answers.get("discipline", 3) >= 4:
        reasons.append("хорошая дисциплина")

    for q, label in [
        ("strength","силу"),("endurance","выносливость"),
        ("coordination","координацию"),("flexibility","гибкость"),
        ("balance","равновесие"),("reaction","реакцию")
    ]:
        if answers.get(q, 3) <= 2 and label not in improve:
            improve.append(label)

    if not reasons:
        reasons.append("профиль ребёнка в целом соответствует требованиям направления")

    if not improve:
        improve.append("постепенно развивать общую физическую подготовку")

    if age := int(answers.get("age", 0)):
        if age <= 6 and sport in ("Спортивная акробатика","Прыжки на батуте"):
            mode = "рекомендуется прежде всего для общего физического развития"

    return {
        "reasons": reasons[:4],
        "improve": improve[:3],
    }
