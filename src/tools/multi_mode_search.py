"""
多层数据获取方案 - 用户可选模式

设计思路：
- 保留原有的 search_employment_market（搜索引擎模式）
- 新增 get_real_jobs（真实招聘数据模式）
- 让用户或Agent根据需求选择使用哪个工具
"""

from langchain.tools import tool, ToolRuntime
from typing import Optional, Literal
import json

@tool
def search_employment_market_v2(
    query: str,
    data_depth: Literal["shallow", "deep"] = "shallow",
    runtime: ToolRuntime = None
) -> str:
    """
    就业市场信息搜索 - 支持可选的数据深度。

    Args:
        query: 搜索关键词，例如 "前端开发 就业市场"
        data_depth: 数据深度，可选值：
            - "shallow"：浅层模式（默认）
              使用搜索引擎，快速获取市场趋势和报告
              适合：了解行业概况、趋势分析
            - "deep"：深层模式
              尝试获取真实招聘数据（需配置API）
              适合：求职决策、岗位对比
        runtime: LangChain工具运行时

    Returns:
        搜索结果，包含市场信息和真实岗位数据
    """
    from tools.web_search_tool import web_search

    if runtime is None:
        return "错误：缺少运行时上下文"

    ctx = runtime.context

    # ========== 浅层模式：搜索引擎 ==========
    if data_depth == "shallow":
        result_lines = []
        result_lines.append("## 📊 就业市场分析（浅层模式）")
        result_lines.append("")
        result_lines.append("**数据来源**：搜索引擎 + AI总结")
        result_lines.append("**适用场景**：了解行业趋势、市场概况")
        result_lines.append("**数据时效**：最近1个月内")
        result_lines.append("")
        result_lines.append("---")
        result_lines.append("")

        # 调用搜索引擎
        web_items, summary, image_items, raw_result = web_search(
            ctx=ctx,
            query=query,
            search_type="web_summary",
            count=10,
            need_summary=True,
            time_range="OneMonth",
            sites="51job.com|zhaopin.com|liepin.com|lagou.com"  # 只搜招聘网站
        )

        # AI总结
        result_lines.append("### 🤖 AI智能总结")
        result_lines.append(summary if summary else "暂无总结")
        result_lines.append("")

        # 详细结果
        result_lines.append("### 📋 详细信息")
        for i, item in enumerate(web_items[:5], 1):
            result_lines.append(f"**{i}. {item.Title}**")
            result_lines.append(f"- 来源：{item.SiteName or '未知'}")
            result_lines.append(f"- 发布时间：{item.PublishTime or '未知'}")
            result_lines.append(f"- 权威度：{item.AuthInfoDes} (等级{item.AuthInfoLevel})")
            if item.Url:
                result_lines.append(f"- 链接：{item.Url}")
            result_lines.append(f"- 摘要：{item.Snippet}")
            result_lines.append("")

        result_lines.append("---")
        result_lines.append("")
        result_lines.append("### 💡 数据说明")
        result_lines.append("- 本数据来自招聘网站公开发布的**报告、新闻、趋势分析**")
        result_lines.append("- 适用于了解**宏观市场情况**和**行业趋势**")
        result_lines.append("- **不包含**实时岗位列表，如需具体职位请使用深层模式")
        result_lines.append("- 建议访问原始链接获取详细信息")
        result_lines.append("")
        result_lines.append("### 🎯 下一步建议")
        result_lines.append("- 如果您想了解**具体岗位**和**实时招聘**信息")
        result_lines.append("- 请告诉我：\"我想看真实招聘数据\" 或 \"使用深层模式\"")
        result_lines.append("- 我可以为您调用深层模式获取更多具体信息")

        return "\n".join(result_lines)

    # ========== 深层模式：真实招聘数据 ==========
    elif data_depth == "deep":
        result_lines = []
        result_lines.append("## 📊 就业市场分析（深层模式）")
        result_lines.append("")
        result_lines.append("**数据来源**：真实招聘数据（API或爬虫）")
        result_lines.append("**适用场景**：求职决策、岗位对比、薪资分析")
        result_lines.append("**数据时效**：实时/准实时")
        result_lines.append("")
        result_lines.append("---")
        result_lines.append("")

        # 尝试获取真实招聘数据
        try:
            # 方案1：如果配置了官方API，使用API
            if is_api_configured():
                real_jobs = get_jobs_from_api(query, ctx)
                result_lines.append("### ✅ 数据来源：官方API")
                result_lines.append(format_real_jobs(real_jobs))
            # 方案2：如果没有API，返回说明
            else:
                result_lines.append("### ⚠️ 深层模式说明")
                result_lines.append("")
                result_lines.append("当前系统**未配置**真实的招聘数据API。")
                result_lines.append("")
                result_lines.append("**深层模式可获取**：")
                result_lines.append("- ✅ 真实岗位列表（实时更新）")
                result_lines.append("- ✅ 具体薪资信息")
                result_lines.append("- ✅ 详细的岗位要求")
                result_lines.append("- ✅ 公司信息")
                result_lines.append("")
                result_lines.append("**如何开启深层模式**：")
                result_lines.append("1. 申请招聘平台开放API（Boss直聘、拉勾等）")
                result_lines.append("2. 或购买第三方招聘数据服务")
                result_lines.append("3. 配置API密钥到系统中")
                result_lines.append("")
                result_lines.append("**临时替代方案**：")
                result_lines.append("- 访问招聘网站直接搜索：")
                result_lines.append("  - Boss直聘：https://www.zhipin.com/")
                result_lines.append("  - 拉勾网：https://www.lagou.com/")
                result_lines.append("  - 猎聘：https://www.liepin.com/")
                result_lines.append("  - 51job：https://www.51job.com/")

        except Exception as e:
            result_lines.append(f"### ❌ 获取真实数据失败")
            result_lines.append(f"错误信息：{str(e)}")
            result_lines.append("")
            result_lines.append("**当前使用浅层模式作为替代**")
            # 回退到浅层模式
            shallow_result = search_employment_market_v2(query, "shallow", runtime)
            return shallow_result

        return "\n".join(result_lines)


def is_api_configured() -> bool:
    """
    检查是否配置了招聘数据API

    Returns:
        bool: 是否已配置
    """
    import os

    # 检查环境变量
    api_key = os.getenv("RECRUITMENT_API_KEY")
    api_endpoint = os.getenv("RECRUITMENT_API_ENDPOINT")

    return bool(api_key and api_endpoint)


def get_jobs_from_api(query: str, ctx) -> list:
    """
    从API获取真实招聘数据

    Args:
        query: 搜索关键词
        ctx: 上下文对象

    Returns:
        list: 职位列表
    """
    import os
    import requests
    from coze_coding_utils.runtime_ctx.context import default_headers

    api_key = os.getenv("RECRUITMENT_API_KEY")
    api_endpoint = os.getenv("RECRUITMENT_API_ENDPOINT")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    headers.update(default_headers(ctx))

    # 调用API（示例，实际API调用方式根据具体平台调整）
    params = {
        "keyword": query,
        "page": 1,
        "pageSize": 10,
    }

    response = requests.get(api_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # 根据API返回格式解析
        return data.get("jobs", [])
    else:
        raise Exception(f"API调用失败: {response.status_code}")


def format_real_jobs(jobs: list) -> str:
    """
    格式化真实职位数据

    Args:
        jobs: 职位列表

    Returns:
        str: 格式化后的职位信息
    """
    if not jobs:
        return "暂无相关职位"

    lines = []
    lines.append(f"### 📝 找到 {len(jobs)} 个相关岗位")
    lines.append("")

    for i, job in enumerate(jobs, 1):
        lines.append(f"**{i}. {job.get('title', '未知职位')}**")
        lines.append(f"- 公司：{job.get('company', '未知公司')}")
        lines.append(f"- 薪资：{job.get('salary', '面议')}")
        lines.append(f"- 地点：{job.get('location', '未知')}")
        lines.append(f"- 经验要求：{job.get('experience', '未知')}")
        lines.append(f"- 学历要求：{job.get('education', '未知')}")
        lines.append(f"- 发布时间：{job.get('publishTime', '未知')}")
        if job.get('url'):
            lines.append(f"- 查看详情：{job['url']}")
        lines.append("")

        if job.get('description'):
            lines.append(f"**职位描述**：")
            lines.append(f"```")
            lines.append(job['description'][:200] + "..." if len(job['description']) > 200 else job['description'])
            lines.append(f"```")
            lines.append("")

    return "\n".join(lines)


# ========== 用户引导工具 ==========

@tool
def guide_user_choice(query: str, runtime: ToolRuntime = None) -> str:
    """
    根据用户查询，引导用户选择合适的数据模式。

    Args:
        query: 用户的查询内容
        runtime: LangChain工具运行时

    Returns:
        引导建议
    """
    query_lower = query.lower()

    # 判断用户需求类型
    trend_keywords = ['趋势', '前景', '发展', '市场', '概况', '分析']
    job_keywords = ['岗位', '职位', '招聘', '工作', '薪资', '具体', '投递', '找工作']

    if any(kw in query_lower for kw in trend_keywords):
        return """
## 💡 推荐使用：浅层模式

**原因**：
- 您想了解的是行业**趋势**和**市场概况**
- 浅层模式提供的是**行业报告**和**趋势分析**
- 数据来自招聘平台发布的公开报告，更有参考价值

**浅层模式会提供**：
- ✅ 行业发展趋势分析
- ✅ 薪资水平调查
- ✅ 技能需求变化
- ✅ 市场供需情况
- ✅ 权威数据来源

**如果您需要**：
- 了解"前端开发就业前景如何？" ✅ 浅层模式
- 分析"2025年IT行业趋势" ✅ 浅层模式
- 查询"程序员平均薪资水平" ✅ 浅层模式

---

**需要切换到深层模式吗？**
如果您的需求是：
- 找具体的岗位
- 查看实时招聘信息
- 准备投递简历

请告诉我：**"我想看真实招聘数据"** 或 **"使用深层模式"**
"""

    elif any(kw in query_lower for kw in job_keywords):
        return """
## 💡 推荐使用：深层模式

**原因**：
- 您想了解的是**具体岗位**和**招聘信息**
- 深层模式提供的是**真实的职位数据**
- 适合求职决策和简历投递

**深层模式会提供**：
- ✅ 真实的岗位列表（实时更新）
- ✅ 具体的薪资信息
- ✅ 详细的岗位要求
- ✅ 公司信息
- ✅ 可直接投递的链接

**如果您需要**：
- 查找"北京前端开发岗位" ✅ 深层模式
- 了解"腾讯具体薪资多少" ✅ 深层模式
- 准备"投递简历找工作" ✅ 深层模式

---

**当前深层模式状态**：
- 如果已配置API：会立即获取真实数据
- 如果未配置API：会提供替代方案（推荐访问招聘网站）

---

**需要现在调用深层模式吗？**
请告诉我：**"是的，使用深层模式"** 或 **"显示具体岗位"**
"""

    else:
        return """
## 💡 请选择数据模式

**根据您的需求，我提供两种模式：**

### 📊 浅层模式（默认）
- **数据类型**：行业报告、趋势分析、市场概况
- **数据来源**：招聘网站公开报告 + AI总结
- **适用场景**：
  - 了解行业趋势
  - 分析就业前景
  - 查看薪资调查
  - 了解技能需求
- **优点**：快速、免费、权威、有参考价值
- **缺点**：不包含实时岗位列表

---

### 💼 深层模式（可选）
- **数据类型**：真实岗位列表、具体职位信息
- **数据来源**：招聘数据API或爬虫
- **适用场景**：
  - 查找具体岗位
  - 了解实时招聘信息
  - 准备投递简历
  - 对比公司薪资
- **优点**：真实、具体、实时
- **缺点**：可能需要配置、速度较慢

---

## 🎯 您想了解什么？

**示例问题**：
- "前端开发的就业前景怎么样？" → 建议浅层模式
- "我想找北京前端开发的工作" → 建议深层模式
- "AI工程师平均薪资多少" → 建议浅层模式
- "腾讯有哪些前端岗位在招" → 建议深层模式

---

请告诉我您的具体需求，我会为您选择最合适的模式！
"""
