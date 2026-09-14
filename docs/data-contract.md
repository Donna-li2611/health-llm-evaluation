# 数据契约

问题 CSV：`question_id,topic,question,risk_level,origin,review_status`。首版全部为自编合成情境，review_status 为 pending_expert_review。

回答 JSONL 每行代表一次独立运行，必须包含：

| 字段 | 含义 |
| --- | --- |
| run_id / question_id | 运行 ID 与问题关联；run_id 唯一 |
| batch_id / repeat_index | 批次与从 1 开始的重复序号 |
| platform / model / model_version | 平台及已披露模型信息 |
| entry_type / network_enabled | 入口与联网条件 |
| run_at | 含时区的 ISO 8601 时间 |
| status | success 或 failed |
| answer_text / error | 成功保留原文；失败保留原因 |
| citations | 来源 URL 或来源记录，数组格式 |
| synthetic | 是否为合成演示，布尔值 |
| scoring_status | not_scored 或 scored |

演示记录必须 synthetic=true；正式实验应使用独立结果目录，不能把演示混入比较。校验器不验证网页真实性，不判断答案安全性，也不代替人工复核。
