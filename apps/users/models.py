import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def image_folder(instance, filename):  # принимает 2 параметра - instance, filename
    return 'user_images/' + str(uuid.uuid4()) + '.png'


class CustomUser(AbstractUser):
    image = models.ImageField(_('аватарка'), upload_to='user_images', blank=True, default='user_images/default.png')
    about_me = models.CharField(_('о себе'), blank=True, max_length=128)
    is_verified_email = models.BooleanField(_('подтвержденная почта'), default=False)
    date_joined = models.DateTimeField(_('присоединился'), default=timezone.now)
    email = models.EmailField(_("почта"), blank=True, unique=True)

    phone = models.CharField(_('телефон'), max_length=16, blank=True)
    city = models.CharField(_('город'), max_length=32, blank=True)
    street = models.CharField(_('улица'), max_length=64, blank=True)
    house = models.CharField(_('дом'), max_length=16, blank=True)
    building = models.CharField(_('корпус'), max_length=16, blank=True)
    apartment = models.CharField(_('квартира'), max_length=16, blank=True)

    comments = models.PositiveIntegerField(_('комментариев'), default=0, editable=False,
                                           help_text=_('количество комментариев'
                                                       'под постами пользователя'))

    @staticmethod
    def get_user(username_or_email, password):
        try:
            user = CustomUser.objects.filter(username=username_or_email) \
                   or CustomUser.objects.filter(email=username_or_email)
            user = user.last()
        except CustomUser.DoesNotExist:
            user = None
        if user:
            pwd = check_password(password, user.password)
            if pwd:
                return user
        return False

    def add_comment(self):
        self.comments += 1
        self.save()

    def remove_comment(self):
        self.comments -= 1
        self.save()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
