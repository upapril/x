#!/usr/bin/env python3
"""Ingest a CallDynamicTool write_to_file X API response into the research archive."""
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
SHANGHAI = timezone(timedelta(hours=8))

HANDLES = {
    "615818451": "alexandr_wang",
    "1589763597705437184": "iiiinvest",
    "1435990322702520320": "silverfang88",
    "368245720": "taresky",
    "705564530936418304": "thankUcrypto",
}

def now_utc():
    return datetime.now(timezone.utc)

def to_shanghai(iso):
    if not iso:
        return None
    s = iso.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S GMT+8")

def extract_json(text: str, path: Path | None = None):
    # If the write_to_file view was truncated, follow the "Full text:" pointer.
    mfull = re.search(r"Full text:\s*(\S+)", text)
    if mfull and ("bytes " in text and "omitted" in text):
        full = Path(mfull.group(1).rstrip("."))
        if full.exists() and (path is None or full.resolve() != Path(path).resolve()):
            text = full.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<cursor_untrusted_data[^>]*>\s*(.*?)\s*</cursor_untrusted_data[^>]*>", text, re.S)
    body = m.group(1) if m else text
    i = body.find("{")
    j = body.rfind("}")
    if i < 0 or j <= i:
        raise ValueError("no JSON object found")
    blob = body[i:j+1]
    try:
        return json.loads(blob, strict=False)
    except json.JSONDecodeError:
        return json.loads(_repair_json_strings(blob), strict=False)

def _repair_json_strings(s: str) -> str:
    """Escape raw newlines/control chars that sometimes appear inside JSON strings."""
    out = []
    in_str = False
    esc = False
    for c in s:
        if in_str:
            if esc:
                out.append(c)
                esc = False
            elif c == "\\":
                out.append(c)
                esc = True
            elif c == '"':
                out.append(c)
                in_str = False
            elif c == "\n":
                out.append("\\n")
            elif c == "\r":
                out.append("\\r")
            elif c == "\t":
                out.append("\\t")
            elif ord(c) < 32:
                out.append("\\u%04x" % ord(c))
            else:
                out.append(c)
        else:
            if c == '"':
                in_str = True
            out.append(c)
    return "".join(out)

def classify_post(post, author_id):
    refs = post.get("referenced_tweets") or post.get("referenced_posts") or []
    types = {r.get("type") for r in refs if isinstance(r, dict)}
    if "retweeted" in types or "reposted" in types:
        kind = "repost"
    elif "quoted" in types:
        kind = "quote"
    elif "replied_to" in types or post.get("in_reply_to_user_id"):
        kind = "reply"
    else:
        kind = "original"
    text = post.get("text") or ""
    if text.startswith("RT @") and kind == "original":
        kind = "repost"
    return kind, refs

def referenced_ids(refs):
    out = []
    for r in refs or []:
        if isinstance(r, dict) and r.get("id") is not None:
            out.append({"type": r.get("type"), "id": str(r.get("id"))})
    return out

def normalize_post(post, includes, source_meta):
    author_id = str(post.get("author_id") or "")
    pid = str(post.get("id"))
    kind, refs = classify_post(post, author_id)
    note = post.get("note_tweet") or post.get("note_post") or {}
    full_text = None
    if isinstance(note, dict):
        full_text = note.get("text")
        if not full_text and isinstance(note.get("note_tweet"), dict):
            full_text = note["note_tweet"].get("text")
    text = post.get("text") or ""
    created = post.get("created_at")
    metrics = post.get("public_metrics") or {}
    if "retweet_count" in metrics and "repost_count" not in metrics:
        metrics = dict(metrics)
        metrics["repost_count"] = metrics.get("retweet_count")
    url = post.get("url") or f"https://x.com/i/status/{pid}"
    users = {str(u.get("id")): u for u in (includes.get("users") or [])}
    posts_inc = {str(p.get("id")): p for p in (includes.get("posts") or includes.get("tweets") or [])}
    media = {m.get("media_key"): m for m in (includes.get("media") or [])}
    polls = {str(p.get("id")): p for p in (includes.get("polls") or [])}
    media_keys = ((post.get("attachments") or {}).get("media_keys") or [])
    poll_ids = [str(x) for x in ((post.get("attachments") or {}).get("poll_ids") or [])]
    author = users.get(author_id) or {}
    username = author.get("username") or HANDLES.get(author_id)
    rec = {
        "id": pid,
        "author_id": author_id,
        "author_username": username,
        "author_name": author.get("name"),
        "created_at_utc": created,
        "created_at_shanghai": to_shanghai(created),
        "post_type": kind,
        "lang": post.get("lang"),
        "text": text,
        "full_text": full_text if full_text and full_text != text else None,
        "conversation_id": str(post["conversation_id"]) if post.get("conversation_id") else None,
        "in_reply_to_user_id": str(post["in_reply_to_user_id"]) if post.get("in_reply_to_user_id") else None,
        "referenced_tweets": referenced_ids(refs),
        "public_metrics": metrics,
        "possibly_sensitive": post.get("possibly_sensitive"),
        "reply_settings": post.get("reply_settings"),
        "source": post.get("source"),
        "entities": post.get("entities"),
        "attachments": {
            "media_keys": media_keys,
            "poll_ids": poll_ids,
            "media": [media[k] for k in media_keys if k in media],
            "polls": [polls[i] for i in poll_ids if i in polls],
        } if (media_keys or poll_ids) else None,
        "community_id": str(post["community_id"]) if post.get("community_id") else None,
        "geo": post.get("geo"),
        "card_uri": post.get("card_uri"),
        "withheld": post.get("withheld"),
        "edit_controls": post.get("edit_controls"),
        "edit_history_ids": [str(x) for x in (post.get("edit_history_tweet_ids") or post.get("edit_history_post_ids") or [])],
        "canonical_url": url if str(url).startswith("http") else f"https://x.com/i/status/{pid}",
        "article": post.get("article") or post.get("article_title"),
        "collection": source_meta,
    }
    ref_expanded = []
    for r in rec["referenced_tweets"]:
        rp = posts_inc.get(r["id"])
        if rp:
            ref_expanded.append({
                "id": str(rp.get("id")),
                "type": r["type"],
                "author_id": str(rp.get("author_id")) if rp.get("author_id") else None,
                "created_at_utc": rp.get("created_at"),
                "text": rp.get("text"),
                "lang": rp.get("lang"),
                "public_metrics": rp.get("public_metrics"),
            })
    rec["referenced_expanded"] = ref_expanded or None
    return rec

def load_jsonl(path: Path):
    """Load JSONL. If a record was split by a raw newline, join and escape losslessly."""
    rows = []
    if not path.exists():
        return rows
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    n = len(lines)
    while i < n:
        buf = lines[i]
        i += 1
        if not buf.strip():
            continue
        while True:
            try:
                rows.append(json.loads(buf))
                break
            except json.JSONDecodeError:
                if i >= n:
                    rows.append(json.loads(_repair_json_strings(buf)))
                    break
                # Join at most one continuation line, then escape raw breaks.
                buf = buf + "\n" + lines[i]
                i += 1
                try:
                    rows.append(json.loads(_repair_json_strings(buf)))
                    break
                except json.JSONDecodeError:
                    # rare: more than one split; keep joining one more
                    continue
    return rows

def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def ingest(path: Path, handle_hint=None, tool="get_users_posts", page_name=None, request_meta=None):
    text = path.read_text(encoding="utf-8", errors="replace")
    obj = extract_json(text, path)
    request_meta = dict(request_meta or {})
    data = obj.get("data") or []
    includes = obj.get("includes") or {}
    meta = obj.get("meta") or {}
    errors = obj.get("errors") or []
    if not data and not meta and not errors:
        raise ValueError(f"unexpected payload keys: {list(obj.keys())}")

    handle = handle_hint
    if not handle and data:
        aid = str(data[0].get("author_id") or "")
        handle = HANDLES.get(aid)
    if not handle:
        raise ValueError("could not determine handle")

    dest = ROOT / handle
    raw_dir = dest / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    collected_at = now_utc()
    collected_iso = collected_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    collected_sh = collected_at.astimezone(SHANGHAI).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    page_idx_path = dest / "raw" / "_page_index.json"
    page_index = json.loads(page_idx_path.read_text()) if page_idx_path.exists() else {"pages": []}
    n = len(page_index["pages"]) + 1
    page_name = page_name or f"page_{n:04d}_{tool}.json"
    source_meta = {
        "tool": f"x.{tool}",
        "source_file": str(path),
        "collected_at_utc": collected_iso,
        "collected_at_shanghai": collected_sh,
        "page_file": f"raw/{page_name}",
        "result_count": meta.get("result_count"),
        "newest_id": str(meta["newest_id"]) if meta.get("newest_id") else None,
        "oldest_id": str(meta["oldest_id"]) if meta.get("oldest_id") else None,
        "pagination_token_in": request_meta.get("input_token"),
        "pagination_token_out": meta.get("next_token"),
        "query": request_meta.get("query"),
        "start_time": request_meta.get("start_time"),
        "end_time": request_meta.get("end_time"),
        "sort_order": request_meta.get("sort_order"),
        "window_label": request_meta.get("window_label"),
    }
    raw_payload = {
        "collected_at_utc": collected_iso,
        "collected_at_shanghai": collected_sh,
        "tool": f"x.{tool}",
        "source_file": str(path),
        "request": {
            "query": request_meta.get("query"),
            "start_time": request_meta.get("start_time"),
            "end_time": request_meta.get("end_time"),
            "sort_order": request_meta.get("sort_order") or "recency",
            "max_results": request_meta.get("max_results") or 25,
            "input_token": request_meta.get("input_token"),
            "window_label": request_meta.get("window_label"),
        },
        "data": data,
        "includes": includes,
        "meta": meta,
        "errors": errors,
    }
    (raw_dir / page_name).write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    norms = [normalize_post(p, includes, source_meta) for p in data]
    jsonl_path = dest / "normalized" / "posts.jsonl"
    existing = load_jsonl(jsonl_path)
    have = {r["id"] for r in existing}
    added = 0
    dupes = 0
    for r in norms:
        if r["id"] in have:
            dupes += 1
            continue
        existing.append(r)
        have.add(r["id"])
        added += 1
    existing.sort(key=lambda r: (r.get("created_at_utc") or "", r["id"]), reverse=True)
    write_jsonl(jsonl_path, existing)

    dates = [r.get("created_at_utc") for r in norms if r.get("created_at_utc")]
    types = defaultdict(int)
    for r in norms:
        types[r["post_type"]] += 1

    page_rec = {
        "page": n,
        "file": page_name,
        "tool": tool,
        "result_count": meta.get("result_count", len(data)),
        "returned": len(data),
        "added": added,
        "duplicates_in_page": dupes,
        "newest_id": source_meta["newest_id"],
        "oldest_id": source_meta["oldest_id"],
        "newest_created_at": max(dates) if dates else None,
        "oldest_created_at": min(dates) if dates else None,
        "next_token": meta.get("next_token"),
        "input_token": request_meta.get("input_token"),
        "query": request_meta.get("query"),
        "start_time": request_meta.get("start_time"),
        "end_time": request_meta.get("end_time"),
        "window_label": request_meta.get("window_label"),
        "type_counts": dict(types),
        "errors_count": len(errors) if isinstance(errors, list) else (1 if errors else 0),
        "collected_at_utc": collected_iso,
    }
    if errors:
        page_rec["errors"] = errors
    page_index["pages"].append(page_rec)
    page_index["latest_next_token"] = meta.get("next_token")
    page_index["updated_at_utc"] = collected_iso
    page_idx_path.write_text(json.dumps(page_index, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "handle": handle,
        "added": added,
        "duplicates": dupes,
        "returned": len(data),
        "archive_total": len(existing),
        "page": n,
        "next_token": meta.get("next_token"),
        "oldest_in_page": min(dates) if dates else None,
        "newest_in_page": max(dates) if dates else None,
        "type_counts": dict(types),
        "errors": errors[:3] if isinstance(errors, list) else errors,
        "end_of_results": not bool(meta.get("next_token")),
    }
    return summary

if __name__ == "__main__":
    path = Path(sys.argv[1])
    handle = sys.argv[2] if len(sys.argv) > 2 else None
    tool = sys.argv[3] if len(sys.argv) > 3 else "get_users_posts"
    s = ingest(path, handle, tool)
    print(json.dumps(s, ensure_ascii=False, indent=2))
