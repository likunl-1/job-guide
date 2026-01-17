# 快速开始指南

本指南帮助您快速运行就业指导AI Agent演示。

---

## 🚀 方式1：本地运行（推荐）

### 前置要求
- Python 3.9 或更高版本
- pip 包管理器

### 快速启动（3步）

```bash
# 1. 进入项目目录
cd jobsurfing

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python src/main.py -m http -p 8000
```

### 访问界面

服务启动后，在浏览器中打开：**http://localhost:8000**

---

## 🐳 方式2：Docker运行

```bash
# 构建并运行
docker build -t jobsurfing .
docker run -d -p 8000:8000 --name jobsurfing jobsurfing

# 访问
浏览器打开 http://localhost:8000
```

---

## ✅ 快速测试

启动服务后，在Web界面中尝试以下功能：

**智能问答**
- "帮我分析金融专业的就业前景"
- "Python开发需要掌握哪些技能"

**简历分析**
- 上传简历文件，询问："分析我的简历，给出优化建议"

**市场分析**
- "分析数据分析师的薪资水平"
- "2025年热门技术岗位有哪些"

---

## 💡 常见问题

**Q: 启动失败？**
- 检查Python版本 >= 3.9
- 确保端口8000未被占用

**Q: 如何停止服务？**
- 按 `Ctrl + C` 停止

**Q: 更多功能？**
- 查看 [README.md](../README.md) 了解详细功能
