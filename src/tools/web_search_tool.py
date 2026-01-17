import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import tool, ToolRuntime
from cozeloop.decorator import observe
from coze_coding_utils.runtime_ctx.context import Context, default_headers


class WebItem(BaseModel):
    """Web搜索结果项模型（对应WebItem-搜索结果项）"""

    Id: str = Field(..., description="结果Id")
    SortId: int = Field(..., description="排序Id")
    Title: str = Field(..., description="标题")
    SiteName: Optional[str] = Field(None, description="站点名")
    Url: Optional[str] = Field(None, description="落地页")
    Snippet: str = Field(..., description="普通摘要（100字左右的相关切片）")
    Summary: Optional[str] = Field(None, description="精准摘要（300~500字左右经过模型处理的相关片段）")
    Content: Optional[str] = Field(None, description="正文（引用站点正文）")
    PublishTime: Optional[str] = Field(None, description="发布时间, ISO时间格式\n示例: 2025-05-30T19:35:24+08:00")
    LogoUrl: Optional[str] = Field(None, description="落地页IconUrl链接")
    RankScore: Optional[float] = Field(None, description="得分")
    AuthInfoDes: str = Field(..., description="权威度描述, 包括: 非常权威、正常权威、一般权威、一般不权威")
    AuthInfoLevel: int = Field(...,
                               description="权威度评级, 对应权威度描述, 包括: 1 非常权威、2 正常权威、3 一般权威、4 一般不权威")


class ImageInfo(BaseModel):
    """ImageInfo-图片结果项（图片详情子模型）"""

    Url: str = Field(..., description="图片链接")
    Width: Optional[int] = Field(None, description="宽")
    Height: Optional[int] = Field(None, description="高")
    Shape: str = Field(
        ...,
        description="""横长方形，判断: (宽>高*1.2)；竖长方形，判断: (宽<高*1.2)；方形，判断: (其余情况)"""
    )


class ImageItem(BaseModel):
    """ImageItem-搜索结果项（SearchType=image的结果项）"""

    Id: str = Field(..., description="结果Id")
    SortId: int = Field(..., description="排序Id")
    Title: Optional[str] = Field(None, description="标题")
    SiteName: Optional[str] = Field(None, description="站点名")
    Url: Optional[str] = Field(None, description="落地页")
    PublishTime: Optional[str] = Field(
        None,
        description="发布时间, ISO时间格式。示例: 2025-05-30T19:35:24+08:00"
    )
    Image: ImageInfo = Field(..., description="图片详情")


@observe
def web_search(
        ctx: Context,
        query: str,
        search_type: str = "web",
        count: Optional[int] = 10,
        need_content: Optional[bool] = False,
        need_url: Optional[bool] = False,
        sites: Optional[str] = None,
        block_hosts: Optional[str] = None,
        need_summary: Optional[bool] = True,
        time_range: Optional[str] = None,
) -> tuple[list[WebItem], str, Optional[list[ImageItem]], dict]:
    """
    融合信息搜索API，返回搜索结果项列表、搜索结果内容总结和原始响应数据。

    Args:
        ctx: 上下文对象，用于串联一次运行态的相关信息
        query (str): 用户搜索query，1~100个字符(过长会截断)，不支持多词搜索。
        search_type (str, 可选): 搜索类型枚举值，目前支持 web：web搜索，返回搜索到的站点信息；web_summary：web搜索总结版，返回搜索到的站点信息及LLM总结结果；image：图片搜索，返回搜索到的图片信息。
        count (int, 可选): 返回条数，最多50条，默认10条。
        need_content (bool, 可选): 是否仅返回有正文的结果，默认false（不限制必须有正文）。
        need_url (bool, 可选): 是否仅返回原文链接的结果，默认false（不限制必须有Url）。
        sites (str, 可选): 指定搜索的Site范围，多个域名使用'|'分隔，最多支持5个。需填入完整域名，示例：aliyun.com|mp.qq.com。
        block_hosts (str, 可选): 指定屏蔽的搜索Site，多个域名使用'|'分隔，最多支持5个。需填入完整域名，示例：aliyun.com|mp.qq.com。
        need_summary (bool, 可选): 是否需要精准摘要，默认true。调用 web_summary web搜索总结版 时，本字段必须为true。
        time_range (str, 可选): 指定搜索的发文时间。以下枚举值，不填即为不限制：OneDay：1天内；OneWeek：1周内；OneMonth：1月内；OneYear：1年内；YYYY-MM-DD..YYYY-MM-DD：从日期A（包含）至日期B（包含）区间段内发文的内容，示例"2024-12-30..2025-12-30"。

    Returns:
        tuple[list[WebItem], str, Optional[list[ImageItem]], dict]: 包含WebItem列表、搜索结果摘要、ImageItem列表(如有)和原始响应数据的元组。
    """
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_BASE_URL")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    headers.update(default_headers(ctx))
    request = {
        "Query": query,
        "SearchType": search_type,
        "Count": count,
        "Filter": {
            "NeedContent": need_content,
            "NeedUrl": need_url,
            "Sites": sites,
            "BlockHosts": block_hosts,
        },
        "NeedSummary": need_summary,
        "TimeRange": time_range,
    }
    try:
        response = requests.post(f'{base_url}/api/search_api/web_search', json=request, headers=headers)
        response.raise_for_status()  # 检查HTTP请求状态
        data = response.json()

        response_metadata = data.get("ResponseMetadata", {})
        result = data.get("Result", {})
        if response_metadata.get("Error"):
            raise Exception(f"web_search 失败: {response_metadata.get('Error')}")

        web_items = []
        image_items = []
        if result.get("WebResults"):
            web_items = [WebItem(**item) for item in result.get("WebResults", [])]
        if result.get("ImageResults"):
            image_items = [ImageItem(**item) for item in result.get("ImageResults", [])]
        content = None
        if result.get("Choices"):
            content = result.get("Choices", [{}])[0].get("Message", {}).get("Content", "")
        return web_items, content, image_items, result
    except requests.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"web_search 失败: {str(e)}")
    finally:
        response.close()


@tool
def search_employment_market(query: str, runtime: ToolRuntime) -> str:
    """
    搜索就业市场信息，包括岗位需求、薪资水平、行业趋势等。
    
    Args:
        query: 搜索关键词，例如 "前端开发 就业市场 2025" 或 "数据分析师 薪资 北京"
        runtime: LangChain工具运行时，用于获取上下文
        
    Returns:
        格式化后的搜索结果字符串，包含相关就业市场信息。
    """
    ctx = runtime.context  # 获取Context对象
    # 调用web_search函数，使用默认参数
    web_items, summary, image_items, raw_result = web_search(
        ctx=ctx,
        query=query,
        search_type="web_summary",  # 使用总结版，获取LLM总结
        count=10,
        need_summary=True,
        time_range="OneMonth"  # 默认搜索一个月内的信息，保证时效性
    )
    
    # 格式化结果
    result_lines = []
    result_lines.append(f"## 就业市场搜索：{query}")
    result_lines.append(f"**AI总结**：{summary if summary else '暂无总结'}")
    result_lines.append("\n**详细结果**：")
    
    for i, item in enumerate(web_items[:5]):  # 只显示前5条
        result_lines.append(f"{i+1}. **{item.Title}**")
        result_lines.append(f"   来源：{item.SiteName or '未知'}")
        result_lines.append(f"   摘要：{item.Snippet}")
        if item.PublishTime:
            result_lines.append(f"   发布时间：{item.PublishTime}")
        if item.Url:
            result_lines.append(f"   链接：{item.Url}")
        result_lines.append("")
    
    # 添加统计数据
    result_lines.append(f"**共找到 {len(web_items)} 条相关结果**")
    
    return "\n".join(result_lines)


@tool
def get_employment_trend(industry: str, location: str = "", runtime: ToolRuntime = None) -> str:
    """
    获取特定行业和地区的就业趋势报告。
    
    Args:
        industry: 行业/职业方向，例如 "软件开发"、"市场营销"、"金融分析"
        location: 地区，例如 "北京"、"上海"、"全国"（可选）
        runtime: LangChain工具运行时
        
    Returns:
        就业趋势分析报告。
    """
    if runtime is None:
        return "错误：缺少运行时上下文"
    
    ctx = runtime.context
    query = f"{industry} 就业趋势 市场需求 薪资水平"
    if location:
        query = f"{location} {query}"
    
    web_items, summary, image_items, raw_result = web_search(
        ctx=ctx,
        query=query,
        search_type="web_summary",
        count=15,
        need_summary=True,
        time_range="OneYear"  # 就业趋势可以看一年内的变化
    )
    
    # 构建分析报告
    report_lines = []
    report_lines.append(f"# {industry}就业趋势分析报告")
    if location:
        report_lines.append(f"**地区**：{location}")
    report_lines.append(f"**分析时间**：{raw_result.get('Timestamp', '近期')}")
    report_lines.append("\n## 市场概况")
    report_lines.append(summary if summary else "暂无AI总结")
    
    report_lines.append("\n## 关键发现")
    
    # 从结果中提取关键信息
    salary_mentions = 0
    demand_mentions = 0
    skill_mentions = {}
    
    for item in web_items:
        content = f"{item.Title} {item.Snippet} {item.Summary or ''}".lower()
        if "薪资" in content or "工资" in content or "薪酬" in content:
            salary_mentions += 1
        if "需求" in content or "招聘" in content or "岗位" in content:
            demand_mentions += 1
    
    report_lines.append(f"1. **薪资关注度**：在{len(web_items)}条结果中，{salary_mentions}条提及薪资信息")
    report_lines.append(f"2. **市场需求**：{demand_mentions}条结果提及招聘需求")
    
    report_lines.append("\n## 建议搜索关键词")
    report_lines.append(f"- {industry} 岗位需求")
    report_lines.append(f"- {industry} 薪资水平")
    report_lines.append(f"- {industry} 技能要求")
    if location:
        report_lines.append(f"- {location} {industry} 招聘")
    
    report_lines.append("\n## 数据来源")
    unique_sites = set(item.SiteName for item in web_items if item.SiteName)
    for site in list(unique_sites)[:5]:
        report_lines.append(f"- {site}")
    
    return "\n".join(report_lines)