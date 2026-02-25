from __future__ import annotations

import base64
import json
import os
import sys
from urllib import error, request

from pr_body_guard_lib import (
    find_marker_path,
    is_safe_relative_path,
    normalize_text,
    validate_text_content,
)


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required env: {name}")
    return value


def _api_get(url: str, token: str) -> dict:
    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "pr-body-guard",
        },
    )
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _fetch_pr(repo: str, pr_number: str, token: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    return _api_get(url, token)


def _fetch_repo_file(repo: str, path: str, ref: str, token: str) -> str:
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    payload = _api_get(url, token)
    encoded = payload.get("content", "")
    if not encoded:
        raise RuntimeError(f"empty content for path: {path}")
    decoded = base64.b64decode(encoded).decode("utf-8")
    return decoded


def main() -> int:
    try:
        token = _require_env("GITHUB_TOKEN")
        repo = _require_env("GITHUB_REPOSITORY")
        pr_number = _require_env("PR_NUMBER")
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        pr = _fetch_pr(repo, pr_number, token)
    except error.HTTPError as exc:
        print(f"error: failed to fetch PR: {exc}", file=sys.stderr)
        return 1

    body = pr.get("body") or ""
    body_issues = validate_text_content(body)
    for issue in body_issues:
        print(f"PR body violation: {issue}")

    marker_path = find_marker_path(body)
    if not marker_path:
        print("PR body violation: missing marker <!-- PR_BODY_FILE: <path> -->")
        return 1
    if not is_safe_relative_path(marker_path):
        print(f"PR body violation: unsafe marker path: {marker_path}")
        return 1

    head_sha = (pr.get("head") or {}).get("sha", "")
    if not head_sha:
        print("PR body violation: could not resolve PR head sha")
        return 1

    try:
        file_text = _fetch_repo_file(repo, marker_path, head_sha, token)
    except Exception as exc:  # pragma: no cover - network path in CI
        print(f"PR body violation: failed to fetch marker file '{marker_path}': {exc}")
        return 1

    if normalize_text(body).rstrip("\n") != normalize_text(file_text).rstrip("\n"):
        print("PR body violation: body content does not match marker file content")
        return 1

    if body_issues:
        return 1

    print("PR body policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

