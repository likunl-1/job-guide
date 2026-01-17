"""
测试HTML报告生成工具的Markdown渲染功能
"""

import sys
import os

# 添加项目根目录到Python路径
workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from src.tools.html_report_tool import generate_html_report

# 获取工具的实际函数（去掉tool装饰器）
html_report_func = generate_html_report.func

# 准备测试数据
user_profile = {
    "name": "李同学",
    "education": "211财经院校 金融学院 硕士在读",
    "major": "金融学",
    "grade": "前30%",
    "interests": "就业vs读博选择",
    "skills": ["Python", "金融学", "统计学"],
    "expectations": "稳定工作，薪资适中"
}

# 使用Markdown格式的测试内容
employment_analysis = """
## 当前就业市场形势

### 整体趋势
- 金融行业竞争激烈，但仍有大量机会
- 银行等传统金融机构招聘稳定
- 金融科技新兴领域人才需求旺盛

### 不同方向的就业情况

**1. 商业银行**
- 招聘规模大，机会多
- 工作相对稳定
- 薪资水平适中

**2. 券商投行**
- 竞争最为激烈
- 薪资水平较高
- 工作强度大

**3. 企业财务**
- 需求稳定
- 工作生活平衡较好
- 发展路径清晰

> 关键洞察：根据你的特点，商业银行和企业财务是最适合的选择。
"""

recommendations = """
## 个性化建议

### 短期建议（6个月内）

1. **技能提升**
   - 深入学习Excel高级功能
   - 完成Python数据分析项目
   - 考取CFA一级或FRM一级

2. **实践经历**
   - 寻找银行或企业财务实习
   - 参加相关竞赛
   - 完善简历

### 中长期建议（1-2年）

**职业发展方向**
- 优先考虑商业银行系统
- 备选企业财务岗位
- 避免投行等高压岗位

**技能规划**
| 优先级 | 技能 | 时间投入 |
|--------|------|----------|
| 高 | 数据分析 | 3个月 |
| 高 | 财务分析 | 2个月 |
| 中 | 量化建模 | 1个月 |
| 低 | 学术研究 | 不建议 |

### 避坑指南

⚠️ **不建议**：
- 不要盲目追求高薪高风险岗位
- 不要在不感兴趣的学术方向投入过多
- 不要忽视实习的重要性
"""

action_plan = """
## 具体行动计划

### 第一阶段：研一下学期（3-6月）

**目标确定期**
- [x] 明确商业银行为主要目标方向
- [x] 制定学习计划
- [ ] 完成Excel高级功能学习
- [ ] 完成至少2个财务分析项目

**技能强化**
```python
# 学习计划示例
skills_to_learn = {
    "Excel高级": "VLOOKUP, PivotTable, 宏",
    "Python数据分析": "Pandas, Matplotlib, NumPy",
    "财务报表": "三张核心报表分析"
}
```

### 第二阶段：暑期（7-8月）

**实习实战**
- 寻找银行实习机会
- 积累实际工作经验
- 学习职场沟通技巧

### 第三阶段：研二上学期（9-12月）

**简历准备**
- 完善个人简历
- 突出实习和项目经验
- 准备面试常见问题

**秋招准备**
- 关注各大银行招聘信息
- 参加校园招聘宣讲会
- 开始网申投递

### 第四阶段：研二下学期（1-6月）

**冲刺阶段**
- 大规模投递简历
- 参加面试
- 收集Offer并对比
- 确定最终去向

---

**重要提醒**：
1. 每个阶段都要设定明确目标
2. 定期回顾和调整计划
3. 保持积极心态，不要焦虑
"""

# 转换为JSON字符串
import json
user_profile_json = json.dumps(user_profile)

# 调用工具生成报告
result = html_report_func(
    user_profile=user_profile_json,
    employment_analysis=employment_analysis,
    recommendations=recommendations,
    action_plan=action_plan,
    report_type="confused",
    output_filename="test_markdown_rendering.html"
)

print(result)
print("\n✅ 测试完成！请检查生成的报告文件，查看Markdown格式是否正确渲染。")
