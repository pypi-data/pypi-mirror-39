from django.core.exceptions import ValidationError
from django.db import models
from entity.models import Person, Organization
from campaign.models import Campaign


class Endorsement(models.Model):
    """
    A person's endorsement of a candidate
    """

    endorser = models.CharField(max_length=300)
    endorsee = models.ForeignKey(
        Campaign, related_name="endorsements", on_delete=models.CASCADE
    )
    endorsement_date = models.DateField()
    active = models.BooleanField(default=True)
    statement = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
