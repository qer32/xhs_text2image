# 小红书文生图 Web应用

这是一个基于Django的Web应用，用于将文本转换为小红书风格的图片。

## 功能特点

- 将文本转换为小红书风格的图片
- 支持多种背景样式：纯色、横格线、点状、渐变、纸张纹理
- 支持多种字体样式：普通、粗体、细体
- 自定义图片尺寸、字体大小和行间距
- 自动分页和页码标注
- 生成长图和分页图片
- 历史记录管理和查看

## 安装说明

### 环境要求

- Python 3.8+
- Django 4.2+
- Pillow 9.0+

### 安装步骤

1. 克隆或下载本项目到本地

2. 安装依赖包
```bash
pip install -r requirements.txt
```

3. **重要**: 初始化数据库 (首次运行前必须执行)
```bash
python manage.py makemigrations text_image
python manage.py migrate
```

4. 创建超级用户（可选，用于管理后台）
```bash
python manage.py createsuperuser
```

5. 收集静态文件
```bash
python manage.py collectstatic
```

6. 启动开发服务器
```bash
python manage.py runserver
```

7. 访问应用
在浏览器中访问 http://127.0.0.1:8000/

### 快速启动方式 (推荐)

使用提供的启动脚本可以自动完成上述步骤：

- Windows: 双击运行 `run.bat`
- Linux/macOS: 在终端执行 `bash run.sh`

启动脚本会自动:
- 安装依赖项
- 创建必要的目录
- 执行数据库迁移
- 收集静态文件
- 启动服务器并打开浏览器

## 使用说明

1. 在首页输入要转换为图片的文本内容
2. 选择背景样式和字体样式
3. 调整图片尺寸、字体大小和行间距（可选）
4. 点击"生成图片"按钮
5. 等待图片生成完成，然后下载或分享

## 自定义字体

如果要使用自定义字体，请将字体文件放在 `text_image/resources/` 目录下：
- 普通字体：`font.ttf`
- 粗体字体：`bold.ttf`
- 细体字体：`light.ttf`

如果没有提供自定义字体，系统将使用默认的系统字体。

## 常见问题

### 1. 出现数据库错误
如果看到 "no such table" 错误，请确保已执行数据库迁移:
```bash
python manage.py makemigrations text_image
python manage.py migrate
```

### 2. 图片无法保存
确保项目中的 `media` 目录存在且可写入，或者使用启动脚本自动创建相关目录。

### 3. 静态文件未加载
如果页面样式不正确，请确保已执行静态文件收集:
```bash
python manage.py collectstatic --noinput
```

## 部署到生产环境

### 使用Gunicorn和Nginx部署

1. 安装Gunicorn
```bash
pip install gunicorn
```

2. 启动Gunicorn
```bash
gunicorn xiaohongshu_web.wsgi:application --bind 0.0.0.0:8000
```

3. 配置Nginx（示例配置）
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 许可证

MIT License 