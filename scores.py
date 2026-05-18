import json
from pathlib import Path
from datetime import datetime

SCORES_FILE = Path(__file__).parent / "highscores.json"

def load_scores():
    if SCORES_FILE.exists():
        try:
            return json.loads(SCORES_FILE.read_text())
        except json.JSONDecodeError:
            return []
    return []

def save_score(name, score, difficulty="medium"):
    scores = load_scores()
    entry = {
        "name": name,
        "score": score,
        "difficulty": difficulty,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    scores.append(entry)
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:20]  # Keep top 20
    SCORES_FILE.write_text(json.dumps(scores, indent=2))
    return get_rank(score, scores)

def get_rank(score, scores=None):
    if scores is None:
        scores = load_scores()
    for i, s in enumerate(scores, 1):
        if s["score"] == score:
            return i
    return len(scores) + 1

def show_scores(difficulty=None):
    scores = load_scores()
    if difficulty:
        scores = [s for s in scores if s.get("difficulty") == difficulty]
    if not scores:
        print("No high scores yet!")
        return
    print("\n=== HIGH SCORES ===")
    if difficulty:
        print(f"Difficulty: {difficulty}")
    print(f"{'#':<4} {'Name':15} {'Score':>6} {'Difficulty':>10} {'Date':>12}")
    print("-" * 50)
    for i, s in enumerate(scores, 1):
        print(f"{i:<4} {s['name']:15} {s['score']:>6} {s.get('difficulty', 'N/A'):>10} {s.get('date', 'N/A'):>12}")

def clear_scores():
    SCORES_FILE.write_text("[]")
    print("High scores cleared.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_scores()
    elif len(sys.argv) > 1:
        show_scores(sys.argv[1])
    else:
        show_scores()
