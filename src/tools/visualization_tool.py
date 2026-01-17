"""
就业市场可视化工具

提供就业市场数据的可视化功能，支持生成多种类型的图表：
- 薪资分布图
- 岗位需求趋势图
- 地区分布图
- 技能要求图
"""

import os
import json
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from langchain.tools import tool

# 配置中文字体支持 - 使用已安装的中文字体
# 优先使用 WenQuanYi Zen Hei，其次使用 Micro Hei
chinese_font = 'WenQuanYi Zen Hei'  # 文泉驿正黑
font_found = False

# 检查字体是否存在
available_fonts = set(f.name for f in fm.fontManager.ttflist)
if chinese_font in available_fonts:
    plt.rcParams['font.sans-serif'] = [chinese_font, 'WenQuanYi Micro Hei', 'DejaVu Sans']
    font_found = True
else:
    # 尝试其他中文字体
    for font_name in ['WenQuanYi Micro Hei', 'AR PL UMing CN', 'AR PL UKai CN']:
        if font_name in available_fonts:
            plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
            chinese_font = font_name
            font_found = True
            break
    
    if not font_found:
        print(f"⚠️ 警告：未找到中文字体，使用默认字体")
        print(f"可用的中文字体: {[f for f in available_fonts if 'WenQuanYi' in f or 'AR PL' in f or 'WQY' in f]}")
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置图表样式
try:
    plt.style.use('seaborn-v0_8')
except:
    # 如果seaborn-v0_8不可用，使用默认样式
    plt.style.use('default')


@tool
def generate_salary_distribution_chart(
    job_title: str,
    salary_ranges: Optional[List[str]] = None,
    counts: Optional[List[int]] = None,
    data_source: str = "search"
) -> str:
    """
    生成薪资分布图

    Args:
        job_title: 职位名称，如"前端开发工程师"、"数据分析师"
        salary_ranges: 薪资区间列表，如["0-10k", "10-20k", "20-30k", "30k+"]
        counts: 各区间的岗位数量，如[10, 25, 15, 5]
        data_source: 数据来源，可选"search"（搜索结果）或"local"（本地数据）

    Returns:
        包含图片路径和图表说明的字符串
    """
    try:
        # 创建输出目录
        output_dir = "assets/charts"
        os.makedirs(output_dir, exist_ok=True)

        # 如果没有提供数据，生成示例数据用于演示
        if salary_ranges is None or counts is None:
            salary_ranges = ["0-10k", "10-15k", "15-20k", "20-30k", "30k+"]
            counts = np.random.randint(5, 30, size=len(salary_ranges)).tolist()
            data_note = "（示例数据）"
        else:
            data_note = ""

        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 7))

        # 绘制柱状图
        bars = ax.bar(salary_ranges, counts, color='steelblue', edgecolor='navy', alpha=0.7)

        # 添加数值标签
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')

        # 设置图表标题和标签
        ax.set_xlabel('薪资区间', fontsize=12, fontweight='bold')
        ax.set_ylabel('岗位数量', fontsize=12, fontweight='bold')
        ax.set_title(f'{job_title} 薪资分布图 {data_note}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # 添加统计信息
        total_jobs = sum(counts)
        avg_salary_index = len(salary_ranges) // 2
        stats_text = f'总岗位数: {total_jobs} | 平均薪资区间: {salary_ranges[avg_salary_index]}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        # 保存图表
        filename = f"{job_title}_薪资分布.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        # 生成返回结果
        result = f"""
## 📊 薪资分布图已生成

**职位名称**：{job_title}
**数据来源**：{data_source}
**图表类型**：柱状图
**保存路径**：{filepath}

### 📈 数据概览
- 总岗位数：{total_jobs}
- 薪资区间：{salary_ranges[0]} 至 {salary_ranges[-1]}
- 主要集中区间：{salary_ranges[np.argmax(counts)]}

### 💡 分析建议
"""
        # 添加分析建议
        max_index = np.argmax(counts)
        result += f"- 该职位的主流薪资区间为 **{salary_ranges[max_index]}**，占所有岗位的 {counts[max_index]/total_jobs*100:.1f}%\n"
        result += f"- 建议求职者根据自身能力，目标定在 {salary_ranges[max_index]} 及以上区间\n"
        result += f"- 若想获得更高薪资（{salary_ranges[-1]}），建议提升核心技能和项目经验\n"

        return result

    except Exception as e:
        return f"❌ 生成薪资分布图失败：{str(e)}"


@tool
def generate_trend_chart(
    title: str,
    labels: List[str],
    values: List[float],
    chart_type: str = "line",
    unit: str = "岗位数"
) -> str:
    """
    生成趋势图（折线图或柱状图）

    Args:
        title: 图表标题，如"前端开发需求趋势"
        labels: X轴标签，如["1月", "2月", "3月", "4月", "5月", "6月"]
        values: Y轴数值，如[120, 150, 180, 200, 220, 250]
        chart_type: 图表类型，"line"（折线图）或"bar"（柱状图）
        unit: Y轴单位，如"岗位数"、"薪资(k)"

    Returns:
        包含图片路径和图表说明的字符串
    """
    try:
        # 创建输出目录
        output_dir = "assets/charts"
        os.makedirs(output_dir, exist_ok=True)

        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 7))

        if chart_type == "line":
            # 折线图
            ax.plot(labels, values, marker='o', linewidth=2, markersize=8,
                   color='#2E86AB', markerfacecolor='#A23B72')
            ax.fill_between(labels, values, alpha=0.3, color='#2E86AB')
        else:
            # 柱状图
            bars = ax.bar(labels, values, color='#F18F01', edgecolor='#C73E1D', alpha=0.8)
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value}', ha='center', va='bottom', fontsize=10)

        # 设置图表标题和标签
        ax.set_xlabel('时间', fontsize=12, fontweight='bold')
        ax.set_ylabel(unit, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # 添加趋势信息
        if len(values) >= 2:
            growth_rate = ((values[-1] - values[0]) / values[0]) * 100
            trend_text = f'增长趋势: {"上升" if growth_rate > 0 else "下降"} {abs(growth_rate):.1f}%'
            ax.text(0.02, 0.98, trend_text, transform=ax.transAxes,
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

        plt.tight_layout()

        # 保存图表
        filename = f"{title}.png".replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        # 生成返回结果
        result = f"""
## 📈 趋势图已生成

**图表标题**：{title}
**图表类型**：{"折线图" if chart_type == "line" else "柱状图"}
**数据点数**：{len(values)}
**保存路径**：{filepath}

### 📊 数据分析
"""
        # 添加趋势分析
        if len(values) >= 2:
            growth_rate = ((values[-1] - values[0]) / values[0]) * 100
            result += f"- 整体趋势：{'上升 📈' if growth_rate > 0 else '下降 📉'}\n"
            result += f"- 增长幅度：{abs(growth_rate):.1f}%\n"
            result += f"- 最低值：{min(values)} {unit} ({labels[values.index(min(values))]})\n"
            result += f"- 最高值：{max(values)} {unit} ({labels[values.index(max(values))]})\n"

        return result

    except Exception as e:
        return f"❌ 生成趋势图失败：{str(e)}"


@tool
def generate_skill_requirements_chart(
    skills: List[str],
    counts: List[int],
    chart_type: str = "horizontal_bar"
) -> str:
    """
    生成技能需求分布图

    Args:
        skills: 技能列表，如["Python", "JavaScript", "SQL", "Docker", "Git"]
        counts: 各技能的需求次数，如[25, 20, 18, 12, 10]
        chart_type: 图表类型，"horizontal_bar"（水平柱状图）或"pie"（饼图）

    Returns:
        包含图片路径和图表说明的字符串
    """
    try:
        # 创建输出目录
        output_dir = "assets/charts"
        os.makedirs(output_dir, exist_ok=True)

        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))

        if chart_type == "horizontal_bar":
            # 水平柱状图
            y_pos = np.arange(len(skills))
            cmap = plt.get_cmap('viridis')
            colors = cmap(np.linspace(0.3, 0.9, len(skills)))

            bars = ax.barh(y_pos, counts, color=colors, alpha=0.8)

            # 添加数值标签
            for i, (bar, count) in enumerate(zip(bars, counts)):
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                       f'{count}', ha='left', va='center', fontsize=10)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(skills, fontsize=11)
            ax.invert_yaxis()  # 最重要的技能在顶部
            ax.set_xlabel('需求次数', fontsize=12, fontweight='bold')

        else:
            # 饼图
            cmap = plt.get_cmap('Set3')
            colors = cmap(np.linspace(0, 1, len(skills)))
            wedges, texts, autotexts = ax.pie(counts, labels=skills, autopct='%1.1f%%',
                                             colors=colors, startangle=90,
                                             textprops={'fontsize': 10})

            # 美化文本
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

        ax.set_title('技能需求分布图', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        # 保存图表
        filename = f"技能需求分布_{'横向柱状图' if chart_type == 'horizontal_bar' else '饼图'}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        # 生成返回结果
        result = f"""
## 🎯 技能需求分布图已生成

**图表类型**：{"水平柱状图" if chart_type == "horizontal_bar" else "饼图"}
**技能数量**：{len(skills)}
**保存路径**：{filepath}

### 🔥 热门技能 TOP 5
"""

        # 排序并显示前5
        sorted_data = sorted(zip(skills, counts), key=lambda x: x[1], reverse=True)
        for i, (skill, count) in enumerate(sorted_data[:5]):
            result += f"{i+1}. **{skill}** - 出现 {count} 次\n"

        result += f"\n### 💡 学习建议\n"
        top_skill = sorted_data[0][0]
        result += f"- 优先掌握 **{top_skill}**，这是最热门的技能\n"
        result += f"- 前3名技能覆盖率超过 {(sorted_data[0][1] + sorted_data[1][1] + sorted_data[2][1])/sum(counts)*100:.0f}%，建议重点学习\n"

        return result

    except Exception as e:
        return f"❌ 生成技能需求图失败：{str(e)}"


@tool
def generate_multi_chart_report(
    job_title: str,
    salary_data: Optional[Dict[str, Any]] = None,
    trend_data: Optional[Dict[str, Any]] = None,
    skill_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    生成综合分析报告（包含多个图表）

    Args:
        job_title: 职位名称
        salary_data: 薪资数据，如{"ranges": ["0-10k", "10-20k"], "counts": [10, 20]}
        trend_data: 趋势数据，如{"labels": ["1月", "2月"], "values": [100, 120]}
        skill_data: 技能数据，如{"skills": ["Python", "JS"], "counts": [25, 20]}

    Returns:
        包含所有图表的综合报告
    """
    try:
        output_dir = "assets/charts"
        os.makedirs(output_dir, exist_ok=True)

        report_parts = []
        report_parts.append(f"# 📊 {job_title} 综合分析报告\n")

        # 如果没有提供数据，生成示例数据
        if salary_data is None and trend_data is None and skill_data is None:
            report_parts.append("> ⚠️ 未提供具体数据，使用示例数据生成演示图表\n\n")

        # 生成薪资分布图
        if salary_data is None:
            salary_ranges = ["0-10k", "10-15k", "15-20k", "20-30k", "30k+"]
            salary_counts = np.random.randint(5, 30, size=len(salary_ranges)).tolist()
            report_parts.append(generate_salary_distribution_chart(job_title, salary_ranges, salary_counts))
        else:
            report_parts.append(generate_salary_distribution_chart(
                job_title,
                salary_data.get("ranges"),
                salary_data.get("counts")
            ))

        report_parts.append("\n---\n\n")

        # 生成趋势图
        if trend_data is None:
            trend_labels = ["1月", "2月", "3月", "4月", "5月", "6月"]
            trend_values = np.cumsum(np.random.randint(10, 30, size=6)).tolist()
            report_parts.append(generate_trend_chart(f"{job_title}需求趋势", trend_labels, trend_values))
        else:
            report_parts.append(generate_trend_chart(
                f"{job_title}需求趋势",
                trend_data.get("labels"),
                trend_data.get("values")
            ))

        report_parts.append("\n---\n\n")

        # 生成技能需求图
        if skill_data is None:
            skill_names = ["Python", "JavaScript", "SQL", "Docker", "Git", "AWS", "React", "Linux"]
            skill_counts = np.random.randint(10, 40, size=len(skill_names)).tolist()
            report_parts.append(generate_skill_requirements_chart(skill_names, skill_counts))
        else:
            report_parts.append(generate_skill_requirements_chart(
                skill_data.get("skills"),
                skill_data.get("counts")
            ))

        return "".join(report_parts)

    except Exception as e:
        return f"❌ 生成综合分析报告失败：{str(e)}"


@tool
def list_generated_charts() -> str:
    """
    列出所有已生成的图表文件

    Returns:
        可用的图表文件列表
    """
    charts_dir = "assets/charts"

    if not os.path.exists(charts_dir):
        return f"⚠️ 图表目录不存在：{charts_dir}\n\n请先生成图表。"

    files = []
    for filename in os.listdir(charts_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            files.append(filename)

    if not files:
        return f"⚠️ 目录 '{charts_dir}' 中没有图表文件。\n\n请使用可视化工具生成图表。"

    result = f"## 📁 已生成的图表\n\n"
    result += f"共找到 {len(files)} 个图表文件：\n\n"

    for filename in sorted(files):
        filepath = os.path.join(charts_dir, filename)
        file_size = os.path.getsize(filepath)
        result += f"- **{filename}**\n"
        result += f"  - 路径：{filepath}\n"
        result += f"  - 大小：{file_size/1024:.1f} KB\n\n"

    return result
