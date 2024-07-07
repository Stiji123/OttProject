from django.contrib import admin
from .models import Customer, UserProfile, Adult_Movie, SubscriptionPlan, Kids_Movie


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('firstname','username', 'password', 'email','phonenumber')  # Customize the fields you want to display

admin.site.register(UserProfile)
list_display = ('firstname','username', 'password', 'email','phonenumber') # Customize the fields you want to display

admin.site.register(Adult_Movie)
admin.site.register(Kids_Movie)
admin.site.register(SubscriptionPlan)