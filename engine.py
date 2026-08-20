from sports import SPORTS


def score_sport(profile, sport):
    score = 0
    max_score = 0

    # Физические качества
    for quality, value in profile["qualities"].items():
        sport_value = sport["qualities"].get(quality, 0)

        score += min(value, sport_value)
        max_score += 5

    # Предпочтения
    for preference, value in profile["preferences"].items():
        sport_value = sport["preferences"].get(preference, 0)

        score += min(value, sport_value)
        max_score += 5

    # Возраст
    age = profile["age"]

    if sport["age_min"] <= age <= sport["age_max"]:
        score += 10
        max_score += 10
    else:
        max_score += 10

    return round(score / max_score * 100)


def recommend(profile):
    results = []

    for sport_id, sport in SPORTS.items():

        score = score_sport(profile, sport)

        results.append({
            "id": sport_id,
            "name": sport["name"],
            "score": score,
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:5]