from django.db import models

from . import utils




class UrlIndex(models.Model):

    objects = models.Manager()

    key = models.CharField(
        verbose_name        = 'key',
        primary_key         = True,
        max_length          = utils.KEY_LEN,
        unique              = True,
        blank               = True,
        default             = utils.generate_key,
    )


    url = models.URLField(
        verbose_name        = 'url',
        unique              = True,
    )


    is_active = models.BooleanField(
        verbose_name        = 'isActive',
        default             = True,
    )


    created_at = models.DateTimeField(
        verbose_name        = 'createdAt',
        auto_now_add        = True,
    )


    updated_at = models.DateTimeField(
        verbose_name        = 'updatedAt',
        auto_now            = True,
    )



    class Meta:
        verbose_name        = 'URL Index',
        verbose_name_plural = 'URL Index',
        ordering            = ['-updated_at', '-created_at', 'active', 'url', 'key'],
