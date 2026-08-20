from app.engine import build_profile,score_sports

def test_top5_exists():
    p=build_profile([{"speed":5,"reaction":5,"contact":5,"competition":5,"individual":5},{"coordination":5}])
    r=score_sports(p,8)
    assert len(r)==10 and r[0][1]>=r[-1][1]

def test_precision_prefers_archery():
    p=build_profile([{"precision":5,"individual":5},{"precision":5,"balance":4}])
    r=dict(score_sports(p,10))
    assert r["archery"]>r["wrestling"]
