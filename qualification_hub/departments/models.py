from django.db import models
# from managers.models import Manager


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # head = models.ForeignKey(Manager, verbose_name="Head manager of department", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
