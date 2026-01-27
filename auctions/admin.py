
from django.contrib import admin
from .models import Listings, Bid, Comment, User

#Register your models here

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Bid)
admin.site.register(Comment)
