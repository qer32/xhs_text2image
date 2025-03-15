from django.db import models
import os
import uuid

class TextImageRequest(models.Model):
    """文本图片生成请求模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text_content = models.TextField(verbose_name="文本内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    # 图片生成配置
    image_width = models.IntegerField(default=1200, verbose_name="图片宽度")
    image_height = models.IntegerField(default=1500, verbose_name="图片高度")
    font_size = models.IntegerField(default=36, verbose_name="字体大小")
    line_spacing = models.FloatField(default=2.0, verbose_name="行间距")
    background_style = models.CharField(max_length=20, default='notebook', verbose_name="背景样式")
    font_style = models.CharField(max_length=20, default='normal', verbose_name="字体样式")
    
    def __str__(self):
        return f"文本图片请求 {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "文本图片请求"
        verbose_name_plural = "文本图片请求"
        ordering = ['-created_at']

class GeneratedImage(models.Model):
    """生成的图片模型"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(TextImageRequest, on_delete=models.CASCADE, related_name='images', verbose_name="关联请求")
    image_file = models.ImageField(upload_to='text_images/%Y/%m/%d/', verbose_name="图片文件")
    page_number = models.IntegerField(default=0, verbose_name="页码")
    is_long_image = models.BooleanField(default=False, verbose_name="是否为长图")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return f"图片 {self.id} - 请求 {self.request.id} - 页码 {self.page_number}"
    
    def delete(self, *args, **kwargs):
        # 删除图片文件
        if self.image_file:
            if os.path.isfile(self.image_file.path):
                os.remove(self.image_file.path)
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "生成图片"
        verbose_name_plural = "生成图片"
        ordering = ['request', 'page_number'] 