from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределенный пользователь, дополнен нужными полями
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = [
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    ]
    bio = models.CharField(
        max_length=4000, null=True, verbose_name="Информация о себе"
    )
    role = models.CharField(
        max_length=50, choices=ROLES, verbose_name="Роль", default=USER
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
