from django.contrib.auth.models import User
from django.db import models

from wye.base.constants import OrganisationType
from wye.base.models import AuditModel
from wye.regions.models import Location


class Organisation(AuditModel):
    organisation_type = models.PositiveSmallIntegerField(
        choices=OrganisationType.CHOICES, verbose_name="Organisation Type")
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    location = models.ForeignKey(Location)
    organisation_role = models.CharField(max_length=300)
    user = models.ManyToManyField(User, related_name='organisation_users')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'organisations'

    def __str__(self):
        return '{}-{}-{}'.format(self.name,
                                 self.organisation_type, self.location)
