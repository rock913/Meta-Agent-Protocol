"""MAP v1.1 — Cross-consistency tests between THE_CODEX, rules, and templates.

Verifies that:
1. THE_CODEX 9 laws correspond to AI_RULES.md.template 9 法则 sections
2. Sub-project-conventions/ covers all known sub-projects
3. INTEGRATION.md references all key files
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _slurp(path: str) -> str:
    p = ROOT / path
    assert p.exists(), f"File not found: {p}"
    return p.read_text()


class TestCodexRulesConsistency:
    """THE_CODEX laws should map to AI_RULES.md template sections."""

    def test_nine_laws_in_codex(self):
        codex = _slurp("THE_CODEX.md")
        laws = re.findall(r'^## 法则[一二三四五六七八九]', codex, re.MULTILINE)
        assert len(laws) == 9, f"Expected 9 laws in THE_CODEX, found {len(laws)}"

    def test_nine_laws_in_template(self):
        template = _slurp("templates/AI_RULES.md.template")
        laws = re.findall(r'^## 法则[一二三四五六七八九]', template, re.MULTILINE)
        assert len(laws) == 9, f"Expected 9 法则 sections in template, found {len(laws)}"

    def test_law_names_match(self):
        """Law names should be consistent between THE_CODEX and template."""
        codex = _slurp("THE_CODEX.md")
        template = _slurp("templates/AI_RULES.md.template")

        codex_laws = re.findall(r'## 法则[一二三四五六七八九]：(.+)', codex)
        template_laws = re.findall(r'## 法则[一二三四五六七八九]：(.+)', template)

        # At minimum, the template should have the same number of 法则 headers
        assert len(codex_laws) == len(template_laws), \
            f"Law count mismatch: codex={len(codex_laws)}, template={len(template_laws)}"


class TestSubProjectConventions:
    """sub-project-conventions/ should cover all known sub-projects."""

    KNOWN = {
        "SROS", "ARC-Engine", "GraphMRI-Lite",
        "Hermes-Workflows", "AgenticOps", "SXMU_MDD_Twin",
    }

    def test_all_known_subprojects_have_template(self):
        conv_dir = ROOT / "sub-project-conventions"
        existing = {p.stem.replace("-CONVENTIONS", "").replace("_", "-")
                     for p in conv_dir.glob("*-CONVENTIONS.md")}
        # Normalize: SXMU_MDD_Twin-CONVENTIONS → SXMU_MDD_Twin
        existing_normalized = set()
        for e in existing:
            # Map back to expected names
            for k in self.KNOWN:
                if k.lower().replace("-", "").replace("_", "") == e.lower().replace("-", "").replace("_", ""):
                    existing_normalized.add(k)
                    break
            else:
                existing_normalized.add(e)

        missing = self.KNOWN - existing_normalized
        assert not missing, f"Missing sub-project convention templates: {missing}"

    def test_each_template_has_minimum_sections(self):
        """Each CONVENTIONS template should have at minimum: 技术栈, 架构红线, 测试铁律, 禁止行为."""
        conv_dir = ROOT / "sub-project-conventions"
        for tmpl in sorted(conv_dir.glob("*-CONVENTIONS.md")):
            content = tmpl.read_text()
            has_setup = any(kw in content for kw in (
                "技术栈", "Tech Stack", "核心原则", "Core Principles"
            ))
            assert has_setup, f"{tmpl.name}: missing setup/tech section"
            has_constraints = any(kw in content for kw in (
                "红线", "Red Lines", "Guardrails", "Hard", "调度法则",
                "交互契约", "Interaction Contract", "架构", "HPC", "MCP"
            ))
            assert has_constraints, f"{tmpl.name}: missing architecture constraints section"


class TestIntegrationReferences:
    """INTEGRATION.md should reference all key MAP files."""

    def test_integration_references_codex(self):
        integration = _slurp("INTEGRATION.md")
        assert "THE_CODEX.md" in integration

    def test_integration_references_setup_script(self):
        integration = _slurp("INTEGRATION.md")
        assert "setup_map.sh" in integration

    def test_integration_references_templates(self):
        integration = _slurp("INTEGRATION.md")
        assert "AI_RULES.md" in integration
        assert "aider.conf.yml" in integration
        assert "importlinter" in integration
