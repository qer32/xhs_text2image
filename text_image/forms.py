from django import forms
from .models import TextImageRequest
from .text_image_generator import get_background_styles, get_font_styles

class TextImageForm(forms.ModelForm):
    """文本图片生成表单"""
    
    # 直接在字段定义时设置选项
    background_style = forms.ChoiceField(
        choices=[(style, style.capitalize()) for style in get_background_styles()],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='背景样式',
        help_text='选择背景样式'
    )
    
    font_style = forms.ChoiceField(
        choices=[(style, style.capitalize()) for style in get_font_styles()],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='字体样式',
        help_text='选择字体样式'
    )
    
    class Meta:
        model = TextImageRequest
        fields = ['text_content', 'image_width', 'image_height', 'font_size', 
                  'line_spacing', 'background_style', 'font_style']
        widgets = {
            'text_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入要生成图片的文本内容...'
            }),
            'image_width': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 800,
                'max': 2000
            }),
            'image_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'max': 2500
            }),
            'font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 24,
                'max': 72
            }),
            'line_spacing': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1.0,
                'max': 3.0,
                'step': 0.1
            }),
        }
        labels = {
            'text_content': '文本内容',
            'image_width': '图片宽度',
            'image_height': '图片高度',
            'font_size': '字体大小',
            'line_spacing': '行间距',
        }
        help_texts = {
            'text_content': '输入要转换为图片的文本内容',
            'image_width': '图片宽度（像素），推荐1200',
            'image_height': '图片高度（像素），推荐1500',
            'font_size': '字体大小（像素），推荐36',
            'line_spacing': '行间距倍数，推荐2.0',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 确保选项已设置（虽然已在字段定义中设置，这里是双重保险）
        self.fields['background_style'].choices = [(style, style.capitalize()) for style in get_background_styles()]
        self.fields['font_style'].choices = [(style, style.capitalize()) for style in get_font_styles()] 