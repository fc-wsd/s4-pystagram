import os

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Photo


class PhotoTest(TestCase):
    # class Photo(models.Model):
    #     user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #     image = models.ImageField(upload_to='%Y/%m/%d/')
    #     description = models.TextField(max_length=500)
    #     created_at = models.DateTimeField(auto_now_add=True)
    #     updated_at = models.DateTimeField(auto_now=True)

    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            username='test1',
            password='1'
        )

    def test_save_photo_by_model(self):
        new_photo = Photo()
        new_photo.user = self.user1
        new_photo.image = os.path.join(settings.MEDIA_ROOT, 'hannal.png')
        new_photo.description = ''

        self.assertIsNone(new_photo.pk)
        new_photo.save()
        self.assertIsNotNone(new_photo.pk)

        new_photo2 = Photo()
        new_photo2.image = os.path.join(settings.MEDIA_ROOT, 'hannal.png')
        new_photo2.description = ''

        with self.assertRaises(ValueError):
            new_photo2.user = 'hannal'
        self.assertIsNone(new_photo2.pk)




