import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cleaner import clean_text, clean_text_with_stats


def test_clean_text_with_stats_counts():
    raw = "店长微信：wx1 some text\xa0more 店长微信：wx2 end\xa0"
    cleaned, stats = clean_text_with_stats(raw)

    assert "店长微信" not in cleaned
    assert stats["removed_wechat"] == 2
    assert stats["replaced_nbsp"] == 2
    assert "\xa0" not in cleaned


def test_clean_text_compatibility():
    raw = "店长微信：wx1 hi\xa0"
    assert clean_text(raw) == clean_text_with_stats(raw)[0]


def test_clean_text_verbose_prints(capsys):
    raw = "店长微信：wx1 middle 店长微信：wx2 end\xa0"
    cleaned, stats = clean_text_with_stats(raw, verbose=True)

    captured = capsys.readouterr()
    assert "removed_wechat:" in captured.out
    assert "removed_wechat_values:" in captured.out
    assert "店长微信：wx1" in captured.out
    assert "店长微信：wx2" in captured.out
    assert "replaced_nbsp:" in captured.out
