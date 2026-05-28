# AI MBTI 测试 API 设计文档

## 概述

为 AI（如 Marvis、Claude、GPT 等）提供 MBTI 人格测试 API。AI 通过 HTTP 请求获取题目、自主作答、提交答案获取结果。

## 架构

```
AI → GET /api/questions → 28题JSON
AI → 自主思考作答
AI → POST /api/submit → 结果JSON（类型 + 维度得分 + 描述）
```

## 技术栈

- 托管：Vercel Serverless Functions
- 语言：Python（Flask）
- 数据：题库和16型描述写在代码常量中，无需数据库

## API 设计

### GET /api/questions

返回28道MBTI测试题。

响应格式：
```json
{
  "version": "28",
  "total": 28,
  "questions": [
    {
      "id": 1,
      "text": "当参加社交活动时，你通常：",
      "optionA": "很容易和很多人交流互动，享受热闹氛围。",
      "optionB": "更愿意和少数熟悉的人聊天，待在相对安静的角落。",
      "dimension": "EI",
      "a_indicates": "E",
      "b_indicates": "I"
    }
  ]
}
```

### POST /api/submit

提交答案，获取结果。

请求格式：
```json
{
  "answers": [
    {"q_id": 1, "choice": "A"},
    {"q_id": 2, "choice": "B"}
  ]
}
```

响应格式：
```json
{
  "type": "INTJ",
  "type_name": "建筑师",
  "dimensions": {
    "EI": {"E": 2, "I": 5, "result": "I"},
    "SN": {"S": 1, "N": 6, "result": "N"},
    "TF": {"T": 5, "F": 2, "result": "T"},
    "JP": {"J": 5, "P": 2, "result": "J"}
  },
  "description": "作为INTJ（建筑师），你...",
  "traits": ["理性", "独立", "战略思维"]
}
```

## 题库

28题，四个维度各7题：
- 第1-7题：E/I 维度
- 第8-14题：S/N 维度
- 第15-21题：T/F 维度
- 第22-28题：J/P 维度

## 计分规则

- 每个维度7题，统计A/B数量
- 选A多 → 取该维度第一个字母（如E），选B多 → 取第二个字母（如I）
- 平局时：EI取I，SN取N，TF取F，JP取P

## 16种人格类型

| 类型 | 名称 | 类型 | 名称 |
|------|------|------|------|
| INTJ | 建筑师 | INTP | 逻辑学家 |
| ENTJ | 指挥官 | ENTP | 辩论家 |
| INFJ | 提倡者 | INFP | 调停者 |
| ENFJ | 主人公 | ENFP | 竞选者 |
| ISTJ | 物流师 | ISFJ | 守卫者 |
| ESTJ | 总经理 | ESFJ | 执政官 |
| ISTP | 鉴赏家 | ISFP | 探险家 |
| ESTP | 企业家 | ESFP | 表演者 |

## 部署

1. 代码推送到 GitHub 仓库
2. Vercel 关联仓库，自动部署
3. API 地址：`https://<project>.vercel.app/api/questions` 和 `/api/submit`
