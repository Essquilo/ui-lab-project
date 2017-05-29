from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Packaging(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    img = models.ImageField()
    packaging = models.ForeignKey(Packaging, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User)
    cart = models.ManyToManyField(ShopItem)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)