#!/bin/bash

# JobSurfing 快速部署脚本
# 支持本地运行、Railway部署、Docker部署

set -e

echo "================================================"
echo "    JobSurfing AI Agent - 快速部署脚本"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示菜单
show_menu() {
    echo "请选择部署方式："
    echo "1) 本地运行（推荐开发者）"
    echo "2) Docker运行"
    echo "3) 部署到Railway（推荐生产环境）"
    echo "4) 临时分享（ngrok）"
    echo "5) 查看部署指南"
    echo "6) 退出"
    echo ""
    read -p "请输入选项 [1-6]: " choice
}

# 本地运行
deploy_local() {
    echo -e "${GREEN}[1/3] 检查Python环境...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误：未找到Python3，请先安装Python3.9+${NC}"
        exit 1
    fi
    
    python_version=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Python版本: $python_version${NC}"
    
    echo ""
    echo -e "${GREEN}[2/3] 安装依赖...${NC}"
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}错误：未找到requirements.txt${NC}"
        exit 1
    fi
    
    pip3 install -r requirements.txt
    
    echo ""
    echo -e "${GREEN}[3/3] 配置环境变量...${NC}"
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${YELLOW}已创建.env文件，请编辑.env配置API Key${NC}"
            echo -e "${YELLOW}需要配置的环境变量：${NC}"
            echo "  - COZE_WORKLOAD_IDENTITY_API_KEY"
            echo "  - COZE_INTEGRATION_MODEL_BASE_URL"
            read -p "按Enter继续..."
        else
            echo -e "${YELLOW}未找到.env.example，跳过环境变量配置${NC}"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}启动服务...${NC}"
    python3 src/main.py -m http -p 8000
}

# Docker运行
deploy_docker() {
    echo -e "${GREEN}[1/3] 检查Docker环境...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误：未找到Docker${NC}"
        echo -e "${YELLOW}请访问 https://docs.docker.com/get-docker/ 安装Docker${NC}"
        exit 1
    fi
    
    docker_version=$(docker --version)
    echo -e "${GREEN}✓ $docker_version${NC}"
    
    echo ""
    echo -e "${GREEN}[2/3] 构建Docker镜像...${NC}"
    docker build -t jobsurfing .
    
    echo ""
    echo -e "${GREEN}[3/3] 启动容器...${NC}"
    
    # 检查.env文件
    if [ -f ".env" ]; then
        echo -e "${GREEN}使用.env文件配置环境变量${NC}"
        docker run -d -p 8000:8000 --name jobsurfing --env-file .env jobsurfing
    else
        echo -e "${YELLOW}未找到.env文件，使用默认配置${NC}"
        docker run -d -p 8000:8000 --name jobsurfing jobsurfing
    fi
    
    echo ""
    echo -e "${GREEN}✓ 容器已启动！${NC}"
    echo -e "${GREEN}访问地址：http://localhost:8000${NC}"
    echo ""
    echo "常用命令："
    echo "  查看日志: docker logs -f jobsurfing"
    echo "  停止容器: docker stop jobsurfing"
    echo "  启动容器: docker start jobsurfing"
    echo "  删除容器: docker rm -f jobsurfing"
}

# 部署到Railway
deploy_railway() {
    echo -e "${GREEN}Railway部署指南${NC}"
    echo ""
    echo "前提条件："
    echo "  1) GitHub账号"
    echo "  2) Railway账号"
    echo ""
    echo "步骤："
    echo "  1) 初始化Git仓库"
    echo "  2) 推送到GitHub"
    echo "  3) 在Railway上部署"
    echo ""
    
    read -p "是否初始化Git仓库？[y/n] " init_git
    if [ "$init_git" = "y" ] || [ "$init_git" = "Y" ]; then
        if [ -d ".git" ]; then
            echo -e "${YELLOW}Git仓库已存在${NC}"
        else
            git init
            echo -e "${GREEN}✓ Git仓库已初始化${NC}"
        fi
        
        git add .
        
        read -p "输入Git commit信息 (默认: Initial commit): " commit_msg
        commit_msg=${commit_msg:-"Initial commit"}
        
        git commit -m "$commit_msg"
        echo -e "${GREEN}✓ 代码已提交${NC}"
        
        read -p "输入GitHub仓库地址 (如: https://github.com/username/jobsurfing.git): " git_url
        if [ -n "$git_url" ]; then
            git remote add origin $git_url
            git branch -M main
            git push -u origin main
            echo -e "${GREEN}✓ 代码已推送到GitHub${NC}"
        fi
    fi
    
    echo ""
    echo "下一步："
    echo "  1) 访问 https://railway.app"
    echo "  2) 使用GitHub登录"
    echo "  3) 点击 'New Project' → 'Deploy from GitHub repo'"
    echo "  4) 选择jobsurfing仓库"
    echo "  5) 点击 'Deploy Now'"
    echo "  6) 配置环境变量（COZE_WORKLOAD_IDENTITY_API_KEY等）"
    echo ""
    echo "详细文档请查看：docs/快速部署指南.md"
}

# 临时分享
share_temp() {
    echo -e "${GREEN}临时分享（使用ngrok）${NC}"
    echo ""
    
    if ! command -v ngrok &> /dev/null; then
        echo -e "${YELLOW}未找到ngrok${NC}"
        echo -e "${YELLOW}请访问 https://ngrok.com 下载安装ngrok${NC}"
        echo ""
        read -p "是否继续？[y/n] " continue
        if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
            exit 0
        fi
    fi
    
    echo "启动本地服务..."
    python3 src/main.py -m http -p 8000 &
    SERVER_PID=$!
    
    sleep 3
    
    echo "启动ngrok..."
    echo -e "${GREEN}复制下面的URL分享给其他人：${NC}"
    echo ""
    
    ngrok http 8000
    
    # 当ngrok停止时，也停止本地服务
    kill $SERVER_PID 2>/dev/null
}

# 查看部署指南
show_guide() {
    if [ -f "docs/快速部署指南.md" ]; then
        cat docs/快速部署指南.md
    else
        echo -e "${RED}未找到部署指南文档${NC}"
    fi
}

# 主循环
while true; do
    show_menu
    
    case $choice in
        1)
            deploy_local
            break
            ;;
        2)
            deploy_docker
            break
            ;;
        3)
            deploy_railway
            break
            ;;
        4)
            share_temp
            break
            ;;
        5)
            show_guide
            ;;
        6)
            echo "退出"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项，请重新选择${NC}"
            ;;
    esac
done
