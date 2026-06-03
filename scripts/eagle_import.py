"""Import generated image files into a running Eagle library.

This helper uses Eagle's local HTTP API. It intentionally has no third-party
dependencies so a Codex automation can call it from a fresh Python install.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_API = "http://localhost:41595"
DEFAULT_LEDGER = Path("runs") / ".eagle_import_ledger.json"


def request_json(api: str, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(f"{api.rstrip('/')}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Eagle API request failed: {exc}") from exc


def flatten_folders(folders: list[dict[str, Any]], prefix: str = "") -> list[dict[str, str]]:
    flat: list[dict[str, str]] = []
    for folder in folders:
        name = str(folder.get("name", ""))
        folder_id = str(folder.get("id", ""))
        path = f"{prefix}/{name}" if prefix else name
        flat.append({"id": folder_id, "name": name, "path": path})
        children = folder.get("children") or []
        flat.extend(flatten_folders(children, path))
    return flat


def get_folders(api: str) -> list[dict[str, str]]:
    response = request_json(api, "GET", "/api/folder/list")
    if response.get("status") != "success":
        raise RuntimeError(f"Eagle folder/list returned non-success: {response}")
    return flatten_folders(response.get("data") or [])


def list_recent_items(api: str, limit: int = 200) -> list[dict[str, Any]]:
    response = request_json(api, "GET", f"/api/item/list?limit={limit}")
    if response.get("status") != "success":
        raise RuntimeError(f"Eagle item/list returned non-success: {response}")
    return response.get("data") or []


def resolve_folder_id(api: str, folder_id: str | None, folder_name: str | None) -> str | None:
    if folder_id:
        return folder_id
    if not folder_name:
        return None

    matches = [
        folder
        for folder in get_folders(api)
        if folder["name"] == folder_name or folder["path"] == folder_name
    ]
    if not matches:
        raise RuntimeError(f"No Eagle folder matched: {folder_name}")
    if len(matches) > 1:
        names = ", ".join(f'{m["path"]} ({m["id"]})' for m in matches[:8])
        raise RuntimeError(f"Multiple Eagle folders matched {folder_name!r}: {names}")
    return matches[0]["id"]


def split_tags(values: list[str]) -> list[str]:
    tags: list[str] = []
    for value in values:
        tags.extend(part.strip() for part in value.split(","))
    return [tag for tag in tags if tag]


def read_annotation(args: argparse.Namespace) -> str:
    if args.annotation_file:
        return Path(args.annotation_file).read_text(encoding="utf-8")
    return args.annotation or ""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "imports": {}}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "imports" not in data:
        data["imports"] = {}
    return data


def save_ledger(path: Path, ledger: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ledger_key(path: Path, digest: str) -> str:
    return f"{path.resolve()}::{digest}"


def known_in_ledger(path: Path, digest: str, ledger: dict[str, Any]) -> dict[str, Any] | None:
    imports = ledger.get("imports") or {}
    key = ledger_key(path, digest)
    if key in imports:
        return imports[key]
    for record in imports.values():
        if record.get("sha256") == digest:
            return record
    return None


def update_ledger(path: Path, digest: str, ledger: dict[str, Any], response: dict[str, Any]) -> None:
    imports = ledger.setdefault("imports", {})
    data = response.get("data")
    imports[ledger_key(path, digest)] = {
        "path": str(path.resolve()),
        "sha256": digest,
        "size": path.stat().st_size,
        "eagle_item": data,
    }


def matching_eagle_item(path: Path, recent_items: list[dict[str, Any]]) -> dict[str, Any] | None:
    stem = path.stem
    size = path.stat().st_size
    for item in recent_items:
        if item.get("name") == stem and item.get("size") == size and not item.get("isDeleted"):
            return item
    return None


def import_path(api: str, path: Path, folder_id: str | None, tags: list[str], annotation: str, name_prefix: str) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Image file does not exist: {path}")
    if not path.is_file():
        raise RuntimeError(f"Path is not a file: {path}")

    payload: dict[str, Any] = {
        "path": str(path.resolve()),
        "name": f"{name_prefix}{path.stem}" if name_prefix else path.stem,
        "tags": tags,
        "annotation": annotation,
    }
    if folder_id:
        payload["folderId"] = folder_id

    response = request_json(api, "POST", "/api/item/addFromPath", payload)
    if response.get("status") != "success":
        raise RuntimeError(f"Eagle import failed for {path}: {response}")
    return response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import image files into Eagle through the local API.")
    parser.add_argument("paths", nargs="*", help="Image paths to import.")
    parser.add_argument("--api", default=DEFAULT_API, help=f"Eagle API base URL. Default: {DEFAULT_API}")
    parser.add_argument("--folder-id", help="Target Eagle folder id.")
    parser.add_argument("--folder-name", help="Target Eagle folder name or full nested path.")
    parser.add_argument("--tag", action="append", default=[], help="Tag or comma-separated tags. Can be repeated.")
    parser.add_argument("--annotation", default="", help="Annotation text stored in Eagle.")
    parser.add_argument("--annotation-file", help="Read annotation text from a UTF-8 file.")
    parser.add_argument("--name-prefix", default="", help="Prefix for imported Eagle item names.")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER), help="Local JSON ledger used to skip duplicate imports.")
    parser.add_argument("--no-ledger", action="store_true", help="Disable local duplicate ledger checks.")
    parser.add_argument("--no-eagle-dedupe", action="store_true", help="Disable Eagle recent-item name/size duplicate checks.")
    parser.add_argument("--force", action="store_true", help="Import even if the file appears to be already imported.")
    parser.add_argument("--list-folders", action="store_true", help="Print Eagle folders and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned imports without calling addFromPath.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_folders:
        for folder in get_folders(args.api):
            print(f'{folder["id"]}\t{folder["path"]}')
        return 0

    if not args.paths:
        parser.error("provide at least one image path, or use --list-folders")

    folder_id = resolve_folder_id(args.api, args.folder_id, args.folder_name)
    tags = split_tags(args.tag)
    annotation = read_annotation(args)
    paths = [Path(path) for path in args.paths]
    ledger_path = Path(args.ledger)
    ledger = {"version": 1, "imports": {}} if args.no_ledger else load_ledger(ledger_path)
    recent_items = [] if args.no_eagle_dedupe else list_recent_items(args.api, 300)

    if args.dry_run:
        planned = []
        for path in paths:
            exists = path.exists() and path.is_file()
            digest = file_sha256(path) if exists else None
            planned.append(
                {
                    "path": str(path),
                    "exists": exists,
                    "sha256": digest,
                    "known_in_ledger": bool(digest and known_in_ledger(path, digest, ledger)),
                    "matching_eagle_item": matching_eagle_item(path, recent_items) if exists and digest else None,
                }
            )
        print(
            json.dumps(
                {
                    "api": args.api,
                    "folder_id": folder_id,
                    "tags": tags,
                    "annotation_chars": len(annotation),
                    "paths": planned,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    results = []
    for path in paths:
        if not path.exists() or not path.is_file():
            raise RuntimeError(f"Image file does not exist: {path}")
        digest = file_sha256(path)
        if not args.force:
            ledger_record = None if args.no_ledger else known_in_ledger(path, digest, ledger)
            if ledger_record:
                results.append(
                    {
                        "path": str(path),
                        "status": "skipped",
                        "reason": "known_in_local_ledger",
                        "data": ledger_record.get("eagle_item"),
                    }
                )
                continue

            eagle_item = None if args.no_eagle_dedupe else matching_eagle_item(path, recent_items)
            if eagle_item:
                results.append(
                    {
                        "path": str(path),
                        "status": "skipped",
                        "reason": "matching_eagle_item_name_and_size",
                        "data": eagle_item.get("id"),
                    }
                )
                update_ledger(path, digest, ledger, {"data": eagle_item.get("id")})
                continue

        response = import_path(args.api, path, folder_id, tags, annotation, args.name_prefix)
        data = response.get("data")
        results.append({"path": str(path), "status": "imported", "data": data})
        update_ledger(path, digest, ledger, response)

    if not args.no_ledger:
        save_ledger(ledger_path, ledger)

    print(json.dumps({"status": "success", "imported": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - CLI should return a readable message.
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
