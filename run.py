#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书文生图 Web应用启动脚本
"""

import os
import sys
import webbrowser
import subprocess
import time
import platform
from pathlib import Path

# 获取当前脚本所在目录
BASE_DIR = Path(__file__).resolve().parent

def check_dependencies():
    """检查依赖项是否已安装"""
    try:
        import django
        import PIL
        return True
    except ImportError:
        print("正在安装依赖项...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(BASE_DIR, "requirements.txt")])
        return True

def setup_database():
    """设置数据库"""
    print("正在设置数据库...")
    try:
        # 创建数据库迁移文件
        print("创建数据库迁移文件...")
        subprocess.check_call([sys.executable, os.path.join(BASE_DIR, "manage.py"), "makemigrations", "text_image"])
        
        # 应用数据库迁移
        print("应用数据库迁移...")
        subprocess.check_call([sys.executable, os.path.join(BASE_DIR, "manage.py"), "migrate"])
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"数据库设置失败: {str(e)}")
        print("请手动执行以下命令:")
        print(f"  cd {BASE_DIR}")
        print("  python manage.py makemigrations text_image")
        print("  python manage.py migrate")
        return False

def collect_static():
    """收集静态文件"""
    print("正在收集静态文件...")
    try:
        subprocess.check_call([sys.executable, os.path.join(BASE_DIR, "manage.py"), "collectstatic", "--noinput"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"静态文件收集失败: {str(e)}")
        return False

def create_media_dirs():
    """创建媒体目录"""
    try:
        media_dir = os.path.join(BASE_DIR, "media", "text_images")
        os.makedirs(media_dir, exist_ok=True)
        
        resources_dir = os.path.join(BASE_DIR, "text_image", "resources")
        os.makedirs(resources_dir, exist_ok=True)
        
        print(f"媒体目录已创建: {media_dir}")
        print(f"资源目录已创建: {resources_dir}")
        return True
    except Exception as e:
        print(f"目录创建失败: {str(e)}")
        return False

def start_server(port=8000):
    """启动Django开发服务器"""
    print(f"正在启动服务器，端口: {port}...")
    url = f"http://127.0.0.1:{port}/"
    
    # 延迟打开浏览器，确保服务器已启动
    def open_browser():
        time.sleep(2)
        print(f"正在打开浏览器: {url}")
        webbrowser.open(url)
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Django服务器
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaohongshu_web.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", f"0.0.0.0:{port}"])

def main():
    """主函数"""
    print("=" * 60)
    print("小红书文生图 Web应用启动工具")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 切换到脚本所在目录
    os.chdir(BASE_DIR)
    
    # 检查依赖项
    if not check_dependencies():
        print("错误: 无法安装依赖项")
        sys.exit(1)
    
    # 创建媒体目录
    if not create_media_dirs():
        print("警告: 无法创建所有必要的目录，应用可能无法正常工作")
    
    # 设置数据库
    if not setup_database():
        print("警告: 数据库设置未完成，应用可能无法正常工作")
        
    # 收集静态文件
    if not collect_static():
        print("警告: 静态文件收集失败，应用可能无法正常显示样式")
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 