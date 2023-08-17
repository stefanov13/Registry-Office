from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators
from ..user_profiles.models import Profile

# Create your models here.


class NewsFeedModel(models.Model):
    TITLE_MAX_LENGTH = 100
    TITLE_MIN_LENGTH = 2

    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        editable=False,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            validators.MinLengthValidator(
            TITLE_MIN_LENGTH,
            'Полето трябва да съдържа поне 2 букви',
            ),
        ],
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    date = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        # If the object is being created and the author field is not set, fill it with the currently logged-in user's profile
        if not self.author_id  \
                and hasattr(self, 'request') \
                and hasattr(self.request, 'user') \
                and hasattr(self.request.user, 'profile'):
            self.author = self.request.user.profile

        super().save(*args, **kwargs)
