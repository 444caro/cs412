# bloomboard/admin.py
# tell the admin we want to administer these models 
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Flower)
admin.site.register(Vase)
admin.site.register(BBProfile)
admin.site.register(Post)
admin.site.register(Comment)