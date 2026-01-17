# 部署配置文件

## Docker 部署
- **Dockerfile** - Docker 镜像构建配置
- **docker-compose.yml** - Docker Compose 配置

## 平台部署
- **Procfile** - Heroku 平台配置
- **railway.toml** - Railway 平台配置
- **.dockerignore** - Docker 忽略文件
- **.nixpacks.toml** - Nixpacks 配置

## 使用方法

### Docker
```bash
# 构建镜像
docker build -t job-guide .

# 运行容器
docker run -d -p 8000:8000 --name job-guide job-guide
docker-compose up -d
