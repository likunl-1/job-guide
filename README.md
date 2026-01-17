# 第14组 - 就业指导AI Agent

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**基于大语言模型的智能就业分析系统**

[课程作业](#) • [快速运行](#快速运行) • [功能展示](#功能展示)

</div>

---

## 📖 项目简介

本项目是一个基于大语言模型（DeepSeek-v3）的智能就业指导助手，能够为大学生提供个性化的职业规划建议和就业市场分析。
[就业指导AI Agent详细介绍](assets/documents/introductions/就业指导ai-agent介绍报告.html)

### 核心价值
- 🎯 **个性化指导**：根据学生专业、兴趣、技能提供定制化职业规划
- 📊 **数据驱动**：基于真实就业市场数据进行分析
- 🤖 **智能交互**：通过自然语言对话获取就业建议
- 📈 **趋势洞察**：分析就业市场趋势和热门技能需求

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **智能问答** | 通过自然语言对话获取就业指导和建议 |
| **简历分析** | 上传简历，智能分析优缺点并提供优化建议 |
| **市场分析** | 分析就业市场趋势、薪资分布、热门职位 |
| **技能推荐** | 根据目标职位推荐需要掌握的技能 |
| **案例引导** | 基于历史成功案例提供参考和启发 |
| **招聘信息爬取** | 通过自然语言对话，自动爬取前程无忧真实招聘数据并保存为Excel |
| **可视化报告** | 生成包含图表和词云的精美HTML报告 |

---

## 🚀 快速运行

### 方式1：本地运行（推荐）

#### 前置要求
- Python 3.9 或更高版本
- pip 包管理器

#### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-username/jobsurfing.git
cd jobsurfing

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的 API Key

# 4. 启动服务
python src/main.py -m http -p 8000
```

#### 访问界面

服务启动后，在浏览器中打开：**http://localhost:8000**

### 方式2：Docker运行

```bash
# 1. 构建镜像
docker build -t jobsurfing .

# 2. 运行容器
docker run -d -p 8000:8000 --name jobsurfing jobsurfing

# 3. 访问
# 浏览器打开 http://localhost:8000
```

---

## 📂 项目结构

```
jobsurfing/
├── src/                          # 核心源代码
│   ├── agents/                   # Agent逻辑
│   │   └── agent.py             # 主Agent实现
│   ├── tools/                    # 工具集
│   │   ├── web_search_tool.py   # 联网搜索
│   │   ├── resume_reader_tool.py # 简历读取
│   │   ├── visualization_tool.py # 数据可视化
│   │   ├── wordcloud_tool.py    # 词云生成
│   │   ├── html_report_tool.py  # HTML报告生成
│   │   ├── recruitment_spider_51job.py # 前程无忧招聘爬虫
│   │   ├── citynum.py           # 城市代码映射
│   │   └── data_saver.py        # 数据保存工具
│   ├── utils/                    # 工具函数
│   ├── storage/                  # 存储层
│   └── main.py                   # 程序入口
│
├── config/                       # 配置文件
│   └── agent_llm_config.json    # Agent配置
│
├── web/                          # Web前端
│   ├── index.html               # 主页
│   ├── app.js                   # 前端逻辑
│   └── style.css                # 样式文件
│
├── assets/                       # 资源文件
│   ├── charts/                  # 生成的图表
│   ├── reports/                 # 生成的报告
│   ├── jobs_data/               # 爬取的招聘数据
│   ├── resumes/                 # 简历文件
│   ├── documents/               # 文档资源
│   └── presentations/           # 演示材料
│       └── videos/intro/        # 项目介绍视频
│
├── docs/                         # 文档
│   └── quick-start.md           # 快速开始指南
│
├── tests/                        # 测试文件
├── requirements.txt              # Python依赖
└── README.md                     # 项目说明
```

---

## 🎬 功能展示

### 项目介绍视频
- [项目演示视频](assets/presentations/videos/intro/project-introduction.mov) ⭐
- 注意：视频文件较大，无法在线查看，需下载查看

### 招聘信息爬取
使用深层模式搜索时，可通过自然语言对话，自动爬取前程无忧真实招聘数据：

**示例对话**：
- 用户：帮我爬取北京的Python工程师职位
- Agent：好的，我正在为您爬取北京地区的Python工程师职位信息...
- 结果：自动保存为Excel文件到 `assets/jobs_data/` 目录

**数据字段**：
- 职位名称、公司名称、薪资范围、工作地点
- 职位描述、发布时间、公司规模等

### 案例报告
| 报告名称 | 说明 |
|---------|------|
| [迷茫学生问答报告](assets/reports/迷茫学生问答报告.html) | 学生职业规划案例 |
| [金融市场报告](assets/reports/金融市场报告.html) | 行业分析案例 |
| [李小硕就业报告](assets/reports/li_xiaoshuo_employment_report.html) | 个人就业分析案例 |

### 项目介绍文档
- [就业指导AI Agent详细介绍](assets/documents/introductions/就业指导ai-agent介绍报告.html)
- [团队贡献说明](assets/documents/team/team-contribution.html)
- [历史经济案例](assets/documents/cases/historical_economic_cases.md)

---

## 🛠️ 技术栈

### 核心技术
- **大语言模型**：DeepSeek-v3 / 豆包
- **Agent框架**：LangGraph + LangChain
- **后端框架**：FastAPI
- **前端技术**：HTML5 + JavaScript + CSS3

### 数据处理
- **数据可视化**：ECharts
- **词云生成**：WordCloud2
- **文档处理**：Python-docx, PyPDF2
- **数据爬取**：requests, BeautifulSoup4
- **数据存储**：pandas, openpyxl

### 存储
- **对象存储**：S3兼容存储
- **数据库**：PostgreSQL

---

## 📚 参考文献

1. LangGraph官方文档: https://langchain-ai.github.io/langgraph/
2. LangChain官方文档: https://python.langchain.com/
3. DeepSeek API文档: https://platform.deepseek.com/
4. ECharts文档: https://echarts.apache.org/

---

## 📝 课程信息

- **课程名称**：人工智能金融
- **学期**：2025-2026学年第一学期
- **小组编号**：第14组
- **小组成员**：刘立坤，王陈丽泰

---

## 📧 联系方式

如有问题，请联系：15855189065@163.com

---

## 📄 许可证

MIT License
