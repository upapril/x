#!/usr/bin/env python3
"""Package a NEW day3 zip and under-25MB parts. Never modify prior ZIPs."""
from __future__ import annotations

import hashlib
import json
import os
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path("/workspace/x-research")
OUT_STEM = Path("/workspace/x-research-day3-final")
MAX_PART = 25_000_000  # exclusive upper bound
SH = timezone(timedelta(hours=8))

PRIOR = {
    Path("/workspace/x-research-firstpass.zip"): "455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976",
    Path("/workspace/x-research-expanded.zip"): "d601957063b3610067d2dafd6cab0a6effb63e771bd642df57233b5e44fee6c7",
    Path("/workspace/x-research-latest.zip"): "1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58",
    Path("/workspace/x-research-day1-final.zip"): "537597c2d1c295f18773fb2099d751338f78a354be982b65a26aaf7367efea37",
    Path("/workspace/x-research-day2-final.zip"): "7b4523860662a9744cc4d52df7642fee4728d6af0fa059a4a108a8fa71302e0b",
    Path("/workspace/x-research-day2-final-part01.zip"): "7c9c77173aa0acaddf16c715f5048c2e55b8f52685ceeb39b63a87f63febd1e3",
    Path("/workspace/x-research-day2-final-part02.zip"): "61c135dd16dae48692414d5435f9fe59568c3d96d327e5a9c5531de2599410b2",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_exclude(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    parts = path.parts
    if "__pycache__" in parts or path.suffix == ".pyc":
        return True
    name = path.name
    if ".bak" in name or name.endswith(".bak"):
        return True
    if path.is_symlink():
        return True
    return False


def iter_files() -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            p = Path(dirpath) / fn
            if should_exclude(p):
                continue
            if not p.is_file():
                continue
            out.append(p)
    out.sort(key=lambda p: p.relative_to(ROOT).as_posix())
    return out


def arcname(path: Path) -> str:
    return ("x-research/" + path.relative_to(ROOT).as_posix()).replace("\\", "/")


def write_sums(files: list[Path]) -> Path:
    # hash everything except FILE_SHA256SUMS.json itself
    items = {}
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        if rel == "FILE_SHA256SUMS.json":
            continue
        items[rel] = sha256_file(p)
    dest = ROOT / "FILE_SHA256SUMS.json"
    payload = {
        "written_at_shanghai": datetime.now(SH).isoformat(),
        "pass": "day3-final",
        "file_count": len(items),
        "files": items,
    }
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


def add_to_zip(zf: zipfile.ZipFile, path: Path) -> None:
    zf.write(path, arcname=arcname(path), compress_type=zipfile.ZIP_DEFLATED)


def build_zip(dest: Path, files: list[Path]) -> dict:
    if dest.exists():
        raise SystemExit(f"refusing to overwrite existing {dest}")
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for p in files:
            add_to_zip(zf, p)
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"CRC failure in {dest}: {bad}")
    # compare packaged hashes to disk for CRC already done; also name set
    with zipfile.ZipFile(dest) as zf:
        names = set(zf.namelist())
        expected = {arcname(p) for p in files}
        if names != expected:
            missing = expected - names
            extra = names - expected
            raise SystemExit(f"zip membership mismatch missing={list(missing)[:5]} extra={list(extra)[:5]}")
    return {"path": str(dest), "size_bytes": dest.stat().st_size, "sha256": sha256_file(dest), "file_count": len(files)}


def measure_zip(files: list[Path], dest: Path) -> int:
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for p in files:
            add_to_zip(zf, p)
    return dest.stat().st_size


def split_parts(files: list[Path]) -> list[dict]:
    """Independently extractable parts, each zip strictly under MAX_PART bytes."""
    parts_meta = []
    idx = 1
    i = 0
    n = len(files)
    while i < n:
        dest = Path(f"{OUT_STEM}-part{idx:02d}.zip")
        if dest.exists():
            raise SystemExit(f"refusing to overwrite existing {dest}")
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        lo, hi = i + 1, n
        best = None
        while lo <= hi:
            mid = (lo + hi) // 2
            size = measure_zip(files[i:mid], tmp)
            if size < MAX_PART:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if best is None:
            raise SystemExit(f"single file will not fit under 25MB even compressed: {files[i]}")
        if tmp.exists():
            tmp.unlink()
        meta = build_zip(tmp, files[i:best])
        tmp.rename(dest)
        meta["path"] = str(dest)
        meta["sha256"] = sha256_file(dest)
        meta["size_bytes"] = dest.stat().st_size
        if meta["size_bytes"] >= MAX_PART:
            dest.unlink()
            raise SystemExit(f"part {dest} is {meta['size_bytes']} >= {MAX_PART}")
        parts_meta.append(meta)
        print("part", idx, dest, "files", best - i, meta["size_bytes"], meta["sha256"])
        i = best
        idx += 1
    return parts_meta


def confirm_prior() -> dict:
    out = {}
    for path, expected in PRIOR.items():
        if not path.is_file():
            raise SystemExit(f"missing prior zip {path}")
        got = sha256_file(path)
        out[str(path)] = {"sha256": got, "expected": expected, "unchanged": got == expected, "size_bytes": path.stat().st_size}
        if got != expected:
            raise SystemExit(f"prior zip hash changed: {path}")
    return out


def main():
    full_path = Path(str(OUT_STEM) + ".zip")
    artifacts_path = Path(str(OUT_STEM) + ".artifacts.json")
    if full_path.exists() or artifacts_path.exists():
        raise SystemExit(f"refusing to overwrite {full_path} or {artifacts_path}")

    prior_before = confirm_prior()
    files = iter_files()
    sums = write_sums(files)
    # include sums file now
    files = iter_files()
    if sums not in files:
        files.append(sums)
        files.sort(key=lambda p: p.relative_to(ROOT).as_posix())

    full_meta = build_zip(full_path, files)
    print("full", full_meta)
    parts = []
    if full_meta["size_bytes"] >= MAX_PART:
        parts = split_parts(files)

    prior_after = confirm_prior()
    artifacts = {
        "written_at_shanghai": datetime.now(SH).isoformat(),
        "pass": "day3-final",
        "unique_total": 53706,
        "counts": {
            "silverfang88": 19848,
            "iiiinvest": 4850,
            "alexandr_wang": 3625,
            "taresky": 17532,
            "thankUcrypto": 7851,
        },
        "day3_calls_ingested": 925,
        "full_zip": full_meta,
        "parts": parts,
        "part_limit_bytes": MAX_PART,
        "file_count": len(files),
        "file_sha256sums": "x-research/FILE_SHA256SUMS.json",
        "validation": "x-research/logs/day3_package_validation.json",
        "remaining_jobs": "x-research/logs/remaining_jobs_day3.json",
        "prior_zips_unchanged_before": prior_before,
        "prior_zips_unchanged_after": prior_after,
        "excluded": ["*.bak*", "__pycache__", ".pyc", "symlinks"],
        "collection_stopped": {
            "reason": "true_75_read_reserve_reached",
            "daily_remaining": 75,
            "usable_to_reserve": 0,
            "reset_shanghai": "2026-11-27 08:00 Asia/Shanghai",
            "footer": "X reads left for this user: 29 of 30 this minute (resets at 2026-11-26T01:32:00.000Z), 75 of 1000 today (resets at 2026-11-27T00:00:00.000Z).",
        },
    }
    artifacts_path.write_text(json.dumps(artifacts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("artifacts", artifacts_path)

    # remaining_jobs_day3.json is frozen into the zip before this step
    # (packaging_status already set). SHA256 of the zips lives in artifacts.

    # Hash-bearing checkpoint is the external artifacts JSON only.
    print("done")


if __name__ == "__main__":
    main()
