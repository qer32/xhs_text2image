from django.apps import AppConfig


class TextImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'text_image'
    verbose_name = '小红书文生图' 