"""
词云生成工具

为就业市场分析生成词云，展示热门职位、技能、公司等关键词
"""

import os
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm
from typing import Optional, List, Dict, Any
from collections import Counter
from langchain.tools import tool

# 配置中文字体 - 优先使用系统中已确认的字体文件
chinese_font = None

# 优先使用文泉驿微米黑（支持中文，显示效果较好）
preferred_font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
if os.path.exists(preferred_font_path):
    chinese_font = preferred_font_path
else:
    # 备用字体路径列表
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/arphic/uming.ttc',
        '/usr/share/fonts/truetype/arphic/ukai.ttc'
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            chinese_font = font_path
            break


def extract_keywords(text: str, max_words: int = 100) -> Dict[str, int]:
    """从文本中提取关键词"""
    # 移除标点符号和特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)

    # 分词（简单按空格和常见分隔符）
    words = text.split()

    # 过滤掉太短的词和常见停用词
    stop_words = {'的', '了', '在', '是', '和', '与', '或', '但', '等', '及', '这', '那',
                  'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}

    filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]

    # 统计词频
    word_freq = Counter(filtered_words)

    # 返回前N个高频词
    return dict(word_freq.most_common(max_words))


def parse_keyword_text(text: str) -> Dict[str, int]:
    """
    解析用户输入的关键词文本格式
    支持格式：
    1. "数据分析(95)、Python(90)、SQL(88)"
    2. "数据分析 95, Python 90, SQL 88"
    3. "数据分析:95, Python:90, SQL:88"
    """
    word_freq = {}

    # 尝试匹配 "关键词(权重)" 或 "关键词:权重" 格式
    pattern = r'([^\s()、,，:：]+)[\(:：](\d+)'

    matches = re.findall(pattern, text)
    if matches:
        for keyword, weight in matches:
            keyword = keyword.strip()
            weight = int(weight)
            if keyword and weight > 0:
                word_freq[keyword] = weight
    else:
        # 如果没有匹配到，尝试使用原始文本提取方法
        return extract_keywords(text)

    return word_freq


def get_sample_keywords(max_words: int = 100) -> Dict[str, int]:
    """获取示例关键词数据"""
    keywords = [
        ("Python", 100), ("Java", 95), ("JavaScript", 90), ("SQL", 88), ("React", 85),
        ("Vue", 82), ("数据分析", 95), ("机器学习", 80), ("深度学习", 70), ("算法", 75),
        ("后端开发", 85), ("前端开发", 88), ("全栈开发", 75), ("移动开发", 70),
        ("云计算", 65), ("大数据", 78), ("人工智能", 72), ("区块链", 55), ("物联网", 60),
        ("DevOps", 68), ("微服务", 75), ("Docker", 70), ("Kubernetes", 65), ("Git", 80),
        ("Linux", 78), ("MySQL", 82), ("PostgreSQL", 70), ("MongoDB", 65), ("Redis", 75),
        ("测试", 70), ("自动化测试", 65), ("性能优化", 72), ("系统设计", 78), ("架构", 75),
        ("网络安全", 60), ("数据安全", 58), ("产品经理", 75), ("UI设计", 68), ("UX设计", 65),
        ("项目管理", 72), ("敏捷开发", 70), ("Scrum", 65), ("数据分析", 95), ("数据挖掘", 70),
        ("自然语言处理", 60), ("计算机视觉", 58), ("推荐系统", 62), ("数据可视化", 68),
        ("TensorFlow", 55), ("PyTorch", 60), ("Keras", 50), ("Flask", 65), ("Django", 70),
        ("Spring", 75), ("SpringBoot", 72), ("MyBatis", 65), ("Vue.js", 80), ("Angular", 55),
        ("TypeScript", 70), ("Node.js", 68), ("Go", 60), ("Rust", 50), ("C++", 65),
        ("C#", 62), ("PHP", 55), ("Ruby", 50), ("Swift", 52), ("Kotlin", 55),
        ("Flutter", 58), ("ReactNative", 60), ("Electron", 55), ("Web3", 45), ("Metaverse", 40),
        ("Unity", 50), ("Unreal", 48), ("游戏开发", 65), ("VR", 52), ("AR", 50),
        ("低代码", 58), ("无代码", 55), ("SaaS", 62), ("PaaS", 58), ("IaaS", 55),
        ("Serverless", 60), ("FaaS", 55), ("边缘计算", 55), ("5G", 58), ("IoT", 60)
    ]

    return dict(keywords[:max_words])


def format_wordcloud_result(word_freq: Dict[str, int], filepath: str, title: str) -> str:
    """格式化词云结果"""
    # 按权重排序
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    result = f"""
## ☁️ 词云图已生成

**标题**：{title}
**保存路径**：{filepath}
**词汇数量**：{len(word_freq)}

---

### 🔥 TOP 20 热门词汇

| 排名 | 关键词 | 权重 | 热度 |
|------|--------|------|------|
"""

    for i, (word, weight) in enumerate(sorted_words[:20], 1):
        # 计算热度等级
        if weight >= 90:
            emoji = "🔥🔥🔥"
            level = "极热"
        elif weight >= 80:
            emoji = "🔥🔥"
            level = "很热"
        elif weight >= 70:
            emoji = "🔥"
            level = "热门"
        elif weight >= 60:
            emoji = "⭐"
            level = "流行"
        else:
            emoji = "📌"
            level = "常见"

        result += f"| {i} | **{word}** | {weight} | {emoji} {level} |\n"

    # 添加分析
    result += f"""
---

### 📊 数据分析

**整体特征**：
- 最热门词汇：**{sorted_words[0][0]}**（权重：{sorted_words[0][1]}）
- 前10名词汇平均权重：{sum(w for _, w in sorted_words[:10]) / 10:.1f}
- 权重分布范围：{sorted_words[-1][1]} - {sorted_words[0][1]}

**趋势洞察**：
"""

    # 分析趋势
    top_words = [word for word, _ in sorted_words[:10]]
    result += f"1. **技术方向**：前10名中，{'编程语言类' + str(len([w for w in top_words if w in ['Python', 'Java', 'JavaScript', 'Go', 'Rust']])) + '个' if any(w in ['Python', 'Java', 'JavaScript', 'Go', 'Rust'] for w in top_words) else '综合技术类'}\n"
    result += f"2. **关键词数量**：{'超过100' if len(word_freq) > 100 else f'共{len(word_freq)}'}个关键词\n"
    result += f"3. **权重集中度**：前5名占总权重的{sum(w for _, w in sorted_words[:5]) / sum(word_freq.values()) * 100:.1f}%\n"

    result += f"""
### 💡 使用建议

1. **技能学习**：优先学习权重高的关键词对应的技术或能力
2. **求职准备**：在简历和面试中突出这些热门技能
3. **市场观察**：关注新兴关键词，把握行业趋势
4. **竞品分析**：对比不同时期词云，了解市场变化

---

**📁 查看图片**：词云图已保存到 `{filepath}`，您可以下载或查看。
"""

    return result


def _generate_job_wordcloud_internal(
    text_data: Optional[str] = None,
    keywords: Optional[List[Dict[str, int]]] = None,
    title: str = "就业市场热门职位词云",
    max_words: int = 100,
    width: int = 1200,
    height: int = 800
) -> str:
    """
    内部函数：生成就业市场词云图（不使用@tool装饰器）

    Args:
        text_data: 文本数据，用于提取关键词（从招聘信息、职位描述等）
        keywords: 关键词列表，格式如[{"word": "Python", "weight": 95}, {"word": "Java", "weight": 85}]
        title: 词云标题
        max_words: 最大显示词数
        width: 图片宽度
        height: 图片高度

    Returns:
        包含词云文件路径和文本描述的字符串
    """
    try:
        # 创建输出目录
        output_dir = "assets/charts"
        os.makedirs(output_dir, exist_ok=True)

        # 处理关键词数据
        if keywords:
            # 使用提供的关键词权重
            word_freq = {kw['word']: kw.get('weight', 1) for kw in keywords if 'word' in kw}
        elif text_data:
            # 从文本数据中提取关键词
            word_freq = extract_keywords(text_data, max_words)
        else:
            # 使用示例数据
            word_freq = get_sample_keywords(max_words)

        if not word_freq:
            return "❌ 无法生成词云：没有提供有效的关键词数据"

        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 10))

        # 生成词云
        # 强制使用中文字体，确保中文能正确显示
        if chinese_font and os.path.exists(chinese_font):
            wordcloud = WordCloud(
                width=width,
                height=height,
                background_color='white',
                font_path=chinese_font,  # 使用完整字体路径
                max_words=max_words,
                relative_scaling=0.5,
                min_font_size=10,
                colormap='viridis',
                prefer_horizontal=0.9,  # 优先水平显示文字
                scale=2  # 提高清晰度
            ).generate_from_frequencies(word_freq)

            # 使用相同字体设置标题
            title_font_prop = fm.FontProperties(fname=chinese_font)
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20,
                        fontproperties=title_font_prop)
        else:
            # 如果没有中文字体，仍然生成词云但可能显示方框
            wordcloud = WordCloud(
                width=width,
                height=height,
                background_color='white',
                max_words=max_words,
                relative_scaling=0.5,
                min_font_size=10,
                colormap='viridis',
                prefer_horizontal=0.9,
                scale=2
            ).generate_from_frequencies(word_freq)
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        # 显示词云
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout(pad=0)

        plt.tight_layout(pad=0)

        # 保存词云
        # 过滤文件名中的特殊字符，避免系统解析错误
        safe_title = title
        # 替换或移除特殊字符
        safe_title = safe_title.replace(" ", "_")
        safe_title = safe_title.replace("-", "_")
        safe_title = safe_title.replace("/", "_")
        safe_title = safe_title.replace("\\", "_")
        safe_title = safe_title.replace(":", "_")
        safe_title = safe_title.replace("*", "_")
        safe_title = safe_title.replace("?", "_")
        safe_title = safe_title.replace('"', "_")
        safe_title = safe_title.replace("<", "_")
        safe_title = safe_title.replace(">", "_")
        safe_title = safe_title.replace("|", "_")
        # 移除连续的下划线
        safe_title = re.sub(r'_+', '_', safe_title)
        # 移除首尾的下划线
        safe_title = safe_title.strip('_')

        filename = f"{safe_title}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()

        # 生成文本描述
        return format_wordcloud_result(word_freq, filepath, title)

    except Exception as e:
        return f"❌ 生成词云失败：{str(e)}"


# 工具函数：调用内部函数生成就业市场词云
@tool
def generate_job_wordcloud(
    text_data: Optional[str] = None,
    keywords: Optional[List[Dict[str, int]]] = None,
    title: str = "就业市场热门职位词云",
    max_words: int = 100,
    width: int = 1200,
    height: int = 800
) -> str:
    """
    生成就业市场词云图

    Args:
        text_data: 文本数据，用于提取关键词（从招聘信息、职位描述等）
        keywords: 关键词列表，格式如[{"word": "Python", "weight": 95}, {"word": "Java", "weight": 85}]
        title: 词云标题
        max_words: 最大显示词数
        width: 图片宽度
        height: 图片高度

    Returns:
        包含词云文件路径和文本描述的字符串
    """
    return _generate_job_wordcloud_internal(
        text_data=text_data,
        keywords=keywords,
        title=title,
        max_words=max_words,
        width=width,
        height=height
    )


@tool
def generate_skill_wordcloud(
    skills_data: Optional[List[Dict[str, int]]] = None,
    skills_text: Optional[str] = None,
    job_title: str = "数据分析师"
) -> str:
    """
    生成技能需求词云图

    Args:
        skills_data: 技能数据，格式如[{"skill": "Python", "count": 95}, {"skill": "SQL", "count": 85}]
        skills_text: 技能文本数据，支持格式如"数据分析(95)、Python(90)、SQL(88)"
        job_title: 职位名称，用于标题

    Returns:
        包含词云文件路径和文本描述的字符串
    """
    if not skills_data:
        if skills_text:
            # 从文本中解析技能数据
            word_freq = parse_keyword_text(skills_text)
            skills_data = [{"skill": k, "count": v} for k, v in word_freq.items()]
        else:
            # 使用示例数据
            skills_data = [
                {"skill": "Python", "count": 95},
                {"skill": "SQL", "count": 90},
                {"skill": "Excel", "count": 85},
                {"skill": "Tableau", "count": 70},
                {"skill": "PowerBI", "count": 65},
                {"skill": "机器学习", "count": 60},
                {"skill": "统计学", "count": 55},
                {"skill": "数据分析", "count": 95},
                {"skill": "数据可视化", "count": 70},
                {"skill": "Hadoop", "count": 50},
                {"skill": "Spark", "count": 45},
                {"skill": "Pandas", "count": 80},
                {"skill": "NumPy", "count": 75},
                {"skill": "Matplotlib", "count": 65},
                {"skill": "沟通能力", "count": 60},
                {"skill": "业务理解", "count": 70}
            ]

    # 转换为关键词格式
    keywords = [{"word": item['skill'], "weight": item['count']} for item in skills_data]

    # 生成标题，避免重复的后缀
    if "技能需求词云" in job_title or "技能需求" in job_title:
        title = job_title
    else:
        title = f"{job_title}_技能需求词云"

    return _generate_job_wordcloud_internal(
        keywords=keywords,
        title=title,
        max_words=50,
        width=1000,
        height=700
    )


@tool
def generate_company_wordcloud(
    company_data: Optional[List[Dict[str, int]]] = None,
    industry: str = "互联网"
) -> str:
    """
    生成招聘公司词云图

    Args:
        company_data: 公司数据，格式如[{"name": "字节跳动", "count": 120}, {"name": "腾讯", "count": 110}]
        industry: 行业名称

    Returns:
        包含词云文件路径和文本描述的字符串
    """
    if not company_data:
        # 使用示例数据
        company_data = [
            {"name": "字节跳动", "count": 120},
            {"name": "腾讯", "count": 110},
            {"name": "阿里巴巴", "count": 105},
            {"name": "美团", "count": 95},
            {"name": "京东", "count": 90},
            {"name": "百度", "count": 85},
            {"name": "小米", "count": 80},
            {"name": "华为", "count": 75},
            {"name": "网易", "count": 70},
            {"name": "拼多多", "count": 65},
            {"name": "滴滴", "count": 60},
            {"name": "快手", "count": 55},
            {"name": "B站", "count": 50},
            {"name": "小红书", "count": 45},
            {"name": "蚂蚁集团", "count": 40}
        ]

    # 转换为关键词格式
    keywords = [{"word": item['name'], "weight": item['count']} for item in company_data]

    # 生成标题
    title = f"{industry}行业_招聘公司热度词云"
    return _generate_job_wordcloud_internal(
        keywords=keywords,
        title=title,
        max_words=30,
        width=1000,
        height=700
    )
