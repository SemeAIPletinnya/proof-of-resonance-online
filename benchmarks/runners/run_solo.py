import json
import argparse
from pathlib import Path

def dummy_model_answer(prompt: str) -> str:
    # TODO: replace with real GPT/Grok/Llama call
    return f"[DUMMY_ANSWER] {prompt[:60]}..."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--model", required=True, help="Model name (for logging)")
    parser.add_argument("--out", required=True, help="Output JSONL path")
    args = parser.parse_args()

    import yaml  # simple YAML loader
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    dataset_path = cfg["dataset_path"]
    track = cfg["track"]

    results = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            task = json.loads(line)
            ans = dummy_model_answer(task["prompt"])

            result = {
                "mode": "solo",
                "track": track,
                "task_id": task["id"],
                "model_name": args.model,
                "response": ans,
                "task_score": 0.0,   # placeholder
                "ha_score": 1.0,
                "drift_score": 1.0
            }
            results.append(result)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Saved {len(results)} solo results to {out_path}")

if __name__ == "__main__":
    main()
