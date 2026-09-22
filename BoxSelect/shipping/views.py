from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Box, Order, Product
from .serializers import (
    BoxSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    ProductSerializer,
)
from .services.box_selector import (
    EmptyOrderError,
    NoSuitableBoxError,
    calculate_box_volume,
    calculate_total_weight,
    get_suitable_boxes,
    select_box,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "items__product"
    ).all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Create an order using OrderCreateSerializer for input validation,
        then return the created order using OrderSerializer.

        This keeps the write serializer separate from the read serializer.
        """
        input_serializer = OrderCreateSerializer(
            data=request.data
        )

        input_serializer.is_valid(raise_exception=True)

        order = input_serializer.save()

        response_serializer = OrderSerializer(
            order
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="recommend-box",
    )
    def recommend_box(self, request, pk=None):
        order = get_object_or_404(
            Order.objects.prefetch_related(
                "items__product"
            ),
            pk=pk,
        )

        try:
            result = select_box(order)

        except EmptyOrderError as exc:
            return Response(
                {
                    "success": False,
                    "error": str(exc),
                    "order_id": order.id,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except NoSuitableBoxError as exc:
            total_weight = calculate_total_weight(order)

            return Response(
                {
                    "success": False,
                    "error": str(exc),
                    "order_id": order.id,
                    "total_order_weight": total_weight,
                    "message": (
                        "The order cannot be packed using any "
                        "currently available box."
                    ),
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        selected_box = result["box"]
        total_weight = result["total_weight"]

        suitable_boxes = get_suitable_boxes(order)

        order_items = []

        for item in order.items.select_related("product").all():
            order_items.append(
                {
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_weight": item.product.weight,
                    "total_item_weight": (
                        item.product.weight * item.quantity
                    ),
                    "dimensions_cm": {
                        "length": item.product.length,
                        "width": item.product.width,
                        "height": item.product.height,
                    },
                }
            )

        suitable_box_details = []

        for box in suitable_boxes:
            suitable_box_details.append(
                {
                    "box_id": box.id,
                    "box_name": box.name,
                    "dimensions_cm": {
                        "length": box.internal_length,
                        "width": box.internal_width,
                        "height": box.internal_height,
                    },
                    "max_weight_kg": box.max_weight,
                    "cost_inr": box.cost,
                    "volume_cm3": calculate_box_volume(box),
                }
            )

        response_data = {
            "success": True,
            "order": {
                "id": order.id,
                "created_at": order.created_at,
                "items": order_items,
            },
            "recommendation": {
                "box_id": selected_box.id,
                "box_name": selected_box.name,
                "dimensions_cm": {
                    "length": selected_box.internal_length,
                    "width": selected_box.internal_width,
                    "height": selected_box.internal_height,
                },
                "max_weight_kg": selected_box.max_weight,
                "cost_inr": selected_box.cost,
                "volume_cm3": calculate_box_volume(
                    selected_box
                ),
            },
            "calculations": {
                "total_order_weight_kg": total_weight,
                "suitable_box_count": result[
                    "suitable_box_count"
                ],
                "suitable_box_ids": result[
                    "suitable_box_ids"
                ],
            },
            "selection_strategy": {
                "primary": "Smallest suitable internal volume",
                "secondary": "Lowest box cost",
                "tie_breaker": "Lowest box ID",
            },
            "explanation": (
                "The recommended box satisfies the order's "
                "weight and dimension requirements. Among all "
                "suitable boxes, the system selects the box "
                "with the smallest internal volume. If multiple "
                "boxes have the same volume, the lower-cost box "
                "is selected. If both volume and cost are equal, "
                "the lower database ID is used as the tie-breaker."
            ),
            "suitable_boxes": suitable_box_details,
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )