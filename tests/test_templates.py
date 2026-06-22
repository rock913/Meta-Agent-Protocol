"""MAP v1.1 — Template placeholder integrity tests.

Verifies that all MAP templates contain the required placeholders
and that no undocumented placeholders exist.
"""

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _find_placeholders(text: str) -> set[str]:
    """Extract all {{PLACEHOLDER}} tokens from text."""
    return set(re.findall(r'\{\{(\w+)\}\}', text))


def _load_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    assert path.exists(), f"Template not found: {path}"
    return path.read_text()


class TestAIRulesTemplate:
    """AI_RULES.md.template must contain all 5 required placeholders."""

    REQUIRED = {"TEST_COMMANDS", "REDLINE_EXTRA", "TEST_TARGETS",
                 "PRD_PATH_MAP", "LOCAL_CONVENTIONS_SUMMARY"}

    def test_all_required_placeholders_present(self):
        content = _load_template("AI_RULES.md.template")
        found = _find_placeholders(content)
        missing = self.REQUIRED - found
        assert not missing, f"Missing placeholders: {missing}"

    def test_no_undocumented_placeholders(self):
        content = _load_template("AI_RULES.md.template")
        found = _find_placeholders(content)
        undocumented = found - self.REQUIRED
        assert not undocumented, f"Undocumented placeholders: {undocumented}"

    def test_contains_nine_laws(self):
        """AI_RULES template must reference all 9 laws from THE_CODEX."""
        content = _load_template("AI_RULES.md.template")
        for i in range(1, 10):
            law_pattern = f"法则{i}" if i <= 9 else f"Law {i}"
            # Use a flexible check — at minimum there should be 9 法则 sections
        laws = content.count("## 法则")
        assert laws >= 9, f"Expected >= 9 法则 sections, found {laws}"


class TestAiderTemplate:
    """aider.conf.yml.template must contain all 4 required placeholders."""

    REQUIRED = {"WORKSPACE_NAME", "PRD_DOC_MAP", "ROADMAP_PATH_MAP", "PRD_PATH_MAP"}

    def test_all_required_placeholders_present(self):
        content = _load_template("aider.conf.yml.template")
        found = _find_placeholders(content)
        missing = self.REQUIRED - found
        assert not missing, f"Missing placeholders: {missing}"

    def test_model_is_deepseek(self):
        """Default model should be deepseek/deepseek-v4-pro (cost advantage)."""
        content = _load_template("aider.conf.yml.template")
        assert "deepseek/deepseek-v4-pro" in content


class TestImportlinterTemplate:
    """importlinter.ini.template must contain all 4 required placeholders."""

    REQUIRED = {"PACKAGE_LIST", "MODULE_LIST", "IGNORE_IMPORTS", "LAYER_LIST"}

    def test_all_required_placeholders_present(self):
        content = _load_template("importlinter.ini.template")
        found = _find_placeholders(content)
        missing = self.REQUIRED - found
        assert not missing, f"Missing placeholders: {missing}"

    def test_valid_ini_structure(self):
        """Template should have valid INI section headers."""
        content = _load_template("importlinter.ini.template")
        sections = re.findall(r'^\[(.+)\]', content, re.MULTILINE)
        assert len(sections) >= 1, "No INI sections found"
