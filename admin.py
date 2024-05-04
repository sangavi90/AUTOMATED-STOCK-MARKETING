from django.contrib import admin
from .models import *
# Register your models here.




class CompanyNameAdmin(admin.ModelAdmin):
    list_display = ('company_name','symboltoken')
    ordering = ('company_name',)
    search_fields=['company_name','symboltoken']

admin.site.register(company_name,CompanyNameAdmin)

class OptionsAdmin(admin.ModelAdmin):
    search_fields=['company_name__company_name']
    ordering = ('company_name__company_name',)

admin.site.register(options, OptionsAdmin)

class ExpiryPriceAdmin(admin.ModelAdmin):
    search_fields=['company_name__company_name']
    ordering = ('company_name__company_name',)

admin.site.register(expirystrikeprice,  ExpiryPriceAdmin)

class strategyadmin(admin.ModelAdmin):
    list_display=('get_user_id','strategy_id','strategy_name')

    def get_user_id(self, obj):
        """
        Custom method to get the user_id of the associated SignInUser.
        """
        if obj.user_id:
            return obj.user_id.user_id  # Assuming user_id is the field representing the user's ID in SignInUser model
        else:
            return None  # Or any other default value you prefer

    get_user_id.short_description = 'User ID'  # Set a short de

admin.site.register( Strategy,strategyadmin)

class LegAdmin(admin.ModelAdmin):
    search_fields=['name','tradingsymbol']
    
    list_display= ('leg_id','name','tradingsymbol')

admin.site.register(Leg,LegAdmin)

class signuseradmin(admin.ModelAdmin):
    list_display=('user_id','username')

admin.site.register(SignInUser,signuseradmin)


# class pladmin(admin.ModelAdmin):
#      list_display = [field.name for field in pl._meta.get_fields()]
#      search_fields=[field.name for field in pl._meta.get_fields()]
class pladmin(admin.ModelAdmin):
    list_display=("company_name","trading_symbol","profit_loss","datetime")
admin.site.register(pl,pladmin)

admin.site.register(themes)