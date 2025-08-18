from django.contrib import admin

from .models import User, Skill, UserSkill

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(UserSkill)
