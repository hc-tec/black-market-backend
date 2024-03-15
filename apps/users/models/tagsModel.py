from django.db import models

class Tags(models.Model):
    class Meta:
        app_label = 'users'
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    tags_content = models.CharField(max_length=32, verbose_name="标签内容")

    def __str__(self):
        return self.tags_content
