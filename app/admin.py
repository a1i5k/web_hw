from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)
