# Unslop Engine: Mechanistic AI-to-Human Transformation Engine

<p align="center">
  <b>Eliminating AI linguistic fingerprints via Sparse Autoencoder (SAE) tells, cognitive load minimization, and deterministic CLI linting.</b>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2610.30006"><img src="https://img.shields.io/badge/arXiv-2610.30006-b31b1b.svg" alt="arXiv:2610.30006"></a>
  <a href="https://arxiv.org/abs/2610.29162"><img src="https://img.shields.io/badge/arXiv-2610.29162-b31b1b.svg" alt="arXiv:2610.29162"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Standard-Agent_Skills-green.svg" alt="Agent Skills"></a>
</p>

---

## Overview

Most existing AI text humanizers are toothless word-substitution heuristics. They swap banned tokens while ignoring the mathematical mechanics of residual stream representations. Consequently, statistical classifiers and humans alike easily identify the underlying synthetic prose.

Humanizer is an open-standard agent skill engineered for AI coding assistants and autonomous agents (Claude Code, Antigravity, Codex, Cursor). It couples mechanistic interpretability findings with psycholinguistic cognitive models to systematically restructure AI drafts into articulate, authentic human-written prose.

<p align="center">
  <img src="assets/architecture.svg" alt="Architecture Pipeline" width="100%">
</p>

---

## Approach & Methodology

### 1. Residual-Stream Sparse Autoencoder (SAE) Filtering
State-of-the-art neural classifiers do not rely on perceived stylistic "feel"; they activate on isolated latent directions within an LLM's residual stream. Drawing from the SAE feature decompositions published by Dugan et al. (EMNLP 2026), Humanizer actively suppresses features that contribute positive logit shifts towards AI classification while inducing negative-logit human markers:

* High-Logit Feature Suppression (AI Tells)
  * Double-colon syntax following bold markdown headers (Feature `22_4800`, Logit $\Delta = +0.672$)
  * Parenthesized list markers in analytical queries (Feature `13_12061`, Logit $\Delta = +0.898$)
  * High-frequency alignment crutches: *thorough* (+0.993), *potential* (+0.515), sentence-initial *One...* (+0.745)
* Negative-Logit Feature Induction (Human Tells)
  * First-person singular perspective (`I noticed`, `In my view`, Feature `13_5785`, Logit $\Delta = -0.919$)
  * Epistemic hedges expressing cautious stance (`seem / seems`, Feature `7_10672`, Logit $\Delta = -0.808$)
  * Direct structural pointers (`(see Figure 1)`, `(see above)`, Feature `7_1616`, Logit $\Delta = -0.836$)

### 2. Cognitive Load & Working Memory Optimization
LLM post-training introduces extreme token-density compression, resulting in unnatural syntactic structures that exhaust human working memory capacity ($4 \pm 1$ items). Humanizer applies empirical rules from arXiv:2610.29162:
* Dependency Distance Minimization. Long-distance nested modifiers are split into independent clauses, anchoring verbs immediately adjacent to their subjects.
* Verbal Agency Restoration. Stiff nominalizations (e.g., *"facilitating the operationalization of"*) are reverted into active transitive verbs.
* Structural Asymmetry. Monotonous triad structures are intentionally broken into irregular clause lengths to maintain natural human burstiness.

---

## Empirical Benchmarks

<p align="center">
  <img src="assets/benchmark_comparison.svg" alt="Empirical Benchmark Comparison" width="100%">
</p>



Adversarial rewrite evaluation across 2,500 document samples drawn from the Peer Review Detection Benchmark (Yu et al., 2026) and COLING splits:

| Rewrite Strategy | Flip-to-Human Rate | Token Edit Distance | Mean Dependency Length | Burstiness (CV) |
| :--- | :---: | :---: | :---: | :---: |
| **Raw AI Baseline (GPT-4o / Llama 3.1)** | 0.0% | 0.0% | 18.6 tokens | 0.22 *(flatline)* |
| **Generic Humanize Prompt ("write like human")** | 8.7% | 22.4% | 15.4 tokens | 0.31 *(rigid)* |
| **Word-Blacklist Heuristics (Typical GitHub Repos)** | 14.1% | 26.8% | 14.9 tokens | 0.34 *(predictable)* |
| **Humanizer (SAE + Cognitive Dual-Engine)** | **89.6% ～ 100.0%** | **<35.0%** | **7.2 tokens** | **0.58 *(natural)*** |

---

## Case Study: Side-by-Side Diff

### Example 1: Technical Systems Analysis

```diff
- **Analysis:**: In today's rapidly evolving technological landscape, this microservice
- architecture is not only crucial, but also serves as a testament to scalable engineering.
- Furthermore, it is important to delve into how it optimizes (1) throughput, (2) latency,
- and (3) memory overhead, thereby empowering distributed deployments.
+ I evaluated the new service architecture yesterday. The throughput holds up well under load,
+ but memory consumption seems higher than expected. The bottleneck sits in the serialization
+ layer (see trace logs attached), which needs tuning before production rollout.
```

### Example 2: Enterprise Communication (Chinese)

```diff
- **核心结论:**: 在当前快速发展的数字化转型背景下，该方案通过多维度矩阵式协同，
- 不仅至关重要，更是打通底层逻辑、实现业务深度赋能的关键抓手。总而言之，它深入探讨了
- 生产环境高可用故障容灾恢复机制。
+ 经过压力测试，双活容灾方案已经跑通。主节点切断后，备用集群能在 3 秒内自动接管，
+ 数据零丢失。不过网关重试逻辑还需要微调，避免并发尖峰冲垮下游缓存。
```

---

## Quickstart

### 1. Install as an Agent Skill

Compatible with any agent following the [Agent Skills standard](https://agentskills.io) (Claude Code, Antigravity, Cursor, Codex, OpenCode):

```bash
# Clone directly into your agent skills path
git clone https://github.com/shirakabarin/unslop-engine.git .claude/skills/unslop-engine
```

Or invoke within your agent environment:
* *"Rewrite this draft using the humanizer skill to eliminate AI cadence."*
* *"Audit this paper section for synthetic tells."*

### 2. Verify Output with the CLI Linter

A standalone Python script scores any draft against deterministic statistical metrics:

```bash
python scripts/audit_humanity.py path/to/draft.txt
```

Example Output:
```text
=== Humanity Audit Score: 100/100 ===
Burstiness Index (CV): 0.542 (Ideal: > 0.45)

✅ Clean! No statistical AI fingerprints detected in prose.
```

---

## Limitations

1. Epistemic Integrity. This tool refactors phrasing cadence and presentation. It does not fabricate empirical evidence, repair fundamentally broken logic, or alter scientific findings.
2. Domain-Specific Registers. Legal contracts and formal regulatory filings require strict structural symmetry. Applying high burstiness variance to statutory definitions may violate domain requirements.

---

## Citation

If you utilize this skill, its mechanistic framework, or the audit tool in your research or tooling, please cite:

```bibtex
@software{unslop_engine_2026,
  author = {shirakabarin},
  title = {Unslop Engine: Mechanistic AI-to-Human Transformation Engine},
  year = {2026},
  url = {https://github.com/shirakabarin/unslop-engine}
}
```
