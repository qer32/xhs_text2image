from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib import messages
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import DatabaseError, IntegrityError, OperationalError

from .models import TextImageRequest, GeneratedImage
from .forms import TextImageForm
from .text_image_generator import XiaohongshuTextImage, get_background_styles, get_font_styles

import os
import json
import uuid
from PIL import Image
import io
import traceback

def index(request):
    """首页视图"""
    try:
        form = TextImageForm()
        return render(request, 'text_image/index.html', {'form': form})
    except Exception as e:
        error_message = f"加载首页时发生错误: {str(e)}"
        return render(request, 'text_image/error.html', {'error_message': error_message, 'traceback': traceback.format_exc()})

def test_styles(request):
    """测试背景样式和字体样式函数"""
    bg_styles = get_background_styles()
    font_styles = get_font_styles()
    
    response = f"背景样式: {bg_styles}<br>字体样式: {font_styles}"
    return HttpResponse(response)

def generate_image(request):
    """生成图片视图"""
    if request.method == 'POST':
        try:
            form = TextImageForm(request.POST)
            if form.is_valid():
                try:
                    # 保存请求
                    text_request = form.save()
                except (DatabaseError, IntegrityError, OperationalError) as e:
                    messages.error(request, f"数据库错误: {str(e)}. 请确保数据库已正确设置。尝试运行 'python manage.py migrate'。")
                    return render(request, 'text_image/index.html', {'form': form})
                
                try:
                    # 获取表单数据
                    text_content = form.cleaned_data['text_content']
                    image_width = form.cleaned_data['image_width']
                    image_height = form.cleaned_data['image_height']
                    font_size = form.cleaned_data['font_size']
                    line_spacing = form.cleaned_data['line_spacing']
                    background_style = form.cleaned_data['background_style']
                    font_style = form.cleaned_data['font_style']
                    
                    # 配置图片生成器
                    config = {
                        'image_width': image_width,
                        'image_height': image_height,
                        'font_size': font_size,
                        'line_spacing': line_spacing,
                        'background_style': background_style,
                        'font_style': font_style,
                        'image_format': 'JPEG',  # 使用JPEG格式
                    }
                    
                    # 创建图片生成器
                    generator = XiaohongshuTextImage(config)
                    
                    # 生成图片
                    output_dir = os.path.join(settings.MEDIA_ROOT, 'text_images', str(text_request.id))
                    os.makedirs(output_dir, exist_ok=True)
                    
                    result = generator.process_text(text_content, output_dir)
                except Exception as e:
                    messages.error(request, f"图片生成错误: {str(e)}")
                    # 删除请求，因为图片生成失败
                    text_request.delete()
                    return render(request, 'text_image/index.html', {'form': form})
                
                try:
                    # 保存生成的图片到数据库
                    # 保存长图
                    long_image_path = os.path.join(settings.MEDIA_ROOT, result['long_image'])
                    with open(long_image_path, 'rb') as f:
                        long_image_content = f.read()
                        
                    long_image = GeneratedImage(
                        request=text_request,
                        is_long_image=True,
                        page_number=0
                    )
                    long_image.image_file.save(
                        f"long_image_{text_request.id}.jpg",
                        ContentFile(long_image_content)
                    )
                    
                    # 保存分页图片
                    for i, image_path in enumerate(result['images']):
                        full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                        with open(full_path, 'rb') as f:
                            image_content = f.read()
                            
                        page_image = GeneratedImage(
                            request=text_request,
                            is_long_image=False,
                            page_number=i+1
                        )
                        page_image.image_file.save(
                            f"page_{i+1}_{text_request.id}.jpg",
                            ContentFile(image_content)
                        )
                except Exception as e:
                    messages.error(request, f"保存图片错误: {str(e)}")
                    # 删除请求，因为保存图片失败
                    text_request.delete()
                    return render(request, 'text_image/index.html', {'form': form})
                
                # 重定向到结果页面
                return redirect('result', pk=text_request.id)
            else:
                # 表单验证失败
                messages.error(request, '表单验证失败，请检查输入。')
                return render(request, 'text_image/index.html', {'form': form})
        except Exception as e:
            messages.error(request, f"未知错误: {str(e)}")
            return render(request, 'text_image/index.html', {'form': TextImageForm()})
    else:
        # GET请求，显示表单
        form = TextImageForm()
        return render(request, 'text_image/index.html', {'form': form})

def result(request, pk):
    """结果页面视图"""
    try:
        text_request = get_object_or_404(TextImageRequest, pk=pk)
        
        # 获取所有生成的图片
        long_image = text_request.images.filter(is_long_image=True).first()
        page_images = text_request.images.filter(is_long_image=False).order_by('page_number')
        
        context = {
            'text_request': text_request,
            'long_image': long_image,
            'page_images': page_images,
        }
        
        return render(request, 'text_image/result.html', context)
    except Exception as e:
        messages.error(request, f"查看结果时发生错误: {str(e)}")
        return redirect('index')

class HistoryListView(ListView):
    """历史记录列表视图"""
    model = TextImageRequest
    template_name = 'text_image/history.html'
    context_object_name = 'requests'
    paginate_by = 10
    ordering = ['-created_at']
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"获取历史记录时发生错误: {str(e)}")
            return redirect('index')

class RequestDetailView(DetailView):
    """请求详情视图"""
    model = TextImageRequest
    template_name = 'text_image/detail.html'
    context_object_name = 'text_request'
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            text_request = self.get_object()
            
            # 获取所有生成的图片
            long_image = text_request.images.filter(is_long_image=True).first()
            page_images = text_request.images.filter(is_long_image=False).order_by('page_number')
            
            context['long_image'] = long_image
            context['page_images'] = page_images
            
            return context
        except Exception as e:
            messages.error(self.request, f"获取详情数据时发生错误: {str(e)}")
            return {'error': str(e)}
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"查看详情时发生错误: {str(e)}")
            return redirect('index')

class RequestDeleteView(DeleteView):
    """请求删除视图"""
    model = TextImageRequest
    template_name = 'text_image/confirm_delete.html'
    context_object_name = 'text_request'
    
    def get_success_url(self):
        messages.success(self.request, '请求已成功删除。')
        return reverse('history')
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"删除请求时发生错误: {str(e)}")
            return redirect('history') 