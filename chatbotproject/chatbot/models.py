from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'