from django.db import models
from election.models import Candidate


class Campaign(models.Model):
    """
    A political campaign for a candidate
    """

    candidate = models.OneToOneField(
        Candidate, on_delete=models.PROTECT, related_name="campaign"
    )
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
