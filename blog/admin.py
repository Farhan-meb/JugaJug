from django.contrib import admin
from blog.models import Post,Comments,Preference
# Register your models here.
admin.site.register(Post)
admin.site.register(Preference)
admin.site.register(Comments)