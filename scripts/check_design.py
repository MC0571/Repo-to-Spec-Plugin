#!/usr/bin/env python3
"""检查本仓库设计登记表与文档的一致性；不验证产品规格的语义充分性。"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from ci_check import check_markdown_links

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "docs/planning/design-baseline.json"
ID = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*")
CONTRACT = re.compile(r"^\|\s*([DWPQ]-\d{2})\s*\|", re.MULTILINE)
STATUS_RULES = {
    "design_status": ({"proposed", "accepted", "superseded"}, "accepted", "approval"),
    "implementation_status": ({"not_implemented", "partial", "implemented"}, "implemented", "implementation"),
    "verification_status": ({"not_run", "partial", "passed", "failed"}, "passed", "verification"),
    "regression_status": ({"not_established", "partial", "protected"}, "protected", "regression"),
}
EVIDENCE_KINDS = {"approval", "implementation", "verification", "regression"}


class DesignError(ValueError):
    """可向贡献者直接报告的登记错误。"""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DesignError(message)


def text(value, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: 必须为非空字符串")
    return value


def safe_file(root: Path, value, label: str) -> Path:
    name = text(value, label)
    parsed = PurePosixPath(name)
    require(not parsed.is_absolute() and ".." not in parsed.parts and "\\" not in name
            and ":" not in name, f"{label}: 必须使用仓库内相对路径")
    resolved = (root / name).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise DesignError(f"{label}: 解析后的路径越界") from error
    require(resolved.is_file(), f"{label}: 文件不存在或不是普通文件：{name}")
    return resolved


def records(data: dict, key: str) -> dict:
    items = data.get(key)
    require(isinstance(items, list), f"{key}: 必须为数组")
    result = {}
    for item in items:
        require(isinstance(item, dict), f"{key}: 每项必须为对象")
        identity = text(item.get("id"), f"{key}.id")
        require(bool(ID.fullmatch(identity)), f"{key}: 无效 ID {identity}")
        require(identity not in result, f"{key}: 重复 ID {identity}")
        text(item.get("name"), f"{identity}.name")
        result[identity] = item
    return result


def refs(value, allowed, label: str, nonempty: bool = False) -> list:
    require(isinstance(value, list), f"{label}: 必须为数组")
    require(all(isinstance(item, str) for item in value), f"{label}: 引用必须为字符串")
    require(len(value) == len(set(value)), f"{label}: 存在重复引用")
    require(not nonempty or bool(value), f"{label}: 不得为空")
    missing = set(value) - set(allowed)
    require(not missing, f"{label}: 悬空引用 {sorted(missing)}")
    return value


def acyclic(graph: dict, label: str) -> None:
    active, visited = [], set()

    def visit(node: str) -> None:
        if node in active:
            start = active.index(node)
            raise DesignError(f"{label}: 依赖环 {' → '.join(active[start:] + [node])}")
        if node in visited:
            return
        active.append(node)
        for dependency in graph[node]:
            visit(dependency)
        active.pop()
        visited.add(node)

    for node in graph:
        visit(node)


def evidence_kinds(item: dict, root: Path, label: str) -> set:
    evidence = item.get("evidence", [])
    require(isinstance(evidence, list), f"{label}.evidence: 必须为数组")
    kinds = set()
    for record in evidence:
        require(isinstance(record, dict), f"{label}: 证据须为对象")
        kind = record.get("kind")
        require(isinstance(kind, str) and kind in EVIDENCE_KINDS, f"{label}: 未知证据种类")
        safe_file(root, record.get("path"), f"{label}.evidence.path")
        kinds.add(kind)
    return kinds


def validate_registry(data: dict, root: Path, known_contracts: set) -> dict:
    require(isinstance(data, dict), "登记表根必须为对象")
    require(type(data.get("registry_version")) is int and data["registry_version"] == 1, "不支持的登记表版本")
    require(bool(re.fullmatch(r"DB-\d{8}", text(data.get("baseline_id"), "baseline_id"))), "基线身份无效")
    require(data.get("status") in {"proposed", "accepted", "superseded"}, "基线状态无效")
    source = data.get("source")
    require(isinstance(source, dict), "source 必须为对象")
    for field in ("commit", "tree"):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", text(source.get(field), f"source.{field}"))), f"source.{field}: SHA 无效")
    root_evidence = evidence_kinds(data, root, "baseline")
    if data["status"] == "accepted":
        require("approval" in root_evidence, "已采纳基线缺少批准记录")

    areas = records(data, "areas")
    capabilities = records(data, "capabilities")
    milestones = records(data, "milestones")
    checks = records(data, "acceptance_checks")
    suites = records(data, "evaluation_suites")
    require(all((areas, capabilities, milestones, checks, suites)), "核心登记集合不得为空")
    for sid, suite in suites.items():
        require(suite.get("status") in {"planned", "implemented", "validated"}, f"{sid}: 集合状态无效")
        safe_file(root, suite.get("definition"), f"{sid}.definition")
        kinds = evidence_kinds(suite, root, sid)
        if suite["status"] in {"implemented", "validated"}:
            require("implementation" in kinds, f"{sid}: 集合实现缺少证据")
        if suite["status"] == "validated":
            require("verification" in kinds, f"{sid}: 集合验证缺少证据")
    for aid, check in checks.items():
        require(check.get("status") in {"not_run", "partial", "passed", "failed"}, f"{aid}: 验收状态无效")
        require(check.get("suite") in suites, f"{aid}: 未知评测集")
        text(check.get("method"), f"{aid}.method")
        text(check.get("pass_criterion"), f"{aid}.pass_criterion")
        kinds = evidence_kinds(check, root, aid)
        if check["status"] != "not_run":
            require("verification" in kinds, f"{aid}: 已执行状态缺少验证记录")

    graph = {}
    for cid, capability in capabilities.items():
        require(capability.get("area") in areas, f"{cid}: 未知职责区")
        require(capability.get("target_milestone") in milestones, f"{cid}: 未知目标里程碑")
        safe_file(root, capability.get("definition"), f"{cid}.definition")
        sections = capability.get("vision_sections")
        require(isinstance(sections, list) and bool(sections)
                and all(isinstance(v, str) and re.fullmatch(r"\d+(?:\.\d+)?", v) for v in sections), f"{cid}: 愿景章节引用无效")
        graph[cid] = refs(capability.get("depends_on"), capabilities, f"{cid}.depends_on")
        refs(capability.get("acceptance_ids"), checks, f"{cid}.acceptance_ids", True)
        refs(capability.get("contract_ids"), known_contracts, f"{cid}.contract_ids", True)
        kinds = evidence_kinds(capability, root, cid)
        for field, (allowed, mature, proof_kind) in STATUS_RULES.items():
            status = capability.get(field)
            require(isinstance(status, str) and status in allowed, f"{cid}.{field}: 状态无效")
            if status == mature or status == "partial" or (field == "verification_status" and status == "failed"):
                require(proof_kind in kinds, f"{cid}.{field}: 缺少 {proof_kind} 证据")
        if capability["verification_status"] == "passed":
            require(capability["implementation_status"] == "implemented", f"{cid}: 未完整实现的能力不能宣称整体验证通过")
            require(all(checks[a]["status"] == "passed" for a in capability["acceptance_ids"]), f"{cid}: 验收尚未全部通过")
        if capability["regression_status"] == "protected":
            require(capability["verification_status"] == "passed", f"{cid}: 未验证能力不能宣称完整回归保护")
    acyclic(graph, "能力")

    milestone_graph = {}
    for mid, milestone in milestones.items():
        milestone_graph[mid] = refs(milestone.get("depends_on"), milestones, f"{mid}.depends_on")
        actual_caps = refs(milestone.get("capability_ids"), capabilities, f"{mid}.capability_ids")
        expected_caps = {c for c, item in capabilities.items() if item["target_milestone"] == mid}
        require(set(actual_caps) == expected_caps, f"{mid}: 目标能力归属不一致")
        actual_checks = refs(milestone.get("exit_check_ids"), checks, f"{mid}.exit_check_ids")
        expected_checks = {a for c in expected_caps for a in capabilities[c]["acceptance_ids"]}
        require(set(actual_checks) == expected_checks, f"{mid}: 出口验收与目标能力不一致")
        require(milestone.get("status") in {"planned", "in_progress", "completed"}, f"{mid}: 里程碑状态无效")
        kinds = evidence_kinds(milestone, root, mid)
        if milestone["status"] == "completed":
            require("approval" in kinds, f"{mid}: 完成缺少批准记录")
            require(all(milestones[d]["status"] == "completed" for d in milestone["depends_on"]), f"{mid}: 前置里程碑未完成")
            require(all(checks[a]["status"] == "passed" for a in actual_checks), f"{mid}: 出口验收尚未通过")
            for cid in actual_caps:
                for field, (_, mature, _) in STATUS_RULES.items():
                    require(capabilities[cid][field] == mature, f"{mid}: {cid} 的 {field} 尚未满足退出条件")
    acyclic(milestone_graph, "里程碑")

    def ancestors(mid: str) -> set:
        result = set(milestone_graph[mid])
        for dependency in milestone_graph[mid]:
            result.update(ancestors(dependency))
        return result

    for cid, capability in capabilities.items():
        stage = capability["target_milestone"]
        allowed_stages = ancestors(stage) | {stage}
        for dependency in capability["depends_on"]:
            require(capabilities[dependency]["target_milestone"] in allowed_stages,
                    f"{cid}: 依赖 {dependency} 的目标阶段不在当前阶段的退出前置中")
    return {"capabilities": len(capabilities), "milestones": len(milestones),
            "acceptance_checks": len(checks), "evaluation_suites": len(suites)}


def check_capability_map(data: dict, root: Path) -> None:
    """导航表不维护独立状态，但其静态索引也不得与登记表漂移。"""
    content = safe_file(root, "docs/planning/CAPABILITY-MAP.md", "能力地图").read_text(encoding="utf-8")
    found = {}
    for line in content.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 8 and re.fullmatch(r"C\d+", parts[1]):
            require(parts[1] not in found, "能力地图存在重复能力")
            found[parts[1]] = parts[2:7]
    expected = {}
    for cap in data["capabilities"]:
        expected[cap["id"]] = [cap["name"], cap["area"], cap["target_milestone"],
                              f'[定义](../../{cap["definition"]})', ", ".join(cap["acceptance_ids"])]
    require(found == expected, "能力地图导航与登记表不一致，请同步导航内容")


def check_all(root: Path) -> dict:
    data = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    ids = []
    for path in sorted((root / "contracts").glob("*.md")):
        ids.extend(CONTRACT.findall(path.read_text(encoding="utf-8")))
    require(len(ids) == len(set(ids)), "契约 ID 重复")
    result = validate_registry(data, root, set(ids))
    check_capability_map(data, root)
    markdown = [str(p.relative_to(root)) for p in root.rglob("*.md")
                if not any(part in {".git", ".venv", "node_modules", "__pycache__"} for part in p.relative_to(root).parts)]
    check_markdown_links(root, markdown)
    result.update(markdown_files=len(markdown), contract_ids=len(ids))
    return result


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "model.md").write_text("# 模型\n", encoding="utf-8")
        (self.root / "proof.md").write_text("# 测试证据占位，仅验证引用结构\n", encoding="utf-8")
        self.data = {
            "registry_version": 1, "baseline_id": "DB-20260928", "status": "proposed",
            "source": {"commit": "a" * 40, "tree": "b" * 40},
            "areas": [{"id": "S1", "name": "区域"}],
            "evaluation_suites": [{"id": "B-TEST", "name": "测试", "status": "planned", "definition": "model.md"}],
            "acceptance_checks": [{"id": "A01", "name": "验收", "suite": "B-TEST", "method": "对照", "pass_criterion": "符合", "status": "not_run", "evidence": []}],
            "capabilities": [{"id": "C01", "name": "能力", "area": "S1", "definition": "model.md", "vision_sections": ["3"], "depends_on": [], "target_milestone": "M1", "acceptance_ids": ["A01"], "contract_ids": ["D-01"], "design_status": "proposed", "implementation_status": "not_implemented", "verification_status": "not_run", "regression_status": "not_established", "evidence": []}],
            "milestones": [{"id": "M1", "name": "阶段", "depends_on": [], "capability_ids": ["C01"], "exit_check_ids": ["A01"], "status": "planned", "evidence": []}],
        }

    def tearDown(self):
        self.directory.cleanup()

    def validate(self):
        return validate_registry(self.data, self.root, {"D-01"})

    def reject(self):
        with self.assertRaises(DesignError):
            self.validate()

    def test_valid(self):
        self.assertEqual(self.validate()["capabilities"], 1)

    def test_duplicate_id(self):
        self.data["capabilities"].append(copy.deepcopy(self.data["capabilities"][0])); self.reject()

    def test_unknown_dependency(self):
        self.data["capabilities"][0]["depends_on"] = ["C99"]; self.reject()

    def test_dependency_cycle(self):
        with self.assertRaises(DesignError):
            acyclic({"C01": ["C02"], "C02": ["C01"]}, "测试")

    def test_self_dependency(self):
        self.data["capabilities"][0]["depends_on"] = ["C01"]; self.reject()

    def test_missing_definition(self):
        self.data["capabilities"][0]["definition"] = "missing.md"; self.reject()

    def test_path_traversal(self):
        self.data["capabilities"][0]["definition"] = "../outside.md"; self.reject()

    def test_windows_style_path(self):
        self.data["capabilities"][0]["definition"] = "C:\\outside.md"; self.reject()

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outer:
            outside = Path(outer) / "outside.md"; outside.write_text("x", encoding="utf-8")
            try:
                (self.root / "escape.md").symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("当前环境不支持创建符号链接")
            self.data["capabilities"][0]["definition"] = "escape.md"; self.reject()

    def test_unknown_status(self):
        self.data["capabilities"][0]["design_status"] = "done"; self.reject()

    def test_accepted_without_record(self):
        self.data["capabilities"][0]["design_status"] = "accepted"; self.reject()

    def test_passed_without_record(self):
        self.data["capabilities"][0]["verification_status"] = "passed"; self.reject()

    def test_unknown_contract(self):
        self.data["capabilities"][0]["contract_ids"] = ["D-99"]; self.reject()

    def test_unknown_acceptance(self):
        self.data["capabilities"][0]["acceptance_ids"] = ["A99"]; self.reject()

    def test_unknown_suite(self):
        self.data["acceptance_checks"][0]["suite"] = "B-MISSING"; self.reject()

    def test_duplicate_reference(self):
        self.data["capabilities"][0]["acceptance_ids"] = ["A01", "A01"]; self.reject()

    def test_milestone_mismatch(self):
        self.data["milestones"][0]["capability_ids"] = []; self.reject()

    def test_premature_milestone(self):
        self.data["milestones"][0]["status"] = "completed"; self.reject()

    def test_executed_check_without_evidence(self):
        self.data["acceptance_checks"][0]["status"] = "failed"; self.reject()

    def test_non_array_references(self):
        self.data["capabilities"][0]["depends_on"] = "C01"; self.reject()

    def test_missing_evidence_file(self):
        self.data["capabilities"][0]["evidence"] = [{"kind": "approval", "path": "missing.md"}]; self.reject()

    def test_mature_states_with_structural_evidence(self):
        cap = self.data["capabilities"][0]
        cap["evidence"] = [{"kind": k, "path": "proof.md"} for k in EVIDENCE_KINDS]
        for field, (_, mature, _) in STATUS_RULES.items():
            cap[field] = mature
        self.data["acceptance_checks"][0].update(status="passed", evidence=[{"kind": "verification", "path": "proof.md"}])
        self.assertEqual(self.validate()["capabilities"], 1)

    def test_empty_collections(self):
        self.data["capabilities"] = []; self.reject()

    def test_cross_stage_dependency(self):
        later = copy.deepcopy(self.data["capabilities"][0])
        later.update(id="C02", target_milestone="M2", depends_on=[])
        self.data["capabilities"].append(later)
        self.data["capabilities"][0]["depends_on"] = ["C02"]
        self.data["milestones"].append({"id": "M2", "name": "后置阶段", "depends_on": ["M1"],
                                        "capability_ids": ["C02"], "exit_check_ids": ["A01"],
                                        "status": "planned", "evidence": []})
        self.reject()

    def test_boolean_version(self):
        self.data["registry_version"] = True; self.reject()

    def test_dag(self):
        acyclic({"C01": [], "C02": ["C01"], "C03": ["C01", "C02"]}, "测试")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="运行登记表检查器的正负向自检")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(RegistryTests)
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    try:
        result = check_all(ROOT)
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(f"设计检查失败：{error}", file=sys.stderr)
        return 1
    print("设计登记与文档结构检查通过：" + json.dumps(result, ensure_ascii=False))
    print("此结果不代表产品功能实现、语义完整性或独立重建验证已通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
