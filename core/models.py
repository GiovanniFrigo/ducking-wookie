from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractBaseUser
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=36, unique=True,
        help_text=_('Required. 36 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    email = models.EmailField(_('email address'), unique=True, null=True)
    primary_phone = models.CharField(_('primary phone number'), max_length=50, blank=False, null=False)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    username_is_generated = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id and not self.username:
            self.username = self.email
        super(User, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __unicode__(self):
        return self.email

class Place(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_person = models.SmallIntegerField(default=10)

    # Allergy info
    contains_grain = models.BooleanField(default=True)
    contains_diary = models.BooleanField(default=False)
    contains_nuts = models.BooleanField(default=False)
    contains_meat = models.BooleanField(default=False)
    contains_fish = models.BooleanField(default=False)

    available_in = models.ManyToManyField(Place)

    def vegan_suitable(self):
        return not self.contains_meat and \
               not self.contains_fish and \
                not self.contains_diary

    def __unicode__(self):
        return self.name

class Cook(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User)

    date = models.DateTimeField()
    place = models.ForeignKey(Place)

    guest_number = models.PositiveSmallIntegerField(default=2)
    menu = models.ForeignKey(Menu)
    cook = models.ForeignKey(Cook)

    def __unicode__(self):
        return self.user + " " + self.date
