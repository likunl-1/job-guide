#!/bin/bash

# GitHub Token 推送脚本
# 使用方法：
# 1. 将你的 GitHub Token 设置为环境变量：export GITHUB_TOKEN="your_token_here"
# 2. 运行脚本：bash push_to_github.sh

if [ -z "$GITHUB_TOKEN" ]; then
    echo "错误：未设置 GITHUB_TOKEN 环境变量"
    echo ""
    echo "请先设置你的 GitHub Token："
    echo "  export GITHUB_TOKEN=\"your_token_here\""
    echo ""
    echo "然后重新运行此脚本。"
    exit 1
fi

echo "正在推送代码到 GitHub..."
echo "仓库地址：https://github.com/likunl-1/job-guide.git"

# 使用 token 进行认证
git push https://${GITHUB_TOKEN}@github.com/likunl-1/job-guide.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
else
    echo ""
    echo "❌ 推送失败，请检查你的 Token 是否正确。"
    exit 1
fi
