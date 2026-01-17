import os
import json
import sys
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from coze_coding_utils.runtime_ctx.context import default_headers

# 添加src目录到sys.path以便导入utils
workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
src_path = os.path.join(workspace_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from utils.helper import graph_helper

# 导入工具
from tools.web_search_tool import search_employment_market, get_employment_trend
from tools.user_profile_tool import analyze_user_profile, generate_personalized_advice
# 新增多模式搜索工具
from tools.multi_mode_search import search_employment_market_v2
# 新增：读取八爪鱼采集的数据
from tools.read_jobs_data import read_local_jobs, list_available_jobs
# 新增：简历文件读取工具（支持Word/PDF）
from tools.resume_reader_tool import read_resume_file, list_resume_files
# 新增：数据可视化工具
from tools.visualization_tool import (
    generate_salary_distribution_chart,
    generate_trend_chart,
    generate_skill_requirements_chart,
    generate_multi_chart_report,
    list_generated_charts
)
# 新增：词云生成工具
from tools.wordcloud_tool import (
    generate_job_wordcloud,
    generate_skill_wordcloud,
    generate_company_wordcloud
)
# 新增：HTML报告生成工具
from tools.html_report_tool import generate_html_report
# 新增：前程无忧招聘信息爬虫工具
from tools.recruitment_spider_51job import search_51job

LLM_CONFIG = "config/agent_llm_config.json"

in_memory_checkpointer = None

# 开发环境默认使用内存记忆, 生产环境默认无记忆
if graph_helper.is_dev_env():
    in_memory_checkpointer = MemorySaver()

def build_agent(ctx=None):
    """
    构建并返回就业指导Agent。
    
    Args:
        ctx: 上下文对象
        
    Returns:
        LangChain Agent实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    # 创建LLM实例
    llm = ChatOpenAI(
        model=cfg['config'].get("model", "doubao-seed-1-6-251015"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 准备工具列表
    tools = [
        search_employment_market,  # 保留旧版本工具（向后兼容）
        get_employment_trend,
        analyze_user_profile,
        generate_personalized_advice,
        search_employment_market_v2,  # 新增多模式搜索工具
        read_local_jobs,  # 新增：读取本地招聘数据（八爪鱼采集）
        list_available_jobs,  # 新增：列出可用的招聘数据文件
        read_resume_file,  # 新增：读取简历文件（支持Word/PDF/TXT/MD）
        list_resume_files,  # 新增：列出简历文件
        # 新增：数据可视化工具
        generate_salary_distribution_chart,  # 生成薪资分布图
        generate_trend_chart,  # 生成趋势图
        generate_skill_requirements_chart,  # 生成技能需求图
        generate_multi_chart_report,  # 生成综合分析报告
        list_generated_charts,  # 列出已生成的图表
        # 新增：词云生成工具
        generate_job_wordcloud,  # 生成就业市场词云
        generate_skill_wordcloud,  # 生成技能需求词云
        generate_company_wordcloud,  # 生成招聘公司词云
        # 新增：HTML报告生成工具
        generate_html_report,  # 生成完整的HTML报告
        # 新增：前程无忧招聘信息爬虫工具
        search_51job  # 从前程无忧爬取招聘信息
    ]
    
    # 创建Agent
    global in_memory_checkpointer
    agent = create_agent(
        model=llm,
        system_prompt=cfg.get("sp", ""),
        tools=tools,
        checkpointer=in_memory_checkpointer
    )
    
    return agent