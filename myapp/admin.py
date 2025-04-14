from django.contrib import admin , messages
from myapp.models import Contact,Category, Team, Dish, Profile,Order
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
    

admin.site.register(Contact,ContactAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Team, TeamAdmin )
admin.site.register(Dish, DishAdmin )
admin.site.register(Profile )
admin.site.register(Order)
