import json
import argparse
from pathlib import Path
import statistics

def semantic_distance(a: str, b: str) -> float:
    # TODO: replace with real embedding distance (GPT/Grok)
    return abs(len(a) - len(b)) / 100

def compute_task_score(resonance_turns):
    # Placeholder heuristic: more stable chain = higher score
    return min(1.0, 0.5 + len(resonance_turns) * 0.05)

def compute_harmonic_score(resonance_turns):
    # Placeholder: small semantic drift = good harmony
    drifts = []
    for t in resonance_turns:
        d = semantic_distance(t["a_output"], t["b_output"])
        drifts.append(d)
    avg = statistics.mean(drifts)
    return max(0.0, 1.0 - avg)

def compute_drift_score(resonance_turns):
    drifts = []
    for t in resonance_turns:
        d = semantic_distance(t["input"], t["b_output"])
        drifts.append(d)
    avg = statistics.mean(drifts)
    return max(0.0, 1.0 - avg)

def compute_por_gain(solo_score, multi_score):
    if solo_score == 0:
        return 0
    return (multi_score - solo_score) / solo_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo", required=True, help="solo run jsonl")
    parser.add_argument("--res", required=True, help="resonance run jsonl")
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    import yaml
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    w1 = cfg["weights"]["w1"]
    w2 = cfg["weights"]["w2"]
    w3 = cfg["weights"]["w3"]

    # Load solo results
    solo_map = {}
    with open(args.solo, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            solo_map[r["task_id"]] = r

    # Load resonance results
    res_map = {}
    with open(args.res, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            res_map[r["task_id"]] = r

    outputs = []

    for task_id in res_map:
        res_r = res_map[task_id]
        solo_r = solo_map.get(task_id)

        turns = res_r["turns"]

        # compute 3 metric components
        task_score = compute_task_score(turns)
        harmonic_score = compute_harmonic_score(turns)
        drift_score = compute_drift_score(turns)

        # weighted PoR total
        por_total = (
            w1 * task_score +
            w2 * harmonic_score +
            w3 * drift_score
        )

        # PoR Gain
        solo_score = solo_r.get("task_score", 0)
        por_gain = compute_por_gain(solo_score, task_score)

        outputs.append({
            "task_id": task_id,
            "solo_score": solo_score,
            "task_score": task_score,
            "harmonic_score": harmonic_score,
            "drift_score": drift_score,
            "por_total": por_total,
            "por_gain": por_gain,
        })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        for o in outputs:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    print(f"Saved PoR evaluation → {out_path}")

if __name__ == "__main__":
    main()
