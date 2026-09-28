#!/usr/bin/env python3
"""Check plugin metadata, its single Skill entry, local links, and marketplace entry."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from ci_check import markdown_targets

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins" / "repo-to-spec"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_frontmatter(content: str) -> dict[str, str]:
    lines = content.splitlines()
    require(bool(lines) and lines[0] == "---", "SKILL.md 必须以 YAML frontmatter 开始")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md 缺少 frontmatter 结束标记") from error

    metadata = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        require(bool(separator and key.strip() and value.strip()), "SKILL.md frontmatter 行格式无效")
        key, value = key.strip(), value.strip()
        require(key not in metadata, f"SKILL.md frontmatter 字段重复：{key}")
        metadata[key] = value
    for key in ("name", "description"):
        require(bool(metadata.get(key)), f"SKILL.md frontmatter 缺少 {key}")
    require(bool(SKILL_NAME.fullmatch(metadata["name"])), "SKILL.md 的 name 格式无效")
    return metadata


def check_package_links(package: Path) -> int:
    package = package.resolve()
    markdown = sorted(package.rglob("*.md"))
    for source in markdown:
        for target in markdown_targets(source.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            try:
                destination.relative_to(package)
            except ValueError as error:
                raise ValueError(f"{source.relative_to(package)}: 包内链接越界：{target}") from error
            require(destination.exists(), f"{source.relative_to(package)}: 本地链接不存在：{target}")
    return len(markdown)


def check_marketplace(path: Path, package: Path) -> None:
    require(path.is_file(), "缺少本地 marketplace.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict) and isinstance(data.get("plugins"), list), "marketplace.json 格式无效")
    require(isinstance(data.get("name"), str) and bool(data["name"].strip()), "marketplace name 缺失")
    interface = data.get("interface")
    require(isinstance(interface, dict) and bool(interface.get("displayName")), "marketplace displayName 缺失")
    entries = [item for item in data["plugins"] if isinstance(item, dict) and item.get("name") == package.name]
    require(len(entries) == 1, "marketplace.json 必须恰好注册一次该插件")
    source = entries[0].get("source")
    require(isinstance(source, dict) and source.get("source") == "local", "插件 marketplace 来源必须为 local")
    location = source.get("path")
    require(isinstance(location, str) and location.startswith("./"), "marketplace 插件路径必须以 ./ 开始")
    policy = entries[0].get("policy")
    require(isinstance(policy, dict) and policy.get("installation") and policy.get("authentication"),
            "marketplace installation/authentication 策略缺失")
    require(bool(entries[0].get("category")), "marketplace 插件类别缺失")
    root = path.parent.parent.parent
    resolved = (root / location).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("marketplace 插件路径越过仓库根目录") from error
    require(resolved == package.resolve(), "marketplace 插件路径与本地插件目录不一致")


def check_package(package: Path, marketplace: Path | None = None) -> dict[str, int]:
    manifest_path = package / "plugin.json"
    require(manifest_path.is_file(), "缺少 plugin.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(manifest, dict), "plugin.json 根必须为对象")
    for key in ("$schema", "name"):
        require(isinstance(manifest.get(key), str) and bool(manifest[key].strip()), f"plugin.json 缺少 {key}")
    require(manifest["$schema"] == PLUGIN_SCHEMA, "plugin.json 必须声明 Agent Plugins 1.0.0 schema")
    require(bool(SKILL_NAME.fullmatch(manifest["name"])), "plugin.json name 必须为 kebab-case")
    require(manifest["name"] == package.name, "plugin.json name 必须与插件目录名一致")

    skills = sorted((package / "skills").glob("*/SKILL.md"))
    all_skills = sorted((package / "skills").rglob("SKILL.md"))
    require(len(skills) == len(all_skills) == 1,
            "必须有且只有一个位于 skills/<name>/SKILL.md 的可发现入口")
    skill = skills[0]
    metadata = parse_frontmatter(skill.read_text(encoding="utf-8"))
    require(metadata["name"] == skill.parent.name, "Skill frontmatter name 必须与目录名一致")
    markdown_files = check_package_links(package)
    if marketplace is not None:
        check_marketplace(marketplace, package)
    return {"skills": len(skills), "markdown_files": markdown_files}


def self_test() -> None:
    valid = "---\nname: demo\ndescription: A sample skill\n---\n# Sample\n"
    assert parse_frontmatter(valid) == {"name": "demo", "description": "A sample skill"}
    for invalid in ("# No frontmatter", "---\nname: sample\n", "---\nname: sample\n---\n"):
        try:
            parse_frontmatter(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid frontmatter must fail")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        package = root / "plugins" / "demo"
        skill_dir = package / "skills" / "demo"
        skill_dir.mkdir(parents=True)
        (package / "plugin.json").write_text(
            json.dumps({"$schema": PLUGIN_SCHEMA, "name": "demo"}), encoding="utf-8"
        )
        (skill_dir / "SKILL.md").write_text(valid + "[ref](../../reference.md)\n", encoding="utf-8")
        (package / "reference.md").write_text("# Reference\n", encoding="utf-8")
        marketplace = root / ".agents" / "plugins" / "marketplace.json"
        marketplace.parent.mkdir(parents=True)
        marketplace.write_text(json.dumps({"plugins": [{
            "name": "demo", "source": {"source": "local", "path": "./plugins/demo"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity"
        }], "name": "demo-local", "interface": {"displayName": "Demo"}}), encoding="utf-8")
        assert check_package(package, marketplace)["skills"] == 1
        (package / "plugin.json").write_text(
            json.dumps({"$schema": "schema.json", "name": "demo"}), encoding="utf-8"
        )
        try:
            check_package(package, marketplace)
        except ValueError:
            pass
        else:
            raise AssertionError("unsupported plugin schema must fail")
        (package / "plugin.json").write_text(
            json.dumps({"$schema": PLUGIN_SCHEMA, "name": "Bad Name"}), encoding="utf-8"
        )
        try:
            check_package(package, marketplace)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid plugin names must fail")
        (package / "plugin.json").write_text(
            json.dumps({"$schema": PLUGIN_SCHEMA, "name": "demo"}), encoding="utf-8"
        )
        (package / "skills" / "extra").mkdir()
        (package / "skills" / "extra" / "SKILL.md").write_text(valid.replace("demo", "extra"), encoding="utf-8")
        try:
            check_package(package, marketplace)
        except ValueError:
            pass
        else:
            raise AssertionError("multiple skill entry points must fail")
        (package / "skills" / "extra" / "SKILL.md").unlink()
        nested = package / "skills" / "nested" / "hidden" / "SKILL.md"
        nested.parent.mkdir(parents=True)
        nested.write_text(valid, encoding="utf-8")
        try:
            check_package(package, marketplace)
        except ValueError:
            pass
        else:
            raise AssertionError("undiscoverable nested skill must fail")
        nested.unlink()
        (skill_dir / "SKILL.md").write_text(valid + "[outside](../../../outside.md)\n", encoding="utf-8")
        try:
            check_package(package, marketplace)
        except ValueError:
            pass
        else:
            raise AssertionError("package links escaping the package must fail")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run built-in assertions")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("self-test passed")
        else:
            result = check_package(PACKAGE, MARKETPLACE)
            print(f"plugin package passed: {result['skills']} Skill, {result['markdown_files']} Markdown files")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
