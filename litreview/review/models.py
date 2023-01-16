from django.db import models
from PIL import Image
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Ticket(models.Model):
    """Definition of a ticket."""

    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(
        max_length=2048, blank=True, verbose_name='Description'
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    image = models.ImageField(null=False, blank=False, verbose_name='Image')
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """Definition of a review."""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Note',
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    headline = models.CharField(max_length=128, verbose_name='Titre')
    body = models.TextField(
        max_length=8192, blank=True, verbose_name='Commentaire'
    )
    time_created = models.DateTimeField(auto_now_add=True)
