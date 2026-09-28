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

import yaml
from jsonschema import Draft202012Validator

from ci_check import markdown_targets

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins" / "repo-to-spec"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SCHEMA_FILE = Path(__file__).parent / "schemas" / "plugin-1.0.0.json"


class StrictLoader(yaml.SafeLoader):
    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict:
        seen = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                continue
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("SKILL.md frontmatter 字段名必须为文本")
            if key in seen:
                raise ValueError(f"SKILL.md frontmatter 字段重复：{key}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_frontmatter(content: str) -> dict[str, object]:
    lines = content.splitlines()
    require(bool(lines) and lines[0] == "---", "SKILL.md 必须以 YAML frontmatter 开始")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md 缺少 frontmatter 结束标记") from error

    try:
        metadata = yaml.load("\n".join(lines[1:end]) + "\n", Loader=StrictLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"SKILL.md frontmatter YAML 无效：{error}") from error
    require(isinstance(metadata, dict), "SKILL.md frontmatter 必须为对象")
    for key in ("name", "description"):
        value = metadata.get(key)
        require(isinstance(value, str) and bool(value.strip()), f"SKILL.md {key} 必须为非空文本")
    require(len(metadata["name"]) <= 64 and bool(SKILL_NAME.fullmatch(metadata["name"])),
            "SKILL.md 的 name 格式或长度无效")
    require(len(metadata["description"]) <= 1024, "SKILL.md description 超过 1024 字符")
    if "compatibility" in metadata:
        value = metadata["compatibility"]
        require(isinstance(value, str) and 1 <= len(value) <= 500,
                "SKILL.md compatibility 必须是 1–500 字符文本")
    if "metadata" in metadata:
        value = metadata["metadata"]
        require(isinstance(value, dict) and all(isinstance(key, str) and isinstance(item, str)
                                                for key, item in value.items()),
                "SKILL.md metadata 必须是文本到文本的映射")
    if "allowed-tools" in metadata:
        require(isinstance(metadata["allowed-tools"], str), "SKILL.md allowed-tools 必须是文本")
    return metadata


def require_inside(package: Path, path: Path) -> Path:
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(package)
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError(f"插件包路径不存在或越界：{path}") from error
    return resolved


def check_package_links(package: Path) -> int:
    markdown = sorted(package.rglob("*.md"))
    for source in markdown:
        require_inside(package, source)
        for target in markdown_targets(source.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = source.parent / unquote(parsed.path) if parsed.path else source
            try:
                require_inside(package, destination)
            except ValueError as error:
                raise ValueError(f"{source.relative_to(package)}: 本地链接不存在或越界：{target}") from error
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
    require(package.is_dir(), "插件目录不存在")
    package = package.resolve(strict=True)
    for item in package.rglob("*"):
        require_inside(package, item)
    manifest_path = package / "plugin.json"
    require_inside(package, manifest_path)
    require(manifest_path.is_file(), "缺少 plugin.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    require(not errors, f"plugin.json 不符合 Agent Plugins 1.0.0 schema：{errors[0].message}" if errors else "")
    require(bool(SKILL_NAME.fullmatch(manifest["name"])), "plugin.json name 必须为 kebab-case")
    require(manifest["name"] == package.name, "plugin.json name 必须与插件目录名一致")

    skills = sorted((package / "skills").glob("*/SKILL.md"))
    all_skills = sorted((package / "skills").rglob("SKILL.md"))
    require(len(skills) == len(all_skills) == 1,
            "必须有且只有一个位于 skills/<name>/SKILL.md 的可发现入口")
    skill = skills[0]
    require_inside(package, skill)
    metadata = parse_frontmatter(skill.read_text(encoding="utf-8"))
    require(metadata["name"] == skill.parent.name, "Skill frontmatter name 必须与目录名一致")
    markdown_files = check_package_links(package)
    if marketplace is not None:
        check_marketplace(marketplace, package)
    return {"skills": len(skills), "markdown_files": markdown_files}


def self_test() -> None:
    def reject(operation, reason: str) -> None:
        try:
            operation()
        except ValueError:
            return
        raise AssertionError(reason)

    valid = "---\nname: demo\ndescription: A sample skill\n---\n# Sample\n"
    assert parse_frontmatter(valid) == {"name": "demo", "description": "A sample skill"}
    assert parse_frontmatter('---\nname: "demo"\ndescription: |\n  First line\n  Second line\n---\n')["description"] == "First line\nSecond line\n"
    assert parse_frontmatter('---\nbase: &base {description: sample}\n<<: *base\nname: demo\n---\n')["description"] == "sample"
    for invalid in ("# No frontmatter", "---\nname: sample\n", "---\nname: sample\n---\n",
                    "---\nname: demo\ndescription: []\n---\n",
                    '---\nname: demo\ndescription: ""\n---\n',
                    "---\nname: demo\ndescription: [\n---\n",
                    "---\nname: demo\ndescription: text\ncompatibility: []\n---\n",
                    "---\nname: demo\ndescription: text\nmetadata: []\n---\n",
                    "---\nname: demo\ndescription: text\nmetadata: {version: 1}\n---\n",
                    "---\nname: demo\ndescription: text\nallowed-tools: []\n---\n",
                    "---\nname: demo\nname: demo\ndescription: text\n---\n"):
        reject(lambda: parse_frontmatter(invalid), "invalid frontmatter must fail")

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
        manifest = package / "plugin.json"
        for field, value in (("$schema", "schema.json"), ("name", "Bad Name"),
                             ("version", 123), ("description", [])):
            data = {"$schema": PLUGIN_SCHEMA, "name": "demo", field: value}
            manifest.write_text(json.dumps(data), encoding="utf-8")
            reject(lambda: check_package(package, marketplace), f"invalid manifest {field} must fail")
        manifest.write_text(json.dumps({"$schema": PLUGIN_SCHEMA, "name": "demo"}), encoding="utf-8")
        skill = skill_dir / "SKILL.md"
        skill.write_text('---\nname: "demo"\ndescription: |\n  Sample skill\n---\n[ref](../../reference.md)\n', encoding="utf-8")
        assert check_package(package, marketplace)["skills"] == 1
        skill.write_text(valid + "[ref](../../reference.md)\n", encoding="utf-8")
        (package / "skills" / "extra").mkdir()
        (package / "skills" / "extra" / "SKILL.md").write_text(valid.replace("demo", "extra"), encoding="utf-8")
        reject(lambda: check_package(package, marketplace), "multiple skill entry points must fail")
        (package / "skills" / "extra" / "SKILL.md").unlink()
        nested = package / "skills" / "nested" / "hidden" / "SKILL.md"
        nested.parent.mkdir(parents=True)
        nested.write_text(valid, encoding="utf-8")
        reject(lambda: check_package(package, marketplace), "undiscoverable nested skill must fail")
        nested.unlink()
        skill.write_text(valid + "[outside](../../../outside.md)\n", encoding="utf-8")
        reject(lambda: check_package(package, marketplace), "package links escaping the package must fail")
        skill.write_text(valid, encoding="utf-8")
        outside = root / "outside.md"
        outside.write_text(valid, encoding="utf-8")
        for target in (manifest, skill, package / "reference.md"):
            original = target.read_bytes()
            target.unlink()
            target.symlink_to(outside)
            reject(lambda: check_package(package, marketplace), f"symlink escaping package must fail: {target}")
            target.unlink()
            target.write_bytes(original)


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
