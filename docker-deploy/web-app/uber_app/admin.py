from django.contrib import admin
from .models import User, Vehicle, Ride, RideSharer

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email_address', 'user_name', 'is_driver')
    
class DirverAdmin(admin.ModelAdmin):
    list_display = ('driver_id', 'driver_name', 'vehicle_type')
    


admin.site.register(User, UserAdmin)
admin.site.register(Vehicle, DirverAdmin)
admin.site.register(Ride)
admin.site.register(RideSharer)
