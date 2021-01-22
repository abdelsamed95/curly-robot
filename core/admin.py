from django.contrib import admin
from .models import Item, OrderItem, Order, ItemImage, Home


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Home)


class ItemImageAdmin(admin.StackedInline):
    model = ItemImage


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageAdmin]

    class Meta:
        model = Item


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    pass
