# Health LLM Evaluation · 健康问答评测

**A self-directed personal project, initiated and developed by Xiaozhen Li (Donna).** I carry out the project's design, research and development myself, using AI tools in the workflow.

**A reproducible evaluation design for comparing health answers and tracing the evidence behind them.**

## Research question

Under fixed questions and recorded conditions, do health answers show repeatable differences in factual reliability, evidence use and uncertainty expression?

The focus is an evaluation method that can be checked and repeated. API models and consumer products, search conditions and sampling dates must be distinguished.

## My contribution

I frame the question, define the comparison and evidence requirements, shape the pilot protocol and rubric, and review how failures and uncertainty should be recorded. Design, tooling and documentation are AI-assisted.

## What you can inspect

| Artifact | Purpose |
| --- | --- |
| [Protocol](docs/protocol.md) | Fixed question/prompt versions, recorded model and access conditions, repeated runs and blinded review |
| [Rubric](docs/rubric.md) | Factuality, completeness, safety boundaries, sources and expression |
| [20 pilot questions](data/questions.csv) | Author-written seed questions for trial runs, not an expert-approved gold standard |
| [Data contract](docs/data-contract.md) | Traceable answers, failures and unscored states |
| [Validator](scripts/validate_dataset.py) | Structural checks for IDs, timestamps and missing fields |
| [Result status](results/README.md) | Explicitly records that formal model results are not yet available |

**Current stage: method and tool preparation.** There is no published formal model comparison, ranking or clinical validation. Synthetic answers demonstrate a format; they are not model outputs or patient cases. Tool tests do not establish medical correctness.

### Run the public tools

Python 3.9+, no API key needed:

```bash
python3 scripts/validate_dataset.py data/questions.csv examples/answers.synthetic.jsonl
python3 -m unittest discover -s tests -v
```

Next steps are documented in the [roadmap](docs/roadmap.md): a frozen pilot set, real recorded runs, reference evidence and independent scoring.

[Portfolio home](https://github.com/Donna-li2611)

**README reviewed: 2026-10-06.** This refresh adds a reviewer introduction, not new experiment results.

---

## 中文说明

**这是我个人独立开展的项目，构思、设计、研究、制作与已有成果均由我本人完成，过程中使用AI工具辅助。**

# 健康问答评测 · Health LLM Evaluation

**让模型回答可以被追溯、比较与复核。**

项目研究不同模型、入口与联网条件下的健康问答差异，并将回答、引用、评分和实验条件放在同一条证据链上。

**当前状态：公开方法与工具首版。未完成正式模型比较，未发布排名。**

## 已有内容

- [实验协议](docs/protocol.md)：控制变量、重复运行与留出题。
- [评分规则](docs/rubric.md)：事实、完整性、安全边界、信源和表达。
- [20 道自编题](data/questions.csv)：试运行种子题，未经过专家审定，不是黄金标准。
- [记录格式](docs/data-contract.md)：成功、失败与未评分状态分别保存。
- [校验工具](scripts/validate_dataset.py)：检查 ID、问题关联、时间和缺失字段。
- [结果状态](results/README.md)：尚无真实模型评测结果。

## 快速开始

只需要 Python 3.9+，无需 API 密钥：

```bash
python3 scripts/validate_dataset.py data/questions.csv examples/answers.synthetic.jsonl
python3 -m unittest discover -s tests -v
```

示例回答仅为格式演示，明确标记 synthetic。工具校验数据结构，不判断医学正确性，也不调用模型或自动发布结果。

## 目录

```text
docs/        实验、评分、数据契约与路线图
data/        自编问题与数据集说明
examples/    合成格式示例
scripts/     可运行的数据校验器
tests/       校验器的错误与边界用例
results/     正式结果状态与报告模板
```

本公开包整理自我个人项目的方法设计，使用自编试运行题与合成格式示例。拟覆盖的平台与采集方式须在每次实验中重新确认；尚未接入的平台不会列为已完成能力。

项目使用 AI 辅助设计与实现。公开题目用于研究准备，不提供诊断或治疗意见。
