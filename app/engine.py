from .sports import SPORTS

def build_profile(vectors):
    totals={}; counts={}
    for v in vectors:
        for k,val in v.items():
            totals[k]=totals.get(k,0)+val
            counts[k]=counts.get(k,0)+1
    return {k:max(1,min(5,round(totals[k]/counts[k]))) for k in totals}

def score_sports(profile, age=None):
    results=[]
    for key,sport in SPORTS.items():
        numerator=0; denominator=0
        for q,child in profile.items():
            if q in sport["tags"]:
                numerator += child*sport["tags"][q]
                denominator += 5*sport["tags"][q]
        score=round(numerator/denominator*100) if denominator else 0
        # Small age guardrails for MVP: avoid presenting weightlifting as first choice for very young children.
        if age is not None and age < 8 and key == "weightlifting": score=min(score,60)
        results.append((key,score))
    return sorted(results,key=lambda x:x[1],reverse=True)

def explain(key,profile):
    names={"speed":"скорость","reaction":"реакция","strength":"сила","endurance":"выносливость","coordination":"координация","flexibility":"гибкость","balance":"равновесие","contact":"интерес к контактному взаимодействию","competition":"соревновательность","individual":"индивидуальный формат","team":"командный формат","precision":"точность","rhythm":"чувство ритма","jumping":"интерес к прыжкам","outdoor":"интерес к занятиям на открытом воздухе"}
    tags=SPORTS[key]["tags"]
    matches=sorted(((names[q],profile.get(q,0)*tags[q]) for q in tags if q in profile),key=lambda x:x[1],reverse=True)
    return [n for n,v in matches[:3] if v>0]
