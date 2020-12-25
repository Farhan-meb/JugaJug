from django.contrib import admin
from  learning.models import Tutorial,Score,Problem,Submission,TestCase
# Register your models here.
admin.site.register(Tutorial)
admin.site.register(Score)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(TestCase)