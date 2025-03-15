from django.contrib import admin
from .models import TextImageRequest, GeneratedImage

class GeneratedImageInline(admin.TabularInline):
    model = GeneratedImage
    readonly_fields = ['image_file', 'page_number', 'is_long_image', 'created_at']
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(TextImageRequest)
class TextImageRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'background_style', 'font_style', 'image_count']
    list_filter = ['background_style', 'font_style', 'created_at']
    search_fields = ['id', 'text_content']
    readonly_fields = ['id', 'created_at']
    inlines = [GeneratedImageInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = '图片数量'

@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'request_id', 'page_number', 'is_long_image', 'created_at']
    list_filter = ['is_long_image', 'created_at']
    search_fields = ['id', 'request__id']
    readonly_fields = ['id', 'created_at', 'image_preview']
    
    def request_id(self, obj):
        return obj.request.id
    request_id.short_description = '请求ID'
    
    def image_preview(self, obj):
        if obj.image_file:
            return f'<img src="{obj.image_file.url}" width="300" />'
        return '无图片'
    image_preview.short_description = '图片预览'
    image_preview.allow_tags = True 