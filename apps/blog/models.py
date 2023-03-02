import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser


def image_folder(instance, filename):  # принимает 2 параметра - instance, filename
    return 'blog_images/' + str(uuid.uuid4()) + '.png'


class PostQuerySet(models.QuerySet):
    def most_popular(self):
        last_week = timezone.now() - timezone.timedelta(hours=48)
        last_posts = self.filter(created__gt=last_week).order_by('-views')
        return last_posts


class Post(models.Model):
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name=_('пользователь'))

    title = models.CharField(_('заголовок'), max_length=200, unique=True)
    slug = models.SlugField(_('заголовок на англ.'), max_length=200, unique=True, blank=True,
                            help_text=_('можете оставить поле пустым'))

    image = models.ImageField(_('изображение'), upload_to=image_folder)
    content = models.TextField(_('текст поста'))

    created = models.DateTimeField(_('написан'), default=timezone.now)
    updated = models.DateTimeField(_('обновлен'), auto_now=True)
    views = models.IntegerField(_('просмотров'), default=0)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def add_view(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    to_post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    created = models.DateTimeField(_('оставлен'), auto_now_add=True)
    content = models.TextField(max_length=512)

    def __str__(self):
        return f'Комментарий пользователя {self.user.username}'
