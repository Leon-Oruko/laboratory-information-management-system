from django.contrib import admin
from .models import User, Sample, SampleRegistration, AnalystTask, LabManagerTask, AgronomistTask, ChangeLog

# Register your models here.

class ChangeLogAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in ChangeLog._meta.get_fields()]

    def has_add_permission(self, request):
        return False

admin.site.register(User)
admin.site.register(Sample)
admin.site.register(SampleRegistration)
admin.site.register(AnalystTask)
admin.site.register(LabManagerTask)
admin.site.register(AgronomistTask)
admin.site.register(ChangeLog, ChangeLogAdmin)
