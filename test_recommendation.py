from engine import recommend


profile = {
    "age": 9,

    "qualities": {
        "speed": 4,
        "strength": 5,
        "coordination": 5,
        "endurance": 4,
        "flexibility": 3,
    },

    "preferences": {
        "competition": 5,
        "contact": 5,
        "individual": 5,
        "team": 1,
    }
}


results = recommend(profile)


print()
print("РЕКОМЕНДАЦИИ:")
print("=" * 40)

for i, item in enumerate(results, 1):
    print(
        f"{i}. {item['name']} — "
        f"{item['score']}%"
    )