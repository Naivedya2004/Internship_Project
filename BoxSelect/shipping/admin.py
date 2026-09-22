from django.contrib import admin

from .models import Box, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "length",
        "width",
        "height",
        "weight",
        "created_at",
    )
    search_fields = ("name",)
    ordering = ("id",)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "internal_length",
        "internal_width",
        "internal_height",
        "max_weight",
        "cost",
        "created_at",
    )
    search_fields = ("name",)
    ordering = ("id",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
    )
    list_filter = ("product",)
    search_fields = (
        "product__name",
    )