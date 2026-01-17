# 前程无忧爬虫工具说明

## 📌 工具概述

本工具集包含了从前程无忧（51job）网站爬取招聘信息的功能，可以获取真实的职位数据并保存到本地文件中。

## 📁 文件说明

### 1. `src/tools/citynum.py`
- **功能**：城市名称到前程无忧城市代码的映射工具
- **用途**：将城市名称（如"深圳"、"北京"）转换为前程无忧网站所需的数字代码
- **示例**：
  - 输入：["深圳", "武汉"]
  - 输出："040000,180200"

### 2. `src/tools/data_saver.py`
- **功能**：数据保存工具
- **用途**：将爬取的招聘数据保存为 Excel 或 CSV 格式
- **保存路径**：`assets/jobs_data/`
- **文件命名格式**：`关键词_城市_招聘数据.xlsx`

### 3. `src/tools/recruitment_spider_51job.py`
- **功能**：前程无忧招聘信息爬虫（LangChain Tool 格式）
- **用途**：从前程无忧网站爬取招聘信息
- **返回**：爬取结果摘要，包括数据条数、保存路径等

## 🔧 使用方法

### 在 Agent 中使用

用户可以通过自然语言对话让 Agent 调用爬虫：

```
用户：帮我爬取深圳Python开发的职位信息，爬3页
Agent：正在从前程无忧爬取数据... 已保存到 assets/jobs_data/Python开发_深圳_招聘数据.xlsx
```

### 直接使用（Python 代码）

```python
from tools.recruitment_spider_51job import search_51job

# 爬取职位信息
result = search_51job("Python开发", "深圳", 3)
print(result)
```

## 📊 数据字段

爬取的数据包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| 职位名称 | 职位的名称 | Python开发工程师 |
| 公司名称 | 招聘公司名称 | 深圳市某某科技有限公司 |
| 薪资 | 薪资范围 | 15-25K/月 |
| 工作地点 | 工作城市 | 深圳 |
| 发布时间 | 职位发布时间 | 2024-01-15 |
| 招聘链接 | 职位详情链接 | http://jobs.51job.com/... |
| 公司链接 | 公司详情链接 | http://jobs.51job.com/... |

## ⚙️ 配置要求

### 依赖包

需要安装以下 Python 包：

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

如果使用 requirements.txt，确保包含：
- requests
- beautifulsoup4
- pandas
- openpyxl

### 网络要求

- 需要能够访问前程无忧网站（http://search.51job.com）
- 建议使用稳定的网络连接

## 🚀 工作流程

1. **用户请求**：用户通过对话请求爬取职位信息
2. **参数解析**：Agent 解析关键词、城市、页数等参数
3. **城市转换**：使用 `citynum.py` 将城市名称转换为代码
4. **爬取数据**：访问前程无忧网站，解析 HTML 页面
5. **保存数据**：使用 `data_saver.py` 保存到 Excel 文件
6. **返回结果**：返回爬取摘要给用户

## 🎯 与现有工具的集成

### 与 `read_local_jobs` 配合使用

爬取数据后，可以使用 `read_local_jobs` 工具读取并分析数据：

```
用户：爬取深圳Python开发的职位
Agent：爬取完成，保存到 assets/jobs_data/Python开发_深圳_招聘数据.xlsx

用户：读取刚才爬取的数据
Agent：已读取 50 条职位数据...

用户：分析这些数据的薪资分布
Agent：[生成薪资分布图]
```

### 与可视化工具配合

爬取的数据可以用于生成各种图表：

- `generate_salary_distribution_chart`：薪资分布图
- `generate_trend_chart`：职位趋势图
- `generate_skill_wordcloud`：技能需求词云

## ⚠️ 注意事项

1. **爬取频率**：建议设置合理的爬取页数（3-5页），避免请求过快被限制
2. **数据时效性**：爬取的数据反映了当前市场的招聘情况，建议定期更新
3. **网络问题**：如果网络不稳定，爬取可能会失败，可以重试
4. **反爬虫机制**：前程无忧可能有反爬虫机制，如遇到问题可以适当延迟请求间隔

## 🔍 常见问题

### Q1: 爬取失败怎么办？
A: 检查网络连接，确认能够访问前程无忧网站，然后重试。

### Q2: 为什么有些城市匹配不到？
A: `citynum.py` 中包含主要城市的代码，如果城市不在此列表中，会使用默认城市"深圳"。

### Q3: 数据保存在哪里？
A: 数据保存在 `assets/jobs_data/` 目录，文件格式为 Excel (.xlsx)。

### Q4: 可以一次爬取多个城市吗？
A: 可以！在参数中传入城市列表即可，如 ["深圳", "北京", "上海"]。

## 📈 后续优化方向

1. 支持更多招聘平台（如智联招聘、Boss直聘等）
2. 添加数据清洗和去重功能
3. 支持增量更新（只爬取新发布的职位）
4. 添加更详细的数据分析功能

## 📚 参考资料

- 前程无忧官网：https://www.51job.com/
- BeautifulSoup 文档：https://www.crummy.com/software/BeautifulSoup/
- Pandas 文档：https://pandas.pydata.org/
