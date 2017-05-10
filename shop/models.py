from django.db import models


class Packaging(models.Model):
    name = models.CharField(max_length=200)


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)


class Designation(models.Model):
    name = models.CharField(max_length=200)


class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    img = models.ImageField()
    packaging = models.ForeignKey(Packaging, models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    designation = models.ForeignKey(Designation, models.CASCADE)
