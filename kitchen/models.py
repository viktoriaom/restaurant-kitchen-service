from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", ]


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    dishtype = models.ForeignKey(DishType, related_name="dishes", on_delete=models.CASCADE)
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", ]

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    dishes = models.ManyToManyField(Dish, related_name="ingredients")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", ]


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["username", ]

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})
