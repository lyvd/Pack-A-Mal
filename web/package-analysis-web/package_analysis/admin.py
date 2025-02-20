from django.contrib import admin
from .models import Package, Report
# Register your models here.

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'package_version', 'ecosystem')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('package', 'time', 'num_files', 'num_commands', 'num_network_connections', 'num_system_calls') 

admin.site.register(Package, PackageAdmin)
admin.site.register(Report, ReportAdmin)

