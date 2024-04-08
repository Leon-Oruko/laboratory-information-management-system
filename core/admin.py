from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsers, Sample, SampleRegistration, AnalystTask, LabManagerTask, AgronomistTask, ChangeLog,Clients,Chemical,Microbio,Full,Industry
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class ChangeLogAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in ChangeLog._meta.get_fields()]

    def has_add_permission(self, request):
        return False

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUsers
    ordering = ("email",)
    search_fields = ("email",)
    list_display = ("email","post")
    list_filter = ("email","post")
    fieldsets = (
        (None, {"fields": ("username","email", "password","post")}),
        (
            ("Permissions",{"fields":['admin','analyst','agronomist','lab_manager']}),
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",                   
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


admin.site.register(CustomUsers, CustomUserAdmin)
admin.site.register(Sample)
admin.site.register(SampleRegistration)
admin.site.register(AnalystTask)
admin.site.register(LabManagerTask)
admin.site.register(AgronomistTask)
admin.site.register(Clients)
admin.site.register(Chemical)
admin.site.register(Microbio)
admin.site.register(Full)
admin.site.register(Industry)
admin.site.register(ChangeLog, ChangeLogAdmin)