from django.contrib import admin

from globalSetting.models import Setting

# Register your models here.


# class GlobalSettingAdmin(admin.ModelAdmin):
    
#     fields = ('newUserRequireActivation',)
    
#     def __init__(self, model, admin_site) -> None:
#         super().__init__(model, admin_site)
#         if not Setting.objects.all().exists():
#             print('adding 1st setting')
#             Setting.objects.create()
    
    
#     def has_add_permission(self, request) -> bool:
#         return False
    
#     def has_delete_permission(self, request , obj = False) -> bool:
#         return False
    
    

# admin.site.register(Setting, GlobalSettingAdmin)

