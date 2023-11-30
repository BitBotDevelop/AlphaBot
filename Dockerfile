# 使用官方 Python 3.10 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 指定容器启动时执行的命令
CMD ["uvicorn", "server.main:app"]
