from django.db import models
from entity.models import Person
from campaign.models import Campaign


class Staffer(models.Model):
    """
    A staff member of a campaign
    """

    campaign = models.ForeignKey(
        Campaign, related_name="staffers", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        Person, related_name="staff_jobs", on_delete=models.PROTECT
    )
    position = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
