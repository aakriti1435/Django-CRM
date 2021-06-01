from django.contrib import admin
from .models import User, Lead, Agent, UserProfile, Category, FollowUp
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName', 'age', 'email']
    list_display_links = ['firstName']
    list_editable = ['lastName']
    list_filter = ['category']
    search_fields = ['firstName', 'lastName', 'email']

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Agent)
admin.site.register(FollowUp)