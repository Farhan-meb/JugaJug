from django.contrib import admin
from accounts.models import Profile,Follow


admin.site.site_header = "MUOJ Admin Panel"
admin.site.site_title = "MU Online Judge"
admin.site.index_title = "MU Online Judge Admin Panel"


admin.site.register(Profile)
admin.site.register(Follow)
