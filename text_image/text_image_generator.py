#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import uuid
import re
from django.conf import settings

class XiaohongshuTextImage:
    def __init__(self, config=None):
        # 默认配置
        self.config = {
            # 小红书推荐的图片尺寸 (宽x高)
            'image_width': 1200,
            'image_height': 1500,
            
            # 文字和边距设置
            'font_size': 36,
            'line_spacing': 2.0,  # 行间距倍数
            'margin_top': 120,
            'margin_bottom': 120,
            'margin_left': 120,
            'margin_right': 120,
            
            # 背景样式
            'background_style': 'notebook',  # 'plain', 'notebook', 'dot', 'gradient', 'paper'
            'bg_color': (255, 252, 245),  # 米白色背景
            'bg_color2': (245, 242, 235),  # 渐变背景的第二种颜色
            'text_color': (70, 70, 70),   # 深灰色文字
            'line_color': (200, 200, 200),  # 浅灰色线条
            
            # 字体设置
            'font_path': None,  # 会自动查找
            'font_style': 'normal',  # 'normal', 'bold', 'light'
            
            # 其他设置
            'image_quality': 95,  # JPEG质量
            'image_format': 'JPEG',  # 图片格式
            'prefix': 'xhs_',  # 输出文件前缀
            'add_shadow': True,  # 是否添加文字阴影
            'add_border': True,  # 是否添加边框
            'rounded_corners': True,  # 是否使用圆角
            'corner_radius': 30,  # 圆角半径
        }
        
        # 更新配置
        if config:
            self.config.update(config)
        
        # 设置字体
        self._setup_font()
        
        # 计算行高
        self.line_height = int(self.config['font_size'] * self.config['line_spacing'])
        
    def _setup_font(self):
        """设置字体"""
        # 尝试使用用户指定的字体
        if self.config['font_path'] and os.path.exists(self.config['font_path']):
            font_path = self.config['font_path']
        else:
            # 尝试在resources目录中查找字体
            resources_dir = os.path.join(settings.BASE_DIR, "text_image", "resources")
            
            # 根据字体风格选择不同的字体
            if self.config['font_style'] == 'bold':
                font_name = "bold.ttf"
            elif self.config['font_style'] == 'light':
                font_name = "light.ttf"
            else:
                font_name = "font.ttf"
                
            resources_font = os.path.join(resources_dir, font_name)
            
            if os.path.exists(resources_font):
                font_path = resources_font
            else:
                # 使用系统字体
                if os.name == 'nt':  # Windows
                    if self.config['font_style'] == 'bold':
                        font_path = "C:\\Windows\\Fonts\\msyhbd.ttc"
                    elif self.config['font_style'] == 'light':
                        font_path = "C:\\Windows\\Fonts\\msyhl.ttc"
                    else:
                        font_path = "C:\\Windows\\Fonts\\msyh.ttc"
                else:  # Linux/Mac
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        
        try:
            self.font = ImageFont.truetype(font_path, self.config['font_size'])
        except Exception as e:
            # 使用默认字体
            self.font = ImageFont.load_default()
    
    def _add_background(self, img, draw):
        """添加背景样式"""
        width, height = img.size
        style = self.config['background_style']
        
        if style == 'plain':
            # 纯色背景，不做额外处理
            pass
        
        elif style == 'notebook':
            # 横格线背景
            y = self.config['margin_top']
            while y < height - self.config['margin_bottom']:
                draw.line([(self.config['margin_left'], y), 
                          (width - self.config['margin_right'], y)], 
                          fill=self.config['line_color'], width=1)
                y += self.line_height
        
        elif style == 'dot':
            # 点状背景
            dot_spacing = 20
            dot_radius = 1
            for x in range(self.config['margin_left'], width - self.config['margin_right'], dot_spacing):
                for y in range(self.config['margin_top'], height - self.config['margin_bottom'], dot_spacing):
                    draw.ellipse([(x-dot_radius, y-dot_radius), (x+dot_radius, y+dot_radius)], 
                                fill=self.config['line_color'])
        
        elif style == 'gradient':
            # 渐变背景
            # 创建一个新的图像用于渐变
            gradient = Image.new('RGB', (width, height), self.config['bg_color'])
            draw_gradient = ImageDraw.Draw(gradient)
            
            # 创建从上到下的渐变
            for y in range(height):
                # 计算当前位置的颜色
                r = int(self.config['bg_color'][0] + (self.config['bg_color2'][0] - self.config['bg_color'][0]) * y / height)
                g = int(self.config['bg_color'][1] + (self.config['bg_color2'][1] - self.config['bg_color'][1]) * y / height)
                b = int(self.config['bg_color'][2] + (self.config['bg_color2'][2] - self.config['bg_color'][2]) * y / height)
                
                # 绘制一条水平线
                draw_gradient.line([(0, y), (width, y)], fill=(r, g, b))
            
            # 将渐变图像粘贴到原图
            img.paste(gradient, (0, 0))
            
        elif style == 'paper':
            # 纸张纹理背景
            # 添加一些随机噪点模拟纸张纹理
            for x in range(0, width, 2):
                for y in range(0, height, 2):
                    if random.random() > 0.99:  # 1%的概率添加噪点
                        noise_color = (
                            max(0, min(255, self.config['bg_color'][0] - random.randint(0, 10))),
                            max(0, min(255, self.config['bg_color'][1] - random.randint(0, 10))),
                            max(0, min(255, self.config['bg_color'][2] - random.randint(0, 10)))
                        )
                        draw.point((x, y), fill=noise_color)
        
        # 添加边框
        if self.config['add_border']:
            draw.rectangle([(self.config['margin_left']-5, self.config['margin_top']-5), 
                            (width - self.config['margin_right']+5, height - self.config['margin_bottom']+5)], 
                            outline=self.config['line_color'], width=1)
    
    def _add_rounded_corners(self, img, radius):
        """添加圆角"""
        # 创建一个带有圆角的蒙版
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # 绘制圆角矩形
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        
        # 应用蒙版
        result = img.copy()
        result.putalpha(mask)
        
        return result
    
    def get_text_width(self, text):
        """获取文本宽度"""
        # 兼容不同版本的PIL
        try:
            # 新版本PIL
            return self.font.getbbox(text)[2]
        except AttributeError:
            # 旧版本PIL
            return self.font.getsize(text)[0]
    
    def _clean_text(self, text):
        """清理文本，去除可能导致渲染问题的特殊字符，但保留换行符"""
        if text is None:
            return ""
        
        # 替换常见的可能导致问题的Unicode符号为空格或普通符号
        replacements = {
            '\u2028': '\n',  # 行分隔符
            '\u2029': '\n',  # 段落分隔符
            '\u0085': '\n',  # 下一行
            '\u00A0': ' ',   # 不间断空格
            '\u3000': ' ',   # 全角空格
            '\u0009': ' ',   # 制表符
            '\u000C': ' ',   # 换页符
            '\u000B': ' ',   # 垂直制表符
            '\u00AD': '',    # 软连字符
            '\u2022': '•',   # 项目符号（替换为普通点）
            '\u2026': '...',  # 省略号
            '\u2013': '-',   # 短破折号
            '\u2014': '-',   # 长破折号
            '\u2018': "'",   # 左单引号
            '\u2019': "'",   # 右单引号
            '\u201C': '"',   # 左双引号
            '\u201D': '"',   # 右双引号
            '\u25CF': '●',   # 黑圆点
            '\r': '',        # 回车符直接删除
            '\r\n': '\n',    # Windows换行替换为标准换行
        }
        
        # 应用替换
        for old, new in replacements.items():
            if old in text:
                text = text.replace(old, new)
        
        # 单独处理换行符 - 先替换成特殊标记
        text = text.replace('\n', '||NEWLINE||')
        
        # 移除不可见字符和特殊控制字符
        # 扩大清理范围，包括所有控制字符和特殊Unicode区域
        cleaned_text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F\u200B-\u200F\u2028-\u202F\u2060-\u206F\uFEFF]', '', text)
        
        # 移除零宽字符和各种不可见Unicode字符
        cleaned_text = re.sub(r'[\u200B-\u200D\uFEFF\u2060-\u206F]', '', cleaned_text)
        
        # 替换所有特殊空格为普通空格
        cleaned_text = re.sub(r'[\u00A0\u2000-\u200A\u202F\u205F\u3000]', ' ', cleaned_text)
        
        # 替换多个连续空格为单个空格
        cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)
        
        # 处理空段落（可能导致黑方框）
        cleaned_text = cleaned_text.replace('||NEWLINE||||NEWLINE||', '||NEWLINE||')
        
        # 恢复换行符
        cleaned_text = cleaned_text.replace('||NEWLINE||', '\n')
        
        # 删除开头和结尾的空白
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text

    def text_to_long_image(self, text, output_path):
        """将文本转换为长图"""
        # 清理文本
        text = self._clean_text(text)
        
        # 计算每行最大字符数
        available_width = self.config['image_width'] - self.config['margin_left'] - self.config['margin_right']
        
        # 使用更精确的方法计算每行最大字符数
        wrapped_lines = []
        current_line = ""
        
        # 逐字添加并检查宽度
        for char in text:
            test_line = current_line + char
            # 如果是换行符，直接添加当前行并重置
            if char == '\n':
                wrapped_lines.append(current_line)
                current_line = ""
                continue
                
            # 计算当前行宽度
            line_width = self.get_text_width(test_line)
            
            # 如果宽度超过可用宽度，添加当前行并开始新行
            if line_width > available_width:
                wrapped_lines.append(current_line)
                current_line = char
            else:
                current_line += char
        
        # 添加最后一行
        if current_line:
            wrapped_lines.append(current_line)
        
        lines = wrapped_lines
        
        # 计算长图高度
        text_height = len(lines) * self.line_height
        image_height = text_height + self.config['margin_top'] + self.config['margin_bottom']
        
        # 创建长图
        long_image = Image.new('RGB', (self.config['image_width'], image_height), self.config['bg_color'])
        draw = ImageDraw.Draw(long_image)
        
        # 添加背景
        self._add_background(long_image, draw)
        
        # 绘制文本
        y_text = self.config['margin_top']
        for line in lines:
            # 注意：不再二次清理每行文本，因为文本已经在开始时被清理过
            # 且每行已经按照换行符和宽度限制分割好了
            
            # 确保文本不会超出右边界
            line_width = self.get_text_width(line)
            if line_width > available_width:
                # 如果单行文本宽度超过可用宽度，需要进一步截断
                truncated_line = ""
                for char in line:
                    if self.get_text_width(truncated_line + char) <= available_width:
                        truncated_line += char
                    else:
                        break
                line = truncated_line
            
            # 添加文字阴影
            if self.config['add_shadow']:
                shadow_offset = 2
                draw.text((self.config['margin_left'] + shadow_offset, y_text + shadow_offset), 
                          line, font=self.font, fill=(200, 200, 200, 100))
            
            # 绘制文本
            draw.text((self.config['margin_left'], y_text), line, font=self.font, fill=self.config['text_color'])
            y_text += self.line_height
        
        # 添加圆角
        if self.config['rounded_corners'] and self.config['image_format'] == 'PNG':
            long_image = self._add_rounded_corners(long_image, self.config['corner_radius'])
        
        # 保存长图
        long_image.save(output_path, format=self.config['image_format'], quality=self.config['image_quality'])
        
        return long_image, lines
    
    def split_long_image(self, long_image, lines, output_dir, prefix=None):
        """将长图切分为适合小红书的图片"""
        if prefix is None:
            prefix = self.config['prefix']
            
        width, height = long_image.size
        available_width = self.config['image_width'] - self.config['margin_left'] - self.config['margin_right']
        
        # 计算每张图片可以容纳的行数
        lines_per_image = (self.config['image_height'] - self.config['margin_top'] - self.config['margin_bottom'] - 40) // self.line_height
        
        # 计算需要的图片数量
        total_lines = len(lines)
        num_images = math.ceil(total_lines / lines_per_image)
        
        # 切分图片
        images = []
        for i in range(num_images):
            start_line = i * lines_per_image
            end_line = min((i + 1) * lines_per_image, total_lines)
            
            # 创建新图片
            img = Image.new('RGB', (width, self.config['image_height']), self.config['bg_color'])
            draw = ImageDraw.Draw(img)
            
            # 添加背景
            self._add_background(img, draw)
            
            # 绘制文本
            for j in range(start_line, end_line):
                y = self.config['margin_top'] + (j - start_line) * self.line_height
                
                # 确保文本不会超出右边界
                line = lines[j]
                # 注意：不再二次清理每行文本，因为文本已经在开始时被清理过
                
                line_width = self.get_text_width(line)
                if line_width > available_width:
                    # 如果单行文本宽度超过可用宽度，需要进一步截断
                    truncated_line = ""
                    for char in line:
                        if self.get_text_width(truncated_line + char) <= available_width:
                            truncated_line += char
                        else:
                            break
                    line = truncated_line
                
                # 添加文字阴影
                if self.config['add_shadow']:
                    shadow_offset = 2
                    draw.text((self.config['margin_left'] + shadow_offset, y + shadow_offset), 
                              line, font=self.font, fill=(200, 200, 200, 100))
                
                # 绘制文本
                draw.text((self.config['margin_left'], y), line, font=self.font, fill=self.config['text_color'])
            
            # 添加页码
            if num_images > 1:
                page_text = f"{i+1}/{num_images}"
                # 使用较小字体绘制页码
                page_font_size = int(self.config['font_size'] * 0.8)
                try:
                    page_font = ImageFont.truetype(self.font.path, page_font_size)
                except Exception:
                    page_font = self.font
                
                # 计算页码文本宽度
                try:
                    text_width = page_font.getbbox(page_text)[2]
                except AttributeError:
                    text_width = page_font.getsize(page_text)[0]
                
                # 添加页码阴影
                if self.config['add_shadow']:
                    shadow_offset = 1
                    draw.text((width - self.config['margin_right'] - text_width + shadow_offset, 
                              self.config['image_height'] - self.config['margin_bottom'] / 2 + shadow_offset), 
                              page_text, font=page_font, fill=(200, 200, 200, 100))
                
                # 绘制页码
                draw.text((width - self.config['margin_right'] - text_width, 
                          self.config['image_height'] - self.config['margin_bottom'] / 2), 
                          page_text, font=page_font, fill=self.config['text_color'])
            
            # 添加圆角
            if self.config['rounded_corners'] and self.config['image_format'] == 'PNG':
                img = self._add_rounded_corners(img, self.config['corner_radius'])
            
            # 保存图片
            file_ext = 'jpg' if self.config['image_format'] == 'JPEG' else 'png'
            output_path = os.path.join(output_dir, f"{prefix}{i+1}.{file_ext}")
            img.save(output_path, format=self.config['image_format'], quality=self.config['image_quality'])
            images.append(output_path)
            
        return images
    
    def process_text(self, text, output_dir=None):
        """处理文本，生成小红书图片"""
        # 生成唯一ID
        unique_id = str(uuid.uuid4())
        
        # 如果没有指定输出目录，使用媒体目录
        if output_dir is None:
            output_dir = os.path.join(settings.MEDIA_ROOT, 'text_images', unique_id)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成长图
        file_ext = 'jpg' if self.config['image_format'] == 'JPEG' else 'png'
        long_image_path = os.path.join(output_dir, f"long_image.{file_ext}")
        long_image, lines = self.text_to_long_image(text, long_image_path)
        
        # 切分长图
        images = self.split_long_image(long_image, lines, output_dir)
        
        # 返回相对于MEDIA_URL的路径
        relative_paths = []
        for image_path in images:
            relative_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
            relative_paths.append(relative_path)
        
        return {
            'id': unique_id,
            'long_image': os.path.relpath(long_image_path, settings.MEDIA_ROOT),
            'images': relative_paths
        }

def get_background_styles():
    """获取可用的背景样式"""
    return ['plain', 'notebook', 'dot', 'gradient', 'paper']

def get_font_styles():
    """获取可用的字体样式"""
    return ['normal', 'bold', 'light'] 