BEATS = {"R": "P", "P": "S", "S": "R"}


def predict_quincy(opp, mine):
    if len(opp) >= 5:
        return opp[-5]
    return "R"


def predict_kris(opp, mine):
    last = mine[-1] if mine else "R"
    return BEATS[last]


def predict_mrugesh(opp, mine):
    last_ten = ([""] + mine)[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    if most_frequent == "":
        most_frequent = "S"
    return BEATS[most_frequent]


def predict_abbey(opp, mine):
    hist = ["R"] + mine
    counts = {a + b: 0 for a in "RPS" for b in "RPS"}
    for a, b in zip(hist, hist[1:]):
        counts[a + b] += 1
    candidates = [hist[-1] + m for m in "RPS"]
    best = max(candidates, key=lambda k: counts[k])
    return BEATS[best[-1]]


MODELS = [predict_quincy, predict_kris, predict_mrugesh, predict_abbey]


def player(prev_play, state={}):
    if prev_play == "":
        state.clear()
        state.update(opp=[], mine=[], scores=[0] * len(MODELS), preds=None)

    opp, mine = state["opp"], state["mine"]

    if prev_play:
        opp.append(prev_play)
        if state["preds"]:
            for i, guess in enumerate(state["preds"]):
                if guess == prev_play:
                    state["scores"][i] += 1

    preds = [model(opp, mine) for model in MODELS]
    state["preds"] = preds

    best = max(range(len(MODELS)), key=lambda i: state["scores"][i])
    move = BEATS[preds[best]]
    mine.append(move)
    return move