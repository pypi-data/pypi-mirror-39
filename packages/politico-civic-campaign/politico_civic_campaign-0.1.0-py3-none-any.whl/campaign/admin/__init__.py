from django.contrib import admin
from campaign.models import Campaign, Endorsement, Staffer
from .campaign import CampaignAdmin

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Endorsement)
admin.site.register(Staffer)
