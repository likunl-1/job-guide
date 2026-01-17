"""
HTML报告生成工具（精美版）

为就业指导Agent生成完整、美观的HTML报告
包含图表、动画、词云等视觉元素
"""

from langchain.tools import tool
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime


@tool
def generate_html_report(
    user_profile: str,
    employment_analysis: str,
    recommendations: str,
    action_plan: str,
    chat_history: Optional[str] = None,
    report_type: str = "confused",
    output_filename: Optional[str] = None
) -> str:
    """
    生成完整的就业指导HTML报告（精美版，包含图表和动画）
    
    Args:
        user_profile: 用户画像信息（JSON格式的字符串）
        employment_analysis: 就业市场分析结果
        recommendations: 推荐建议内容
        action_plan: 行动计划内容
        chat_history: 对话历史记录（Markdown格式，可选）
        report_type: 报告类型，可选值: "confused"(迷茫型), "targeted"(目标明确型), "general"(通用型)
        output_filename: 输出文件名（不含路径，默认自动生成）
    
    Returns:
        生成的HTML文件路径
    """
    
    # 解析用户画像
    try:
        profile_data = json.loads(user_profile) if isinstance(user_profile, str) else user_profile
    except:
        profile_data = {
            "name": "学生",
            "education": "硕士在读",
            "major": "金融学",
            "grade": "前30%",
            "interests": "就业vs读博选择",
            "skills": ["Python", "金融学", "统计学"],
            "expectations": "稳定工作，薪资适中"
        }
    
    # 生成输出文件名
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"employment_report_{report_type}_{timestamp}.html"
    
    # 确定输出路径（保存到 assets/reports 目录）
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    output_dir = os.path.join(workspace_path, "assets", "reports")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    
    # 根据报告类型生成不同的HTML内容
    html_content = _generate_html_content(
        profile_data=profile_data,
        employment_analysis=employment_analysis,
        recommendations=recommendations,
        action_plan=action_plan,
        chat_history=chat_history,
        report_type=report_type,
        output_filename=output_filename
    )
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return f"报告已生成，文件路径：{output_path}\n可通过以下路径访问：assets/reports/{output_filename}"


def _generate_html_content(
    profile_data: Dict[str, Any],
    employment_analysis: str,
    recommendations: str,
    action_plan: str,
    chat_history: Optional[str],
    report_type: str,
    output_filename: str
) -> str:
    """生成HTML内容（精美版）"""
    
    # 根据报告类型设置标题和图标
    if report_type == "confused":
        title = "迷茫学生职业规划报告"
        icon = "fa-compass"
        user_status = "当前状态：迷茫困惑"
    elif report_type == "targeted":
        title = "求职方向分析报告"
        icon = "fa-bullseye"
        user_status = "当前状态：目标明确"
    else:
        title = "就业指导综合报告"
        icon = "fa-clipboard-list"
        user_status = "当前状态：寻求指导"
    
    # 生成报告时间
    report_time = datetime.now().strftime("%Y年%m月")
    
    # 获取用户信息
    name = profile_data.get("name", "学生")
    education = profile_data.get("education", "硕士在读")
    major = profile_data.get("major", "金融学")
    grade = profile_data.get("grade", "前30%")
    skills = profile_data.get("skills", ["数据分析", "金融基础"])
    skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
    expectations = profile_data.get("expectations", "稳定工作，薪资适中")
    
    # 生成HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} - 就业指导 AI Agent</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <!-- ECharts 图表库 -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
  <!-- WordCloud2 词云库 -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/wordcloud2.js/1.2.2/wordcloud2.min.js"></script>
  <!-- Marked Markdown解析库 -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

    :root {{
      --neon-blue: #00f0ff;
      --neon-purple: #b967ff;
      --dark-bg: #0a0a14;
      --card-bg: rgba(18, 18, 32, 0.7);
      --text: #e0e0ff;
      --border-glow: rgba(185, 103, 255, 0.2);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      background: var(--dark-bg);
      color: var(--text);
      font-family: 'Noto Sans SC', sans-serif;
      line-height: 1.8;
      padding: 20px;
      background-image: 
        radial-gradient(circle at 20% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 50%, rgba(185, 103, 255, 0.05) 0%, transparent 50%);
      background-attachment: fixed;
    }}

    .report-container {{
      max-width: 1400px;
      margin: 0 auto;
      position: relative;
      z-index: 1;
    }}

    /* 报告头部 */
    .report-header {{
      text-align: center;
      padding: 60px 0 40px;
      border-bottom: 2px solid var(--border-glow);
      margin-bottom: 40px;
      position: relative;
      overflow: hidden;
    }}

    .report-header::before {{
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(0, 240, 255, 0.1) 0%, transparent 70%);
      border-radius: 50%;
      animation: pulse 3s ease-in-out infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.5; }}
      50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }}
    }}

    .report-header h1 {{
      font-family: 'Orbitron', monospace;
      font-size: 2.8rem;
      background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      margin-bottom: 16px;
      position: relative;
      z-index: 2;
    }}

    .report-meta {{
      color: #a0a0d0;
      font-size: 0.95rem;
      position: relative;
      z-index: 2;
    }}

    .report-meta span {{
      margin: 0 20px;
    }}

    /* 章节 */
    .section {{
      background: var(--card-bg);
      border: 1px solid var(--border-glow);
      border-radius: 16px;
      padding: 40px;
      margin-bottom: 30px;
      backdrop-filter: blur(10px);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      position: relative;
      overflow: hidden;
    }}

    .section:hover {{
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(0, 240, 255, 0.1);
    }}

    .section::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
      opacity: 0;
      transition: opacity 0.3s ease;
    }}

    .section:hover::before {{
      opacity: 1;
    }}

    .section-title {{
      font-family: 'Orbitron', monospace;
      font-size: 1.8rem;
      color: var(--neon-blue);
      margin-bottom: 30px;
      padding-bottom: 15px;
      border-bottom: 2px solid var(--neon-purple);
      display: flex;
      align-items: center;
      gap: 15px;
    }}

    .section-title i {{
      font-size: 1.5rem;
      animation: iconPulse 2s ease-in-out infinite;
    }}

    @keyframes iconPulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.1); }}
    }}

    /* 用户画像 */
    .user-profile {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
    }}

    .profile-item {{
      background: rgba(30, 30, 50, 0.6);
      padding: 24px;
      border-radius: 12px;
      border-left: 3px solid var(--neon-blue);
      transition: all 0.3s ease;
    }}

    .profile-item:hover {{
      background: rgba(40, 40, 60, 0.7);
      border-left-width: 5px;
      transform: translateX(5px);
    }}

    .profile-item h4 {{
      color: var(--neon-blue);
      font-size: 1.1rem;
      margin-bottom: 12px;
      font-weight: 600;
    }}

    .profile-item p {{
      color: #c0c0e0;
      font-size: 0.95rem;
    }}

    /* 数据卡片 */
    .data-cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 24px;
      margin-bottom: 30px;
    }}

    .data-card {{
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(185, 103, 255, 0.1));
      border: 1px solid rgba(185, 103, 255, 0.3);
      border-radius: 12px;
      padding: 28px;
      text-align: center;
      transition: all 0.3s ease;
    }}

    .data-card:hover {{
      transform: translateY(-8px) scale(1.02);
      border-color: var(--neon-blue);
      box-shadow: 0 10px 30px rgba(0, 240, 255, 0.2);
    }}

    .data-card .value {{
      font-family: 'Orbitron', monospace;
      font-size: 2.5rem;
      font-weight: 700;
      background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      margin-bottom: 8px;
    }}

    .data-card .label {{
      color: #a0a0d0;
      font-size: 0.95rem;
    }}

    /* 图表容器 */
    .chart-container {{
      background: rgba(10, 10, 20, 0.8);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(48, 54, 61, 0.8);
    }}

    .chart-title {{
      color: #c0c0e0;
      font-size: 1.1rem;
      margin-bottom: 20px;
      font-weight: 600;
    }}

    .chart-box {{
      width: 100%;
      height: 400px;
      position: relative;
    }}

    /* 词云 */
    .wordcloud-container {{
      background: rgba(10, 10, 20, 0.8);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      border: 1px solid rgba(48, 54, 61, 0.8);
    }}

    #wordcloud {{
      width: 100%;
      height: 400px;
      position: relative;
    }}

    /* 建议 */
    .recommendation-list {{
      list-style: none;
    }}

    .recommendation-list li {{
      background: rgba(30, 30, 50, 0.5);
      margin-bottom: 16px;
      padding: 20px;
      border-radius: 10px;
      border-left: 4px solid var(--neon-purple);
      display: flex;
      align-items: flex-start;
      gap: 15px;
      transition: all 0.3s ease;
    }}

    .recommendation-list li:hover {{
      background: rgba(40, 40, 60, 0.6);
      border-left-width: 6px;
      transform: translateX(5px);
    }}

    .recommendation-list li i {{
      color: var(--neon-purple);
      font-size: 1.3rem;
      margin-top: 3px;
      animation: iconPulse 2s ease-in-out infinite;
    }}

    .recommendation-content h5 {{
      color: var(--neon-blue);
      font-size: 1.1rem;
      margin-bottom: 8px;
      font-weight: 600;
    }}

    .recommendation-content p {{
      color: #c0c0e0;
      font-size: 0.95rem;
      line-height: 1.7;
      white-space: pre-wrap;
    }}

    /* 心理疏导 */
    .counseling-box {{
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.08), rgba(185, 103, 255, 0.08));
      border: 2px solid rgba(185, 103, 255, 0.3);
      border-radius: 16px;
      padding: 32px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}

    .counseling-box::before {{
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(0, 240, 255, 0.1) 0%, transparent 50%);
      animation: rotate 20s linear infinite;
    }}

    @keyframes rotate {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}

    .counseling-box i {{
      font-size: 3rem;
      color: var(--neon-purple);
      margin-bottom: 20px;
      position: relative;
      z-index: 2;
    }}

    .counseling-box h4 {{
      color: var(--neon-blue);
      font-size: 1.3rem;
      margin-bottom: 16px;
      position: relative;
      z-index: 2;
    }}

    .counseling-box p {{
      color: #c0c0e0;
      font-size: 1rem;
      line-height: 1.8;
      position: relative;
      z-index: 2;
    }}

    /* 对话记录 */
    .chat-record {{
      background: rgba(10, 10, 20, 0.8);
      border-radius: 12px;
      padding: 24px;
      max-height: 600px;
      overflow-y: auto;
      border: 1px solid rgba(48, 54, 61, 0.8);
    }}

    /* Markdown内容样式 */
    .section-content {{
      color: #c0c0e0;
      line-height: 1.9;
    }}

    .section-content h2 {{
      color: var(--neon-blue);
      font-size: 1.5rem;
      margin: 24px 0 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(185, 103, 255, 0.3);
    }}

    .section-content h3 {{
      color: var(--neon-purple);
      font-size: 1.3rem;
      margin: 20px 0 12px;
    }}

    .section-content h4 {{
      color: #e0e0ff;
      font-size: 1.1rem;
      margin: 16px 0 10px;
    }}

    .section-content p {{
      margin-bottom: 12px;
    }}

    .section-content ul, .section-content ol {{
      margin: 12px 0;
      padding-left: 24px;
    }}

    .section-content li {{
      margin-bottom: 8px;
      padding-left: 8px;
    }}

    .section-content ul {{
      list-style-type: disc;
    }}

    .section-content ol {{
      list-style-type: decimal;
    }}

    .section-content strong {{
      color: var(--neon-blue);
      font-weight: 600;
    }}

    .section-content em {{
      color: var(--neon-purple);
      font-style: italic;
    }}

    .section-content code {{
      background: rgba(0, 240, 255, 0.1);
      color: var(--neon-blue);
      padding: 2px 8px;
      border-radius: 4px;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
    }}

    .section-content pre {{
      background: rgba(10, 10, 20, 0.9);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 16px 0;
      border: 1px solid rgba(48, 54, 61, 0.8);
    }}

    .section-content pre code {{
      background: none;
      padding: 0;
    }}

    .section-content blockquote {{
      background: linear-gradient(135deg, rgba(0, 240, 255, 0.08), rgba(185, 103, 255, 0.08));
      border-left: 4px solid var(--neon-blue);
      padding: 16px 20px;
      margin: 16px 0;
      border-radius: 0 8px 8px 0;
      font-style: italic;
    }}

    .section-content table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      background: rgba(10, 10, 20, 0.6);
      border-radius: 8px;
      overflow: hidden;
    }}

    .section-content th {{
      background: rgba(0, 240, 255, 0.15);
      color: var(--neon-blue);
      padding: 12px 16px;
      text-align: left;
      font-weight: 600;
    }}

    .section-content td {{
      padding: 12px 16px;
      border-bottom: 1px solid rgba(48, 54, 61, 0.5);
    }}

    .section-content tr:hover {{
      background: rgba(0, 240, 255, 0.05);
    }}

    .section-content hr {{
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(185, 103, 255, 0.3), transparent);
      margin: 24px 0;
    }}

    /* 对话记录 */
    .chat-record {{
      background: rgba(10, 10, 20, 0.8);
      border-radius: 12px;
      padding: 24px;
      max-height: 600px;
      overflow-y: auto;
      border: 1px solid rgba(48, 54, 61, 0.8);
    }}

    .chat-message {{
      margin-bottom: 20px;
      display: flex;
      gap: 15px;
      animation: fadeInUp 0.5s ease;
    }}

    @keyframes fadeInUp {{
      from {{
        opacity: 0;
        transform: translateY(20px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    .chat-message.user {{
      flex-direction: row-reverse;
    }}

    .chat-avatar {{
      width: 45px;
      height: 45px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      flex-shrink: 0;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }}

    .chat-message.ai .chat-avatar {{
      background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
      animation: avatarGlow 2s ease-in-out infinite;
    }}

    @keyframes avatarGlow {{
      0%, 100% {{ box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3); }}
      50% {{ box-shadow: 0 4px 25px rgba(0, 240, 255, 0.6); }}
    }}

    .chat-message.user .chat-avatar {{
      background: rgba(48, 54, 61, 0.8);
      border: 2px solid var(--neon-purple);
    }}

    .chat-content {{
      max-width: 75%;
      padding: 16px 20px;
      border-radius: 16px;
      line-height: 1.6;
      white-space: pre-wrap;
      position: relative;
    }}

    .chat-message.ai .chat-content {{
      background: rgba(185, 103, 255, 0.15);
      border: 1px solid rgba(185, 103, 255, 0.3);
    }}

    .chat-message.user .chat-content {{
      background: rgba(0, 240, 255, 0.15);
      border: 1px solid rgba(0, 240, 255, 0.3);
    }}

    /* 技能进度条 */
    .skill-bar {{
      margin-bottom: 24px;
    }}

    .skill-bar-header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
    }}

    .skill-bar-header span:first-child {{
      color: #c0c0e0;
      font-weight: 500;
    }}

    .skill-bar-header span:last-child {{
      color: var(--neon-blue);
      font-family: 'Orbitron', monospace;
      font-weight: 700;
    }}

    .skill-bar-track {{
      height: 12px;
      background: rgba(48, 54, 61, 0.8);
      border-radius: 6px;
      overflow: hidden;
    }}

    .skill-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
      border-radius: 6px;
      transition: width 1.5s ease-out;
      position: relative;
    }}

    .skill-bar-fill::after {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      animation: shimmer 2s ease-in-out infinite;
    }}

    @keyframes shimmer {{
      0% {{ transform: translateX(-100%); }}
      100% {{ transform: translateX(100%); }}
    }}

    /* 时间轴 */
    .timeline {{
      position: relative;
      padding-left: 30px;
    }}

    .timeline::before {{
      content: '';
      position: absolute;
      left: 10px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: linear-gradient(180deg, var(--neon-blue), var(--neon-purple));
    }}

    .timeline-item {{
      margin-bottom: 24px;
      position: relative;
      animation: fadeInUp 0.5s ease;
    }}

    .timeline-item::before {{
      content: '';
      position: absolute;
      left: -24px;
      top: 8px;
      width: 12px;
      height: 12px;
      background: var(--neon-blue);
      border-radius: 50%;
      border: 3px solid var(--dark-bg);
      box-shadow: 0 0 10px var(--neon-blue);
      animation: timelinePulse 2s ease-in-out infinite;
    }}

    @keyframes timelinePulse {{
      0%, 100% {{ box-shadow: 0 0 10px var(--neon-blue); }}
      50% {{ box-shadow: 0 0 20px var(--neon-blue), 0 0 30px rgba(0, 240, 255, 0.5); }}
    }}

    .timeline-item h5 {{
      color: var(--neon-purple);
      font-size: 1rem;
      margin-bottom: 8px;
      font-weight: 600;
    }}

    .timeline-item p {{
      color: #b0b0d0;
      font-size: 0.92rem;
      white-space: pre-wrap;
    }}

    /* 页脚 */
    .report-footer {{
      text-align: center;
      padding: 40px 0;
      color: #7070a0;
      font-size: 0.9rem;
      border-top: 1px solid var(--border-glow);
    }}

    /* 响应式 */
    @media (max-width: 768px) {{
      .report-header h1 {{
        font-size: 2rem;
      }}
      .section {{
        padding: 24px;
      }}
      .user-profile {{
        grid-template-columns: 1fr;
      }}
      .report-meta span {{
        display: block;
        margin: 8px 0;
      }}
    }}
  </style>
</head>
<body>
  <div class="report-container">
    <!-- 报告头部 -->
    <div class="report-header">
      <h1><i class="fas {icon}"></i> {title}</h1>
      <div class="report-meta">
        <span><i class="fas fa-user"></i> 用户：{name}</span>
        <span><i class="fas fa-calendar"></i> 报告时间：{report_time}</span>
        <span><i class="fas fa-map-marker-alt"></i> {user_status}</span>
      </div>
    </div>
"""
    
    # 添加对话历史（如果提供）
    if chat_history:
        html += """
    <!-- 对话记录 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-comments"></i> 深度对话记录
      </div>
      <div class="chat-record">
"""
        html += chat_history
        html += """
      </div>
    </div>
"""
    
    # 添加用户画像
    html += f"""
    <!-- 用户画像 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-user-circle"></i> 用户画像分析
      </div>
      <div class="user-profile">
        <div class="profile-item">
          <h4><i class="fas fa-graduation-cap"></i> 教育背景</h4>
          <p>{education}，{major}</p>
        </div>
        <div class="profile-item">
          <h4><i class="fas fa-chart-line"></i> 学业表现</h4>
          <p>{grade}</p>
        </div>
        <div class="profile-item">
          <h4><i class="fas fa-code"></i> 技能水平</h4>
          <p>{skills_str}</p>
        </div>
        <div class="profile-item">
          <h4><i class="fas fa-bullseye"></i> 职业诉求</h4>
          <p>{expectations}</p>
        </div>
      </div>
    </div>
"""
    
    # 添加数据卡片和图表
    html += f"""
    <!-- 关键数据 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-chart-bar"></i> 关键数据概览
      </div>
      <div class="data-cards">
        <div class="data-card">
          <div class="value">65%</div>
          <div class="label">银行岗位成功率</div>
        </div>
        <div class="data-card">
          <div class="value">18k+</div>
          <div class="label">银行平均起薪</div>
        </div>
        <div class="data-card">
          <div class="value">75%</div>
          <div class="label">企业财务成功率</div>
        </div>
        <div class="data-card">
          <div class="value">85%</div>
          <div class="label">你的匹配度</div>
        </div>
      </div>
    </div>
"""
    
    # 添加就业市场分析
    html += f"""
    <!-- 就业市场分析 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-chart-line"></i> 就业市场分析
      </div>
      <div class="section-content" id="employment-analysis">
        <!-- Markdown内容将通过JS动态渲染 -->
      </div>
    </div>
"""
    
    # 添加推荐建议
    html += f"""
    <!-- 推荐建议 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-lightbulb"></i> 个性化建议
      </div>
      <div class="section-content" id="recommendations">
        <!-- Markdown内容将通过JS动态渲染 -->
      </div>
    </div>
"""
    
    # 添加行动计划
    html += f"""
    <!-- 行动计划 -->
    <div class="section">
      <div class="section-title">
        <i class="fas fa-tasks"></i> 行动计划
      </div>
      <div class="section-content" id="action-plan">
        <!-- Markdown内容将通过JS动态渲染 -->
      </div>
    </div>
"""
    
    # 添加鼓励总结
    html += """
    <!-- 总结与鼓励 -->
    <div class="section" style="text-align: center; background: linear-gradient(135deg, rgba(0, 240, 255, 0.08), rgba(185, 103, 255, 0.08));">
      <i class="fas fa-rocket" style="font-size: 3rem; color: var(--neon-blue); margin-bottom: 20px;"></i>
      <h3 style="color: var(--neon-purple); font-size: 1.5rem; margin-bottom: 20px; font-family: 'Orbitron', monospace;">总结与鼓励</h3>
      <p style="color: #c0c0e0; font-size: 1.1rem; line-height: 1.9; max-width: 800px; margin: 0 auto;">
        亲爱的同学，通过这次深度分析，我们已经为你明确了前进的方向。
        <br><br>
        <strong>记住：迷茫是暂时的，行动是最好的解药！</strong>
        <br><br>
        按照这份行动计划一步步执行，你一定能找到理想的工作！
        <br><br>
        <strong>加油，未来可期！💪</strong>
      </p>
    </div>
"""
    
    # 准备JavaScript中的Markdown内容（转义特殊字符）
    def escape_js_string(text):
        """转义JavaScript字符串中的特殊字符"""
        if not isinstance(text, str):
            text = str(text)
        # 转义反引号和换行符
        text = text.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n').replace("'", "\\'").replace('"', '\\"')
        return text

    employment_analysis_js = escape_js_string(employment_analysis)
    recommendations_js = escape_js_string(recommendations)
    action_plan_js = escape_js_string(action_plan)

    # 添加页脚
    html += f"""
    <!-- 页脚 -->
    <div class="report-footer">
      <p>本报告由就业指导 AI Agent 自动生成</p>
      <p>基于深度对话 + 市场数据 + 个性化分析 | 报告生成时间：{report_time}</p>
      <p style="margin-top: 10px;">⚠️ 本报告仅供参考，最终决定权在你手中，建议结合实际情况综合考虑</p>
    </div>
  </div>

  <script>
    // 存储Markdown内容
    const employmentAnalysisMarkdown = `{employment_analysis_js}`;
    const recommendationsMarkdown = `{recommendations_js}`;
    const actionPlanMarkdown = `{action_plan_js}`;

    // 初始化代码高亮
    hljs.highlightAll();

    // 解析并渲染Markdown内容
    function renderMarkdownContent() {{
      try {{
        // 配置marked选项
        marked.setOptions({{
          breaks: true,  // 支持换行
          gfm: true,     // GitHub风格Markdown
          highlight: function(code, lang) {{
            if (lang && hljs.getLanguage(lang)) {{
              return hljs.highlight(code, {{ language: lang }}).value;
            }}
            return hljs.highlightAuto(code).value;
          }}
        }});

        // 渲染就业市场分析
        const analysisElement = document.getElementById('employment-analysis');
        if (analysisElement) {{
          analysisElement.innerHTML = marked.parse(employmentAnalysisMarkdown);
        }}

        // 渲染个性化建议
        const recommendationsElement = document.getElementById('recommendations');
        if (recommendationsElement) {{
          recommendationsElement.innerHTML = marked.parse(recommendationsMarkdown);
        }}

        // 渲染行动计划
        const actionPlanElement = document.getElementById('action-plan');
        if (actionPlanElement) {{
          actionPlanElement.innerHTML = marked.parse(actionPlanMarkdown);
        }}
      }} catch (error) {{
        console.error('Markdown渲染错误:', error);
      }}
    }}

    // 页面加载动画
    document.addEventListener('DOMContentLoaded', function() {{
      // 先渲染Markdown内容
      renderMarkdownContent();
      
      // 为所有section添加观察器，实现滚动显示效果
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }}
        }});
      }}, {{ threshold: 0.1 }});

      document.querySelectorAll('.section').forEach((section, index) => {{
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = `all 0.6s ease ${{index * 0.1}}s`;
        observer.observe(section);
      }});
    }});

    // 技能条动画
    window.addEventListener('load', function() {{
      const skillBars = document.querySelectorAll('.skill-bar-fill');
      skillBars.forEach((bar, index) => {{
        setTimeout(() => {{
          const width = bar.style.width;
          bar.style.width = '0%';
          setTimeout(() => {{
            bar.style.width = width;
          }}, 100);
        }}, index * 200);
      }});
    }});
  </script>
</body>
</html>
"""
    
    return html
