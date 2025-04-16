from django.contrib import admin , messages
from django import forms
from myapp.models import Contact,Category, Team, Dish, Profile,Order,TableBooking
admin.site.site_header = "FoodZone | Admin "

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','added_on','is_approved']
    list_editable = ['name','email','subject']
    # actions = [update_contacts]
    # action_form = Contact 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']


class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'discount_percent', 'discount_price_display', 'added_on', 'updated_on']
    list_editable = ['name', 'price', 'discount_percent', 'discount_price_display']
    @admin.display(description='Discount Price')
    def discount_price_display(self, obj):
        return f"{obj.discount_price():.2f}"
    

class TableBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'date', 'time', 'guests', 'created_at')
    list_filter = ('date', 'guests')
    search_fields = ('name', 'email', 'mobile')

    

admin.site.register(Contact,ContactAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Team, TeamAdmin )
admin.site.register(Dish, DishAdmin )
admin.site.register(Profile )
admin.site.register(Order)
admin.site.register(TableBooking)


