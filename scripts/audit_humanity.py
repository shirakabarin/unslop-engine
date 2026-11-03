#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Linter and Metric Scorer for AI-to-Human Text Transformation
Evaluates text against:
1. Sentence length variance (Burstiness / Perplexity proxy)
2. Mechanistic SAE high-logit tokens (DetectorScope arXiv:2610.30006)
3. Cognitive load markers & corporate pseudo-concepts (arXiv:2610.29162)
4. Formulaic AI structures & formatting crutches (Wikipedia Signs of AI writing)

Ignores markdown code blocks (```...```) and inline code (`...`) so documentation
explaining or showcasing bad AI examples does not trigger false positives on itself.
"""

import sys
import re
import statistics

# Banned vocabulary & High-Logit AI tells
BANNED_WORDS_EN = [
    r"\bdelve\b", r"\btapestry\b", r"\bbeacon\b", r"\btestament\b", r"\bcrucial\b",
    r"\bparamount\b", r"\bpivotal\b", r"\bfurthermore\b", r"\bmoreover\b", r"\bin conclusion\b",
    r"\bit is important to note\b", r"\bworth noting\b", r"\bnot only\b.*?\bbut also\b",
    r"\ba testament to\b", r"\bthe realm of\b", r"\blandscape\b", r"\bmultifaceted\b",
    r"\bunderscores\b", r"\bhighlights the need\b", r"\bdeep dive\b", r"\bgame[- ]changer\b"
]

BANNED_WORDS_ZH = [
    r"值得注意的是", r"不可否认的是", r"总而言之", r"综上所述", r"深入探讨", r"潜在影响",
    r"至关重要", r"有力证明", r"如前所述", r"不言而喻", r"由此可见", r"显而易见",
    r"赋能", r"抓手", r"闭环", r"心智穿透", r"打通底层逻辑", r"维度化", r"矩阵式协同",
    r"不仅如此", r"毫无疑问", r"毋庸置疑", r"在当今.*?的背景下", r"在快速发展的今天"
]

# Formatting tells
FORMAT_TELLS = [
    (r"\*\*[^*]+?\*\*[:：]", "Bold header followed by colon/double-colon (**Header:**)"),
    (r"\([0-9]{1,2}\)", "Parenthesized number list (e.g., (1), (2))"),
    (r"—{1,2}", "Em-dash overuse"),
    (r"🚀|💡|🔥|✨|📌|🎯", "Emoji bullet or marketing decoration"),
]

def strip_code(text):
    # Remove fenced code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code blocks
    text = re.sub(r'`[^`\n]+`', '', text)
    return text

def analyze_burstiness(text):
    raw_sentences = re.split(r'[.!?。！？\n]+', text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    
    if len(sentences) < 2:
        return 0.0, [len(s) for s in sentences]
    
    lengths = [len(s) for s in sentences]
    mean_len = statistics.mean(lengths)
    std_dev = statistics.stdev(lengths)
    cv = std_dev / mean_len if mean_len > 0 else 0.0
    return cv, lengths

def audit_text(text):
    prose = strip_code(text)
    issues = []
    
    # 1. Formatting tells
    for pat, desc in FORMAT_TELLS:
        matches = re.findall(pat, prose)
        if matches:
            issues.append(f"[Format Violation] {desc}: found {len(matches)} occurrences")
            
    # 2. Banned English tells
    for pat in BANNED_WORDS_EN:
        matches = re.findall(pat, prose, re.IGNORECASE)
        if matches:
            issues.append(f"[High-Logit AI Tell (EN)] Matched '{pat}': {len(matches)} times")
            
    # 3. Banned Chinese tells
    for pat in BANNED_WORDS_ZH:
        matches = re.findall(pat, prose)
        if matches:
            issues.append(f"[High-Logit AI Tell (ZH)] 发现八股套话/伪概念 '{pat}': {len(matches)} 处")
            
    # 4. Burstiness (Sentence variation)
    cv, lengths = analyze_burstiness(prose)
    
    # 5. Check Triads (A, B, and C)
    triad_en = re.findall(r'\b\w+,\s+\w+,\s+and\s+\w+\b', prose, re.IGNORECASE)
    triad_zh = re.findall(r'[\u4e00-\u9fa5]{2,6}、[\u4e00-\u9fa5]{2,6}以及[\u4e00-\u9fa5]{2,6}', prose)
    if triad_en or triad_zh:
        issues.append(f"[Symmetry Violation] Forced triad (三元机械排比): {len(triad_en) + len(triad_zh)} occurrences")
        
    score = 100
    score -= len(issues) * 12
    if cv < 0.35 and len(lengths) >= 3:
        score -= 20
        issues.append(f"[Rhythm Monotony] Low burstiness index (CV={cv:.2f} < 0.35). Sentences are too uniform.")
    elif cv >= 0.50:
        score += 5
        
    score = max(0, min(100, score))
    return score, cv, issues

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()
        
    score, cv, issues = audit_text(content)
    print(f"=== Humanity Audit Score: {score}/100 ===")
    print(f"Burstiness Index (CV): {cv:.3f} (Ideal: > 0.45)")
    if issues:
        print("\nFlagged Tells & Violations:")
        for iss in issues:
            print(f"  ❌ {iss}")
    else:
        print("\n✅ Clean! No statistical AI fingerprints detected in prose.")
    sys.exit(0 if score >= 80 else 1)
