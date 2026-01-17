from langchain.tools import tool, ToolRuntime
from typing import Optional, Dict, Any
import json


@tool
def analyze_user_profile(user_info: str, runtime: ToolRuntime = None) -> str:
    """
    分析用户提供的个人信息，生成结构化画像，用于就业建议。
    
    Args:
        user_info: 用户信息字符串，可以是自由文本或JSON格式。
            建议包含以下信息：
            - 专业/学历 (major)
            - 技能 (skills)
            - 工作经验 (work_experience)
            - 兴趣领域 (interests)
            - 地理位置 (location)
            - 职业目标 (career_goals)
            - 薪资期望 (salary_expectation)
            例如："我是计算机科学专业应届生，会Python和Java，想找后端开发工作，在北京"
        runtime: LangChain工具运行时
        
    Returns:
        结构化用户画像分析结果。
    """
    # 尝试解析JSON，如果不是JSON则按文本处理
    try:
        info_dict = json.loads(user_info)
        is_json = True
    except json.JSONDecodeError:
        info_dict = {"raw_text": user_info}
        is_json = False
    
    # 分析文本提取关键信息
    analysis = {
        "专业/学历": "未提及",
        "技能": [],
        "工作经验": "未提及",
        "兴趣领域": "未提及",
        "地理位置": "未提及",
        "职业目标": "未提及",
        "薪资期望": "未提及",
        "匹配岗位类型": [],
        "技能缺口": []
    }
    
    text = user_info.lower() if not is_json else " ".join(str(v).lower() for v in info_dict.values())
    
    # 简单关键词匹配（实际应用中可用更复杂的NLP）
    # 专业检测
    major_keywords = {
        "计算机": ["计算机", "软件", "编程", "码农", "程序员", "开发", "cs", "computer science"],
        "金融": ["金融", "经济", "会计", "银行", "投资", "财务"],
        "市场营销": ["市场", "营销", "销售", "广告", "品牌"],
        "设计": ["设计", "美术", "ui", "ux", "平面"],
        "工程": ["工程", "机械", "电子", "电气", "土木"],
        "医学": ["医学", "医疗", "护理", "医生", "护士"],
        "教育": ["教育", "教师", "培训", "教学"],
    }
    
    for major, keywords in major_keywords.items():
        if any(keyword in text for keyword in keywords):
            analysis["专业/学历"] = major
            break
    
    # 技能检测
    skill_keywords = {
        "编程": ["python", "java", "c++", "javascript", "php", "go", "rust", "编程", "代码", "开发"],
        "前端": ["前端", "html", "css", "react", "vue", "angular", "网页"],
        "后端": ["后端", "服务器", "数据库", "api", "微服务", "分布式"],
        "数据分析": ["数据分析", "数据挖掘", "sql", "excel", "统计", "机器学习", "ai"],
        "设计": ["设计", "ps", "photoshop", "figma", "sketch", "ui", "ux"],
        "语言": ["英语", "日语", "法语", "德语", "外语"],
        "管理": ["管理", "领导", "团队", "项目", "协调"],
    }
    
    for skill, keywords in skill_keywords.items():
        if any(keyword in text for keyword in keywords):
            if skill not in analysis["技能"]:
                analysis["技能"].append(skill)
    
    # 工作经验检测
    if "应届" in text or "毕业生" in text or "刚毕业" in text:
        analysis["工作经验"] = "应届毕业生"
    elif "实习" in text:
        analysis["工作经验"] = "有实习经验"
    elif "经验" in text and ("年" in text or "工作" in text):
        analysis["工作经验"] = "有工作经验"
    
    # 地理位置检测
    location_keywords = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安"]
    for loc in location_keywords:
        if loc in text:
            analysis["地理位置"] = loc
            break
    
    # 职业目标检测
    goal_keywords = {
        "技术开发": ["开发", "编程", "码农", "工程师", "程序员"],
        "产品经理": ["产品", "pm", "产品经理"],
        "运营": ["运营", "用户运营", "内容运营"],
        "市场": ["市场", "营销", "销售"],
        "设计": ["设计", "ui", "ux", "视觉"],
        "数据分析": ["数据分析", "数据科学家", "bi"],
    }
    
    for goal, keywords in goal_keywords.items():
        if any(keyword in text for keyword in keywords):
            analysis["职业目标"] = goal
            break
    
    # 薪资期望检测
    if "薪资" in text or "工资" in text or "薪酬" in text:
        analysis["薪资期望"] = "有明确期望"
    
    # 根据分析推荐岗位类型
    if analysis["专业/学历"] == "计算机" or "编程" in analysis["技能"]:
        analysis["匹配岗位类型"].extend(["软件开发工程师", "后端开发", "前端开发", "全栈开发"])
    if "数据分析" in analysis["技能"] or analysis["职业目标"] == "数据分析":
        analysis["匹配岗位类型"].extend(["数据分析师", "数据科学家", "商业分析师"])
    if "设计" in analysis["技能"] or analysis["职业目标"] == "设计":
        analysis["匹配岗位类型"].extend(["UI设计师", "UX设计师", "平面设计师"])
    
    # 去重
    analysis["匹配岗位类型"] = list(set(analysis["匹配岗位类型"]))
    
    # 生成报告
    report_lines = []
    report_lines.append("# 用户画像分析报告")
    report_lines.append("")
    
    for key, value in analysis.items():
        if isinstance(value, list):
            if value:
                report_lines.append(f"**{key}**：{', '.join(value)}")
            else:
                report_lines.append(f"**{key}**：暂无")
        else:
            report_lines.append(f"**{key}**：{value}")
    
    report_lines.append("")
    report_lines.append("## 分析说明")
    report_lines.append("1. 此分析基于关键词匹配，仅供参考")
    report_lines.append("2. 建议提供更详细的信息以获得更精准的分析")
    report_lines.append("3. 可结合就业市场数据生成个性化建议")
    
    return "\n".join(report_lines)


@tool
def generate_personalized_advice(
    user_profile: str, 
    industry: str, 
    location: str = "",
    runtime: ToolRuntime = None
) -> str:
    """
    根据用户画像和行业方向生成个性化就业建议。
    
    Args:
        user_profile: 用户画像分析结果（来自analyze_user_profile）
        industry: 目标行业/职业方向
        location: 目标地区（可选）
        runtime: LangChain工具运行时
        
    Returns:
        个性化就业建议报告。
    """
    # 这里可以集成更多分析逻辑，目前先返回基础建议
    advice_lines = []
    advice_lines.append(f"# 个性化就业建议：{industry}")
    if location:
        advice_lines.append(f"**目标地区**：{location}")
    advice_lines.append("")
    
    advice_lines.append("## 基于您的画像")
    advice_lines.append(user_profile)
    advice_lines.append("")
    
    advice_lines.append("## 建议方向")
    advice_lines.append(f"1. **岗位匹配**：建议关注{industry}领域的以下岗位：")
    advice_lines.append("   - 初级/助理岗位（适合应届生）")
    advice_lines.append("   - 实习转正机会")
    advice_lines.append("   - 专项培训计划")
    advice_lines.append("")
    
    advice_lines.append("2. **技能提升**：")
    advice_lines.append("   - 补充行业相关证书")
    advice_lines.append("   - 参与实际项目积累经验")
    advice_lines.append("   - 学习最新工具和技术")
    advice_lines.append("")
    
    advice_lines.append("3. **求职策略**：")
    advice_lines.append("   - 关注行业头部公司招聘动态")
    advice_lines.append("   - 利用校友网络和内推机会")
    advice_lines.append("   - 准备针对性简历和面试")
    advice_lines.append("")
    
    advice_lines.append("## 下一步行动")
    advice_lines.append("1. 使用`search_employment_market`工具搜索具体岗位需求")
    advice_lines.append("2. 使用`get_employment_trend`工具了解行业趋势")
    advice_lines.append("3. 根据市场反馈调整求职策略")
    
    return "\n".join(advice_lines)