from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Car(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    price = models.IntegerField()

    def __str__(self):
        return self.name
