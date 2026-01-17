"""
测试HTML报告生成功能
"""

import os
import sys

# 添加src目录到路径
workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
src_path = os.path.join(workspace_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from tools.html_report_tool import generate_html_report
import json

def test_html_report_generation():
    """测试HTML报告生成功能"""
    
    print("=" * 60)
    print("开始测试HTML报告生成功能")
    print("=" * 60)
    
    # 准备测试数据
    user_profile = {
        "name": "某211财经院校研一学生",
        "education": "硕士在读",
        "major": "金融学",
        "grade": "前30%",
        "interests": "就业vs读博选择",
        "skills": ["Python", "金融学", "统计学", "会计学"],
        "expectations": "稳定工作，薪资适中，工作生活平衡"
    }
    
    employment_analysis = """
## 就业市场概况

根据最新市场数据分析，金融行业就业呈现以下特点：

### 行业趋势
1. **商业银行系统**：需求稳定，是金融专业毕业生的主要就业方向
2. **企业财务**：岗位数量多，竞争相对较小，适合追求稳定的学生
3. **券商投行**：薪资高但竞争激烈，适合能力强、目标明确的毕业生
4. **量化研究**：技术要求高，薪资水平居行业前列，但需要扎实的数理基础

### 薪资水平
- 商业银行：15-18k（起薪），3年后可达22-28k
- 企业财务：12-15k（起薪），3年后可达18-25k
- 券商投行：20-30k（起薪），3年后可达35-50k
- 量化研究：25-35k（起薪），3年后可达50k+

### 竞争程度
- 商业银行：中等竞争（成功率约65%）
- 企业财务：低竞争（成功率约75%）
- 券商投行：高竞争（成功率约30%）
- 量化研究：高竞争（成功率约20%）

### 安全性评估
从就业安全性和稳定性角度排序：
1. 商业银行系统（最安全）
2. 企业财务（较安全）
3. 券商投行（中等）
4. 量化研究（风险较高）
"""
    
    recommendations = """
## 个性化建议

### 方向推荐：商业银行系统

**推荐理由：**
- ✅ 与你的金融学背景高度匹配
- ✅ 工作稳定性高，符合你追求稳定的期望
- ✅ 薪资水平适中且福利完善
- ✅ 发展路径清晰，晋升机制透明
- ✅ 对量化能力要求不高，更适合你的技能组合

**适合岗位：**
- 商业银行管培生
- 风险管理岗
- 公司金融岗
- 投资银行部（轻量化）

### 备选方案：企业财务

**推荐理由：**
- ✅ 工作生活平衡度高
- ✅ 与你的会计学优势匹配
- ✅ 职业寿命长，年龄歧视较少
- ✅ 可向财务总监、CFO方向发展

**适合岗位：**
- 企业财务分析师
- 会计主管
- 财务经理助理
- 内部审计

### 就业vs读博建议

**强烈建议：直接就业**

**理由：**
1. 你对学术研究兴趣不大，读博会让你在3-5年内面临较大压力
2. 直接就业可以提前积累工作经验和财富
3. 你的能力在就业市场有足够的竞争力
4. 金融行业更注重实践经验而非学历

**数据支持：**
- 硕士毕业生平均起薪18-22k，工作3年后薪资可达25-30k
- 博士毕业生起薪25-35k，但延迟3-4年
- 从现金流角度，直接就业更优
"""
    
    action_plan = """
## 具体行动计划

### 研一下学期（3-6月）：目标明确 + 技能强化

**3-4月：确定目标方向**
- [ ] 深入了解商业银行系统各岗位的工作内容
- [ ] 确定目标银行（国有大行、股份制银行、城商行）
- [ ] 了解目标银行的招聘要求和流程

**4-6月：技能强化**
- [ ] 深入学习Excel高级功能（数据透视表、VBA）
- [ ] 学习Python数据分析库（pandas、numpy）
- [ ] 完成2-3个财务分析项目
- [ ] 准备银行业务基础知识考试

**暑期：实习积累**
- [ ] 寻找商业银行实习机会
- [ ] 如果找不到银行实习，可选择企业财务实习
- [ ] 积累实际工作经验，丰富简历

### 研二上学期（9-12月）：实习经历 + 简历准备

**9-11月：完成高质量实习**
- [ ] 完成至少1份相关实习（优先银行或企业财务）
- [ ] 争取获得实习证明或推荐信
- [ ] 学习职场沟通和团队协作

**11-12月：简历准备**
- [ ] 用STAR法则整理实习和项目经验
- [ ] 突出金融学、会计学优势
- [ ] 添加相关技能关键词
- [ ] 准备多版本简历（银行版、企业版）

**寒假：网申准备**
- [ ] 开始网申，关注各大银行的校招信息
- [ ] 参加校园招聘宣讲会
- [ ] 准备面试常见问题

### 研二下学期（2-6月）：秋招 + Offer选择

**2-4月：大规模投递**
- [ ] 投递目标银行（建议30-50份简历）
- [ ] 投递备选企业财务岗位（20-30份）
- [ ] 记录投递状态，建立Excel表格跟踪

**4-5月：面试准备与参加**
- [ ] 准备银行面试题（银行业务知识、时事政治）
- [ ] 准备行为面试题（自我介绍、职业规划）
- [ ] 参加面试，注意着装和礼仪

**6月：Offer选择**
- [ ] 收集收到的Offer
- [ ] 对比薪资、地点、发展空间、企业文化
- [ ] 做出最终决定，准备入职

### 持续优化

**技能提升：**
- 每周投入10-15小时学习Excel和Python
- 关注金融行业新闻和趋势
- 参加行业讲座和沙龙

**人脉建设：**
- 与同学、学长学姐保持联系
- 加入专业社群和论坛
- 参加校友活动

**心态调整：**
- 接受过程中的挫折和拒绝
- 保持积极乐观的心态
- 相信自己的选择和能力
"""
    
    # 模拟对话历史（简略版）
    chat_history = """
<div class="chat-message user">
  <div class="chat-avatar"><i class="fas fa-user"></i></div>
  <div class="chat-content">
    老师，我现在研一，真的很迷茫。不知道是应该直接就业，还是继续读博？
  </div>
</div>

<div class="chat-message ai">
  <div class="chat-avatar"><i class="fas fa-robot"></i></div>
  <div class="chat-content">
    我理解你的焦虑。这确实是一个重要的选择。为了给你最合适的建议，我想先了解你的情况。
  </div>
</div>

<div class="chat-message user">
  <div class="chat-avatar"><i class="fas fa-user"></i></div>
  <div class="chat-content">
    成绩中等偏上，大概前30%。对研究没什么特别兴趣，只是觉得读博可能更稳定。
  </div>
</div>

<div class="chat-message ai">
  <div class="chat-avatar"><i class="fas fa-robot"></i></div>
  <div class="chat-content">
    基于你的描述，我已经分析完成。让我为你生成一份完整的报告。
  </div>
</div>
"""
    
    print("\n1. 准备测试数据...")
    print(f"   - 用户画像: {user_profile.get('name')}")
    print(f"   - 报告类型: confused (迷茫型)")
    
    print("\n2. 调用HTML报告生成工具...")
    
    try:
        # 调用工具（LangChain工具通过invoke方法调用）
        result = generate_html_report.invoke({
            "user_profile": json.dumps(user_profile, ensure_ascii=False),
            "employment_analysis": employment_analysis,
            "recommendations": recommendations,
            "action_plan": action_plan,
            "chat_history": chat_history,
            "report_type": "confused",
            "output_filename": "test_employment_report.html"
        })
        
        print("\n3. 报告生成结果:")
        print(f"   {result}")
        
        # 验证文件是否存在
        file_path = result.split("文件路径：")[1].split("\n")[0]
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"\n4. 文件验证:")
            print(f"   ✅ 文件存在: {file_path}")
            print(f"   ✅ 文件大小: {file_size} bytes")
            
            # 读取文件内容，验证HTML结构
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n5. HTML结构验证:")
            if '<!DOCTYPE html>' in content:
                print("   ✅ DOCTYPE声明正确")
            if '<title>' in content:
                print("   ✅ 标题标签存在")
            if '迷茫学生职业规划报告' in content or '就业指导综合报告' in content:
                print("   ✅ 报告标题正确")
            if '用户画像' in content:
                print("   ✅ 用户画像部分存在")
            if '就业市场分析' in content:
                print("   ✅ 就业市场分析部分存在")
            if '个性化建议' in content:
                print("   ✅ 推荐建议部分存在")
            if '行动计划' in content:
                print("   ✅ 行动计划部分存在")
            
            print("\n" + "=" * 60)
            print("✅ HTML报告生成功能测试成功！")
            print("=" * 60)
            print(f"\n报告已保存到: {file_path}")
            print("你可以用浏览器打开这个文件查看效果。")
            
            return True
        else:
            print(f"\n❌ 错误：文件未生成")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误：生成报告时出现异常")
        print(f"   错误信息: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_html_report_generation()
    sys.exit(0 if success else 1)
