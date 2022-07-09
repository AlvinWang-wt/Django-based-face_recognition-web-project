from django.apps import AppConfig

# 初始化执行
#from django.utils.module_loading import autodiscover_modules


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

# class StarkConfig(AppConfig):
#     name = 'stark'
#     def read(self):
#         autodiscover_modules('stark')