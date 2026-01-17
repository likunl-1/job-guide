"""
读取八爪鱼采集的招聘数据工具

用于读取本地Excel/CSV格式的招聘数据，让Agent能够分析爬取的数据
"""

import os
import pandas as pd
from langchain.tools import tool
from typing import Optional


@tool
def read_local_jobs(
    keyword: str,
    file_type: str = "excel",
    max_results: int = 20
) -> str:
    """
    读取八爪鱼采集的本地招聘数据

    Args:
        keyword: 搜索关键词，用于匹配文件名（如"前端开发"）
        file_type: 文件类型，支持"excel"或"csv"
        max_results: 返回的最大结果数量

    Returns:
        招聘数据字符串，包含职位信息

    Examples:
        >>> read_local_jobs("前端开发")
        >>> read_local_jobs("Python", "csv", 10)
    """
    # 构建文件路径
    jobs_data_dir = "assets/jobs_data"

    if file_type == "excel":
        file_path = os.path.join(jobs_data_dir, f"{keyword}_招聘数据.xlsx")
    elif file_type == "csv":
        file_path = os.path.join(jobs_data_dir, f"{keyword}_招聘数据.csv")
    else:
        return f"不支持的文件类型：{file_type}，请选择 'excel' 或 'csv'"

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return (
            f"⚠️ 未找到 '{keyword}' 的招聘数据文件。\n\n"
            f"请确保：\n"
            f"1. 已使用八爪鱼采集了相关数据\n"
            f"2. 文件已保存到：{jobs_data_dir}/\n"
            f"3. 文件名格式正确：{keyword}_招聘数据.xlsx\n\n"
            f"可用的关键词示例：前端开发、Python、Java、数据分析等"
        )

    try:
        # 读取文件
        if file_type == "excel":
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        # 检查数据是否为空
        if len(df) == 0:
            return f"文件 '{file_path}' 中没有数据，请检查采集是否成功"

        # 限制返回结果数量
        df = df.head(max_results)

        # 构建返回结果
        result = f"## 📊 找到 {len(df)} 个相关职位\n\n"
        result += f"**数据来源**：八爪鱼采集的本地数据\n"
        result += f"**搜索关键词**：{keyword}\n"
        result += f"**文件路径**：{file_path}\n\n"
        result += "---\n\n"

        # 列出所有职位
        for idx, row in df.iterrows():
            idx_num = int(idx) + 1  # 转换为整数避免类型错误
            result += f"### {idx_num}. {row.get('职位名称', '未知职位')}\n\n"

            # 提取各个字段（根据实际列名调整）
            job_fields = [
                ('公司名称', 'company'),
                ('薪资', 'salary'),
                ('地点', 'location'),
                ('经验要求', 'experience'),
                ('学历要求', 'education'),
                ('发布时间', 'publish_time')
            ]

            for display_name, field_key in job_fields:
                # 尝试多种可能的列名
                value = None
                possible_keys = [display_name, field_key]

                for key in possible_keys:
                    if key in row:
                        value = row[key]
                        break

                # 检查值是否存在且不为 NaN
                if value is not None:
                    # 检查是否为 NaN（使用数学检查）
                    is_valid = True
                    try:
                        # 检查是否为 NaN（对于 float 类型）
                        if isinstance(value, float):
                            # NaN 是唯一不等于自身的值
                            if value != value:
                                is_valid = False
                    except:
                        pass
                    if is_valid:
                        result += f"- **{display_name}**：{value}\n"

            result += "\n"

        # 添加数据统计
        result += "---\n\n"
        result += "### 📈 数据统计\n\n"

        # 尝试统计薪资信息
        salary_col = None
        for col in ['薪资', 'salary', '薪酬']:
            if col in df.columns:
                salary_col = col
                break

        if salary_col:
            result += f"共采集到 {len(df)} 个职位\n"
            result += "以上是最新采集的招聘数据，您可以根据这些信息分析市场情况。\n"

        return result

    except Exception as e:
        return f"❌ 读取数据时出错：{str(e)}\n\n请检查文件格式是否正确，或联系技术支持。"


@tool
def list_available_jobs() -> str:
    """
    列出所有可用的招聘数据文件

    Returns:
        可用的招聘数据文件列表
    """
    jobs_data_dir = "assets/jobs_data"

    # 检查目录是否存在
    if not os.path.exists(jobs_data_dir):
        return (
            f"⚠️ 数据目录不存在：{jobs_data_dir}\n\n"
            f"请先创建该目录，并将八爪鱼采集的数据文件放入其中。"
        )

    # 获取所有Excel和CSV文件
    files = []
    for filename in os.listdir(jobs_data_dir):
        if filename.endswith(('.xlsx', '.xls', '.csv')):
            files.append(filename)

    if not files:
        return (
            f"⚠️ 目录 '{jobs_data_dir}' 中没有数据文件。\n\n"
            f"请使用八爪鱼采集招聘数据，并保存到此目录。"
        )

    # 构建结果
    result = f"## 📁 可用的招聘数据文件\n\n"
    result += f"共找到 {len(files)} 个文件：\n\n"

    for filename in files:
        # 提取关键词
        keyword = filename.replace('_招聘数据.xlsx', '').replace('_招聘数据.csv', '')
        result += f"- **{filename}**\n"
        result += f"  - 关键词：{keyword}\n"
        result += f"  - 查询命令：`read_local_jobs(\"{keyword}\")`\n\n"

    return result
