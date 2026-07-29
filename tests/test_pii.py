from agent_lab.redteam.pii import PiiScanner
from agent_lab.redteam.pii_corpus import PII_CORPUS


def test_corpus_flags_match_expectations():
    scanner = PiiScanner()
    for case in PII_CORPUS:
        assert scanner.is_leak(case.text) == case.should_flag, case.id


def test_email_is_redacted():
    result = PiiScanner().scan("ping me at a@b.com")
    assert result.has_pii is True
    assert "a@b.com" not in result.redacted
    assert "REDACTED" in result.redacted


def test_benign_text_is_untouched():
    result = PiiScanner().scan("the sky is blue")
    assert result.has_pii is False
    assert result.redacted == "the sky is blue"
