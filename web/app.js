// API配置
const API_BASE_URL = window.location.origin; // 自动适配部署环境
const SESSION_ID = 'session_' + Date.now(); // 会话ID

// DOM元素
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// 是否正在请求
let isRequesting = false;

// 自动调整输入框高度
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// 发送消息
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isRequesting) {
        return;
    }

    // 清空输入框
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // 显示用户消息
    appendUserMessage(message);

    // 显示加载动画
    showTypingIndicator();

    // 设置请求状态
    isRequesting = true;
    sendButton.disabled = true;

    try {
        // 调用Agent API
        const response = await fetch(`${API_BASE_URL}/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'query',
                session_id: SESSION_ID,
                content: {
                    query: {
                        prompt: [{
                            type: 'text',
                            content: { text: message }
                        }]
                    }
                }
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 显示AI回复
        hideTypingIndicator();
        
        // 提取AI消息内容
        const aiMessage = extractAIMessage(data);
        appendAIMessage(aiMessage);

    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        appendErrorMessage('抱歉，服务暂时不可用，请稍后重试。错误：' + error.message);
    } finally {
        isRequesting = false;
        sendButton.disabled = false;
    }
}

// 提取AI消息内容
function extractAIMessage(data) {
    // 根据实际API响应格式提取消息
    if (data && typeof data === 'object') {
        // 情况1: 直接包含text字段
        if (data.text) {
            return data.text;
        }
        // 情况2: 包含output字段
        if (data.output) {
            return data.output;
        }
        // 情况3: 包含result字段
        if (data.result) {
            return data.result;
        }
        // 情况4: 包含messages数组
        if (data.messages && data.messages.length > 0) {
            return data.messages[data.messages.length - 1].content;
        }
    }
    // 默认返回JSON字符串
    return JSON.stringify(data, null, 2);
}

// 添加用户消息
function appendUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar user-avatar">我</div>
            <div class="message-bubble">${escapeHtml(message)}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 添加AI消息
function appendAIMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar ai-avatar">AI</div>
            <div class="message-bubble">${formatMarkdown(message)}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 添加错误消息
function appendErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar ai-avatar">AI</div>
            <div class="message-bubble error-message">⚠️ ${escapeHtml(message)}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 显示加载动画
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    chatContainer.appendChild(typingIndicator);
    scrollToBottom();
}

// 隐藏加载动画
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// 滚动到底部
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 处理回车键
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 发送建议消息
function sendSuggestion(text) {
    messageInput.value = text;
    sendMessage();
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 简单的Markdown格式化
function formatMarkdown(text) {
    if (typeof text !== 'string') {
        text = String(text);
    }

    return text
        // 代码块
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
        // 行内代码
        .replace(/`([^`]+)`/g, '<code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">$1</code>')
        // 标题
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        // 加粗
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        // 斜体
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        // 无序列表
        .replace(/^- (.*$)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        // 有序列表
        .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
        // 换行
        .replace(/\n/g, '<br>');
}

// 页面加载完成后聚焦输入框
window.onload = function() {
    messageInput.focus();
};