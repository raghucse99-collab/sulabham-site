# Spread the correct answers of one section evenly over a-d (used from Mock 3 on).
# Only questions whose option order is free are touched (not statement-combination,
# Assertion-Reason or the fixed logic options), exactly like build.py.
from mk import C,AR
FIX=set(e for e,t in C.values())|set(e for e,t in AR)|{"Only I is implicit","Only argument I is strong","Only conclusion I follows","Only course of action I follows"}
def bal(Q):
    free=[q for q in Q if q["o"][0]["en"] not in FIX]
    cnt=[0,0,0,0]
    for q in Q:
        if q["o"][0]["en"] in FIX:cnt[q["a"]]+=1
    for i,q in enumerate(free):
        t=min(range(4),key=lambda k:(cnt[k],(k-i)%4))
        a=q["a"];q["o"][a],q["o"][t]=q["o"][t],q["o"][a];q["a"]=t;cnt[t]+=1
    return Q
