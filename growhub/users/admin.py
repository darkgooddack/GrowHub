from django.contrib import admin

from .models import User, Skill, Experience

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Experience)
