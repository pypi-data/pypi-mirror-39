from campaign.models import Endorsement, Staffer
from django.contrib import admin


class EndorsementInline(admin.StackedInline):
    model = Endorsement
    extra = 0


class StafferInline(admin.TabularInline):
    model = Staffer
    extra = 0


class CampaignAdmin(admin.ModelAdmin):
    inlines = [EndorsementInline, StafferInline]
