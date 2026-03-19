---
name: news-summary
description: This skill should be used when the user asks for news updates, daily briefings, or what's happening in the world. Fetches news from Chinese news websites and can create voice summaries.
---

# News Summary (国内版)

## Overview

获取并总结国内可访问的新闻源。

## News Sources

### 今日头条 (Primary)
```bash
# 热点新闻 API
curl -s "https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1152B8F0C9E0F8&cp=595F8C0E2A0E1"
```

### 网易新闻
```bash
# 排行榜
curl -s "https://news.163.com/special/cm_yaowen20200213/"
```

### 新浪新闻
```bash
# 国内新闻
curl -s "https://news.sina.cn/?vt=1&ws=1"
```

### 腾讯新闻
```bash
# 要闻
curl -s "https://news.qq.com/"
```

## Parse News

使用 PowerShell 解析网页示例：
```powershell
$html = Invoke-WebRequest -Uri "https://news.sina.cn/" -UseBasicParsing
$html.ParsedHtml.getElementsByTagName("a") | Select-Object -First 20 innerText, href
```

## Workflow

### Text summary
1. 获取今日头条热点新闻
2. 补充其他源（网易/腾讯）
3. 整理关键信息
4. 按分类展示

### Voice summary
1. 创建文字摘要
2. 用 OpenAI TTS 生成语音
3. 发送语音消息

## Output Format

```
📰 新闻摘要 [日期]

🔴 热点
- 新闻标题1
- 新闻标题2

📌 国内
- 新闻标题

🌍 国际
- 新闻标题

💰 财经
- 新闻标题
```

## Best Practices

- 保持简洁，6-10条重点新闻
- 优先最新和热点新闻
- 语音版控制在2分钟内
