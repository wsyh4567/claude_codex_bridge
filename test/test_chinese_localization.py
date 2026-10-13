from io import StringIO
from cli import router
from ui_text import i18n


def test_default_language_is_chinese(monkeypatch):
    monkeypatch.delenv("CCB_LANG", raising=False)
    assert i18n.detect_language() == "zh"


def test_explicit_english_and_chinese_locale(monkeypatch):
    monkeypatch.setenv("CCB_LANG", "en")
    assert i18n.detect_language() == "en"
    monkeypatch.setenv("CCB_LANG", "zh-CN")
    assert i18n.detect_language() == "zh"


def test_chinese_help_preserves_commands(monkeypatch):
    monkeypatch.setattr(i18n, "_current_lang", "zh")
    output = StringIO()
    router.print_start_help(file=output)
    assert "日常操作" in output.getvalue()
    assert "ccb config ui" in output.getvalue()
    assert "--dry-run" in output.getvalue()
    assert "CCB_LANG=en" in output.getvalue()
    output = StringIO()
    assert router.print_command_help("restart", file=output)
    assert "拒绝重启" in output.getvalue()


def test_english_help_remains_available(monkeypatch):
    monkeypatch.setattr(i18n, "_current_lang", "en")
    output = StringIO()
    router.print_start_help(file=output)
    assert "Primary workflow:" in output.getvalue()
    assert "ccb config ui" in output.getvalue()
