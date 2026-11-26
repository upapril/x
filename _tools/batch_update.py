#!/usr/bin/env python3
"""Ingest a batch of API pages and update expand_jobs.json.
Usage: batch_update.py handle file1:label1 file2:label2 ...
Files may be bare asset filenames or absolute paths.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ingest_page import ingest

ROOT = Path("/workspace/x-research")
ASSETS = Path("/cursor/stores/user/grok-bot/agents/898997d6-7db9-4848-8f4f-e163f93ec083/assets/")
jobs_path = ROOT / "logs" / "expand_jobs.json"

def main():
    handle = sys.argv[1]
    pairs = sys.argv[2:]
    state = json.loads(jobs_path.read_text())
    def job_by_label(label):
        for j in state["jobs"]:
            if j["handle"] == handle and j["label"] == label:
                return j
        raise KeyError((handle, label))
    last_total = None
    for pair in pairs:
        fn, label = pair.split(":", 1)
        path = Path(fn)
        if not path.exists():
            path = ASSETS / fn
        j = job_by_label(label)
        try:
            # Capture the token that fetched THIS page before overwriting with the output token.
            input_token = j.get("next_token")
            request_meta = {
                "query": f"from:{handle}",
                "start_time": j.get("start_time"),
                "end_time": j.get("end_time"),
                "sort_order": "recency",
                "max_results": 25,
                "input_token": input_token,
                "window_label": label,
            }
            s = ingest(path, handle, "search_posts_all", request_meta=request_meta)
            j["pages_fetched"] = j.get("pages_fetched", 0) + 1
            j["last_input_token"] = input_token
            j["last_request"] = request_meta
            j["posts_returned"] = j.get("posts_returned", 0) + s["returned"]
            j["posts_added"] = j.get("posts_added", 0) + s["added"]
            j["last_span"] = [s["oldest_in_page"], s["newest_in_page"]]
            last_total = s["archive_total"]
            if s.get("next_token"):
                j["next_token"] = s["next_token"]
                if s["next_token"] == input_token and input_token:
                    j["status"] = "pagination_stalled"
                    j["stall_note"] = (
                        "API returned the same next_token as the input_token and a duplicate page. "
                        "Do not reuse this token. Subdivide the remaining earlier window instead."
                    )
                    print(f"STALL {label}: output token identical to input token")
                else:
                    j["status"] = "open"
            else:
                j["next_token"] = None
                j["status"] = "exhausted"
            print(f"{label}: added={s['added']:3d} ret={s['returned']:3d} total={s['archive_total']:4d} {s['oldest_in_page']}->{s['newest_in_page']} end={s['end_of_results']} pages={j['pages_fetched']}")
        except Exception as e:
            j["status"] = "error"
            j["error"] = f"{type(e).__name__}: {e}"
            print(f"FAIL {label} size={path.stat().st_size}: {e}")
    state["calls_this_pass"] = state.get("calls_this_pass", 0) + len(pairs)
    jobs_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    open_j = [j for j in state["jobs"] if j["handle"] == handle and j["status"] == "open"]
    exh = [j for j in state["jobs"] if j["handle"] == handle and j["status"] == "exhausted"]
    print("open", [f"{j['label']}(p{j['pages_fetched']},+{j['posts_added']})" for j in open_j])
    print("exhausted", [f"{j['label']}(p{j['pages_fetched']},+{j['posts_added']})" for j in exh])
    print("calls_this_pass", state["calls_this_pass"], "last_total", last_total)

if __name__ == "__main__":
    main()
