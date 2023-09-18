__all__ = ('BaseAbstractUser',)

from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, EmailField, BooleanField, DateTimeField, DecimalField, ImageField

from users.models.manager import BaseManagerUser
from users.services.upload_files import upload_name


class BaseAbstractUser(AbstractBaseUser, PermissionsMixin):
    fullname_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    email = EmailField(_("email"),
                       unique=True,
                       help_text=_("Required. exsample@mail.com"),
                       validators=[email_validator],
                       error_messages={"unique": _("A user with that email already exists.")},
                       )

    fullname = CharField(_("fullname"),
                         max_length=150,
                         unique=True,
                         help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
                         validators=[fullname_validator],
                         error_messages={"unique": _("A user with that fullname already exists.")},
                         )


    is_staff = BooleanField(_("staff status"),
                            default=False,
                            help_text=_("Designates whether the user can log into this admin site."))

    is_active = BooleanField(_("active"),
                             default=False,
                             help_text=_(
                                 "Designates whether this user should be treated as active. "
                                 "Unselect this instead of deleting accounts."))

    is_moderator = BooleanField(_("moderator"),
                                default=False,
                                help_text=_(
                                    "This specifies whether the user should be considered a moderator."
                                    "Unselect this instead of deleting accounts."))
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = BaseManagerUser()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "fullname"
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

