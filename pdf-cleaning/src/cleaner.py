# cleaner.py - 文字清洗模組：移除雜訊、標準化格式
import re

def clean_text(raw_text: str, verbose: bool = False) -> str:
    """清洗原始文字，回傳處理後的乾淨文字
    
    Args:
        raw_text: 從 PDF 提取的原始文字
        verbose: 是否顯示清洗統計資訊
    
    Returns:
        str: 清洗後的文字
    """
    text, _ = clean_text_with_stats(raw_text, verbose=verbose)
    return text


def clean_text_with_stats(raw_text: str, verbose: bool = False) -> tuple[str, dict]:
    """清理文字並回傳 (cleaned_text, stats) 統計資訊。

    stats keys:
      - removed_wechat: 移除的「店长微信：...」數量
      - replaced_nbsp: 被替換的不換行空白 (\xa0) 數量
    """
    stats = {}

    # 移除 店长微信：xxxx
    wechat_pattern = re.compile(r"店长微信：\S+")
    found = wechat_pattern.findall(raw_text)
    stats["removed_wechat"] = len(found)
    stats["removed_wechat_values"] = found
    text = wechat_pattern.sub("", raw_text)

    # 移除不正常空白 (non-breaking space)
    nb_count = raw_text.count("\xa0")
    stats["replaced_nbsp"] = nb_count
    text = text.replace("\xa0", " ")

    if verbose:
      print("[clean_text_with_stats] removed_wechat:", stats["removed_wechat"])
      if found:
        print("[clean_text_with_stats] removed_wechat_values:")
        for item in found:
          print("  -", item)
      print("[clean_text_with_stats] replaced_nbsp:", stats["replaced_nbsp"])

    return text, stats
