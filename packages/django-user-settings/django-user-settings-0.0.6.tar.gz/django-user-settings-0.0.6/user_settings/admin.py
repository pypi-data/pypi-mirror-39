from django.contrib import admin
from .models import UserSettings
# Register your models here.


class UserSettingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not isinstance(obj, UserSettings):
            raise NotImplementedError(
                'Only use this if your model is extend from base model.'
            )
        if not obj.created_by:
            obj.created_by = request.user
        obj.modified_by = request.user

        if not obj.user:
            obj.user = request.user
        return super(UserSettingAdmin, self).save_model(request, obj, form, change)


admin.site.register(UserSettings, UserSettingAdmin)
