"""
WSGI config for xiaohongshu_web project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaohongshu_web.settings')

application = get_wsgi_application() 