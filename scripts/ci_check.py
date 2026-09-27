#!/usr/bin/env python3
"""Dependency-free repository checks used by the required GitHub Actions job."""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
REFERENCE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
TITLE = re.compile(r"[a-z][a-z0-9-]*(?:\([^)]+\))?!?: \S.*")


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout


def markdown_targets(text):
    fence_char = None
    fence_size = 0
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence_char:
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_size:
                fence_char = None
            continue
        if fence:
            fence_char, fence_size = fence.group(1)[0], len(fence.group(1))
            continue
        for pattern in (LINK, REFERENCE):
            for match in pattern.finditer(line):
                yield match.group(1) or match.group(2)


def sensitive(path):
    name = Path(path).name.lower()
    return (
        name == ".env"
        or name.startswith(".env.")
        or name.endswith((".pem", ".key"))
        or name in {"id_rsa", "id_ed25519"}
    )


def check_markdown_links(root, markdown):
    root = root.resolve()
    for name in markdown:
        source = root / name
        for target in markdown_targets(source.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            try:
                destination.relative_to(root)
            except ValueError:
                raise ValueError(f"{name}: link escapes the repository: {target}")
            if not destination.exists():
                raise ValueError(f"{name}: broken local link: {target}")


def check_diff(base, event):
    if base:
        diff_range = f"{base}...HEAD" if event == "pull_request" else f"{base}..HEAD"
        git("diff", "--check", diff_range)
    else:
        git("diff", "--check")
        git("diff", "--cached", "--check")


def check_repository():
    tracked = git("ls-files", "-z").split("\0")
    offenders = [path for path in tracked if path and sensitive(path)]
    if offenders:
        raise ValueError("sensitive filenames are tracked: " + ", ".join(offenders))

    markdown = [path for path in tracked if path.lower().endswith(".md")]
    check_markdown_links(ROOT, markdown)


def self_test():
    assert TITLE.fullmatch("feat(parser): add strict mode")
    assert TITLE.fullmatch("fix!: reject invalid input")
    assert not TITLE.fullmatch("Add strict mode")
    assert list(markdown_targets("[a](./a.md)\n```md\n[b](missing.md)\n```")) == ["./a.md"]
    assert sensitive("secrets/.env.local")
    assert sensitive("keys/server.pem")
    assert not sensitive("docs/environment.md")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "README.md").write_text("[valid](./target.md)", encoding="utf-8")
        (root / "target.md").touch()
        check_markdown_links(root, ["README.md"])
        (root / "README.md").write_text("[broken](missing.md)", encoding="utf-8")
        try:
            check_markdown_links(root, ["README.md"])
        except ValueError:
            pass
        else:
            raise AssertionError("broken local links must fail")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="diff base ref for local range checking")
    parser.add_argument("--self-test", action="store_true", help="run built-in assertions")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test passed")
        return 0

    try:
        event = os.environ.get("GITHUB_EVENT_NAME", "")
        title = os.environ.get("CI_PR_TITLE", "")
        if event == "pull_request" and not TITLE.fullmatch(title):
            raise ValueError("PR title must follow Conventional Commits syntax")
        check_diff(args.base or os.environ.get("CI_DIFF_BASE", ""), event)
        check_repository()
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        detail = (
            (error.stdout + error.stderr).strip()
            if isinstance(error, subprocess.CalledProcessError)
            else str(error)
        )
        print(detail, file=sys.stderr)
        return 1
    print("CI checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
