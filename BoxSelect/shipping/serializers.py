from decimal import Decimal

from rest_framework import serializers

from .models import Box, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "weight",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )

        return value

    def validate(self, attrs):
        for field in ["length", "width", "height", "weight"]:
            value = attrs.get(field)

            if value is not None and value <= Decimal("0"):
                raise serializers.ValidationError(
                    {field: "Value must be greater than zero."}
                )

        return attrs


class BoxSerializer(serializers.ModelSerializer):
    volume = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Box
        fields = [
            "id",
            "name",
            "internal_length",
            "internal_width",
            "internal_height",
            "max_weight",
            "cost",
            "volume",
            "created_at",
        ]
        read_only_fields = ["id", "volume", "created_at"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Box name cannot be empty."
            )

        return value

    def validate(self, attrs):
        positive_fields = [
            "internal_length",
            "internal_width",
            "internal_height",
            "max_weight",
        ]

        for field in positive_fields:
            value = attrs.get(field)

            if value is not None and value <= Decimal("0"):
                raise serializers.ValidationError(
                    {field: "Value must be greater than zero."}
                )

        cost = attrs.get("cost")

        if cost is not None and cost < Decimal("0"):
            raise serializers.ValidationError(
                {"cost": "Cost cannot be negative."}
            )

        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    product_details = ProductSerializer(
        source="product",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_details",
            "quantity",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "product_details",
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )

        return value


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "items",
            "total_weight",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "items",
            "total_weight",
        ]

    def get_total_weight(self, obj):
        total_weight = Decimal("0.00")

        for item in obj.items.select_related("product").all():
            total_weight += item.product.weight * item.quantity

        return total_weight

class OrderCreateSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=OrderItemCreateSerializer(),
        allow_empty=False,
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "An order must contain at least one item."
            )

        return value

    def create(self, validated_data):
        items_data = validated_data["items"]

        order = Order.objects.create()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
                for item in items_data
            ]
        )

        return order