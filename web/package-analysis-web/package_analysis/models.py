from django.db import models

# Create your models here.

class Package(models.Model):
    package_name = models.CharField(max_length=20)
    package_version = models.CharField(max_length=20)
    ecosystem = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.package_name} {self.package_version} {self.ecosystem}"
    
    

class Report(models.Model):
    package = models.OneToOneField(Package, on_delete=models.CASCADE, related_name='report')
    time = models.FloatField()
    num_files = models.IntegerField()
    num_commands = models.IntegerField()
    num_network_connections = models.IntegerField()
    num_system_calls = models.IntegerField()
    files = models.JSONField(default=dict)  # Provide a default value
    dns = models.JSONField(default=list)  # Provide a default value
    ips = models.JSONField(default=list)  # Provide a default value
    commands = models.JSONField(default=list)  # Provide a default value
    syscalls = models.JSONField(default=list)  # Provide a default value



    def __str__(self):
        return f"{self.package} {self.time} (seconds)"