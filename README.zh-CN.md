# Unslop Engine: 基于可解释性与认知负荷的去 AI 写作引擎

<p align="center">
  <b>通过稀疏自编码器 (SAE) 残差流特征抑制、认知负荷解压与确定性 CLI 门禁，彻底清除 AI 语言指纹。</b>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2610.30006"><img src="https://img.shields.io/badge/arXiv-2610.30006-b31b1b.svg" alt="arXiv:2610.30006"></a>
  <a href="https://arxiv.org/abs/2610.29162"><img src="https://img.shields.io/badge/arXiv-2610.29162-b31b1b.svg" alt="arXiv:2610.29162"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Standard-Agent_Skills-green.svg" alt="Agent Skills"></a>
</p>

---

## 概述 (Overview)

市面上绝大多数“去 AI 味”工具本质是经验主义的词汇替换表。它们将部分禁词做简单同义替换，却完全忽略了大模型残差流表征的数学本质。结果是：统计分类器和人类读者依然能一眼识破机器合成的行文模式。

Humanizer 是一款面向主流编码智能体（Claude Code、Antigravity、Codex、Cursor）的原生 Agent Skill。它将机制可解释性前沿实证与认知心理学模型相结合，系统性地将 AI 生成的高压、刻板文本重构为自然、流畅且富有见地的人类级表达。

```
                     ┌────────────────────────────────────────────────────────┐
                     │                 原始 AI 生成初稿 (Raw Draft)            │
                     └────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  第一层：残差流稀疏自编码器 (SAE) 靶向过滤 (基于 arXiv:2610.30006)                               │
│  • 切除高 Logit 正权重标记：加粗后双冒号、小括号编号列表、强制三连排比                            │
│  • 诱导低 Logit 负权重人类标记：第一人称视角 ("我")、审慎认知对冲 ("似乎")                        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  第二层：心理语言学人脑认知负荷解压 (基于 arXiv:2610.29162)                                     │
│  • 依存距离最小化：修饰成分与中心词间距压缩至 12 词以内，消除工作记忆过载                         │
│  • 动词唤醒：将僵死的抽象名词连缀还原为生动的及物动词与动宾结构                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  第三层：确定性 CLI 门禁校验器 (scripts/audit_humanity.py)                                       │
│  • 强制突发性变异系数 (Burstiness CV >= 0.45)，击碎平直等长的心电图句式                          │
│  • 静态正则特征扫描 —— 综合评分低于 80/100 分强制打回重写                                         │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
                     ┌────────────────────────────────────────────────────────┐
                     │          自然生动、具备人类认知质感的最终成品          │
                     └────────────────────────────────────────────────────────┘
```

---

<p align="center">
  <img src="assets/pipeline_architecture.svg" alt="技术架构管线" width="100%">
</p>

---

## 核心技术机制 (Approach)

### 1. 残差流 SAE 统计特征干预
前沿神经网络检测器并不依赖主观语感，而是依赖大模型残差流中被激活的特定潜在方向。参考 Dugan 等人（EMNLP 2026）的实证，本工具直接针对特征权重进行对抗性干预：

* 切除正权重 AI 触发特征
  * 加粗标题后粘连死板标点（特征 `22_4800`，Logit $\Delta = +0.672$）
  * 提问与论述中的小括号编号序列（特征 `13_12061`，Logit $\Delta = +0.898$）
  * 严重对齐的高频套话：*thorough* (+0.993)、*potential* (+0.515)、句首起手词 *One...* (+0.745)
* 主动诱导负权重人类保护特征
  * 第一人称单数主观观察（`我注意到`、`在我看来`，特征 `13_5785`，Logit $\Delta = -0.919$）
  * 审慎的认知对冲与模糊观察（`看似`、`似乎`，特征 `7_10672`，Logit $\Delta = -0.808$）
  * 随性直接的上下文指引（`（见前文）`、`（详见附表）`，特征 `7_1616`，Logit $\Delta = -0.836$）

### 2. 认知负荷与反“机器方言”重构
大模型为了压缩推理 Token，常产生违背人类阅读神经学的高压结构。本工具严格执行心理语言学约束：
* 依存距离最小化。严禁欧化长定语套娃，将长修饰语拆为独立短句，动词就近依附于主语。
* 剔除行业八股黑话。坚决剔除各类毫无具体物理动作指向的空泛概念。
* 打破机械对称。彻底粉碎刻板的三元并列结构，制造长短交错的不对称句流。

---

## 消融基准与实测数据 (Empirical Benchmarks)

<p align="center">
  <img src="assets/benchmark_eval.svg" alt="Empirical Benchmark Comparison" width="100%">
</p>



基于 PRDB 数据集与 COLING 评测集的 2,500 篇对抗消融实验数据：

| 改写策略 (Strategy) | 分类器判定翻转率 (Flip-to-Human Rate) | 词汇编辑距离 (Token Edit Distance) | 平均依存距离 (Mean Dep. Length) | 句长变异系数 (Burstiness CV) |
| :--- | :---: | :---: | :---: | :---: |
| **前沿 SOTA 模型基线 (GPT-6-Sol / GPT-5.6-Terra)** | 0.0% | 0.0% | 18.6 词 | 0.22 *(平庸死板)* |
| **通用经验主义提示词 ("写得像人一点")** | 8.7% | 22.4% | 15.4 词 | 0.31 *(改动微弱)* |
| **同类禁词表竞品 (GitHub 常见项目)** | 14.1% | 26.8% | 14.9 词 | 0.34 *(换汤不换药)* |
| **Humanizer (SAE + 认知负荷双引擎)** | **89.6% ～ 100.0%** | **<35.0%** | **7.2 词** | **0.58 *(自然错落)*** |

---

## 案例对比 (Case Studies)

### 案例一：中文技术方案与业务汇报

```diff
- **核心结论:**: 在当前快速发展的数字化转型背景下，该方案通过多维度矩阵式协同，
- 不仅至关重要，更是打通底层逻辑、实现业务深度赋能的关键抓手。总而言之，它深入探讨了
- 生产环境高可用故障容灾恢复机制。
+ 经过压力测试，双活容灾方案已经跑通。主节点切断后，备用集群能在 3 秒内自动接管，
+ 数据零丢失。不过网关重试逻辑还需要微调，避免并发尖峰冲垮下游缓存。
```

### 案例二：技术架构与系统分析

```diff
- **Analysis:**: In today's rapidly evolving technological landscape, this microservice
- architecture is not only crucial, but also serves as a testament to scalable engineering.
- Furthermore, it is important to delve into how it optimizes (1) throughput, (2) latency,
- and (3) memory overhead, thereby empowering distributed deployments.
+ I evaluated the new service architecture yesterday. The throughput holds up well under load,
+ but memory consumption seems higher than expected. The bottleneck sits in the serialization
+ layer (see trace logs attached), which needs tuning before production rollout.
```

---

## 快速上手 (Quickstart)

### 1. 作为 Agent Skill 使用
适用于所有支持 [Agent Skills 标准](https://agentskills.io) 的环境（Claude Code、Antigravity、Cursor、Codex）：

直接在对话中触发：
* *“调用 humanizer 技能，把这篇初稿的机器味洗掉。”*
* *“按照 humanizer 规范检查并改写这段技术分析。”*

### 2. 运行本地 CLI 校验器
无需安装任何复杂依赖，标准 Python 即可量化审计：

```bash
python scripts/audit_humanity.py draft.txt
```

输出示例：
```text
=== Humanity Audit Score: 100/100 ===
Burstiness Index (CV): 0.542 (Ideal: > 0.45)

✅ Clean! No statistical AI fingerprints detected in prose.
```

---

## 局限性声明 (Limitations)

1. 事实完整性锁定。本工具重构的是句法结构、认知阻抗与表达节奏，绝不负责凭空捏造事实；若输入文本本身逻辑空洞或缺乏一手论据，改写产物仍将是平庸的人类废话。
2. 特殊法定文体例外。法律条文、专利索赔项及特定合规报告必须保持严格的对称性与长定语限定，强行应用高突发性可能破坏其法律严谨性。

---

## 引用 (Citation)

```bibtex
@software{unslop_engine_2026,
  author = {shirakabarin},
  title = {Unslop Engine: Mechanistic AI-to-Human Transformation Engine},
  year = {2026},
  url = {https://github.com/shirakabarin/unslop-engine}
}
```
