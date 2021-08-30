from django.contrib import admin
from .models import Problem, SampleTestCase, HiddenTestCase

admin.site.register(Problem)
admin.site.register(SampleTestCase)
admin.site.register(HiddenTestCase)
