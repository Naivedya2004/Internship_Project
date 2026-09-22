from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shipping.models import Box, Order, OrderItem, Product


class ShippingAPITests(APITestCase):

    def create_product(
        self,
        name="Laptop",
        length="35.00",
        width="25.00",
        height="3.00",
        weight="2.10",
    ):
        return Product.objects.create(
            name=name,
            length=Decimal(length),
            width=Decimal(width),
            height=Decimal(height),
            weight=Decimal(weight),
        )

    def create_box(
        self,
        name="Medium Box",
        length="50.00",
        width="30.00",
        height="15.00",
        max_weight="10.00",
        cost="70.00",
    ):
        return Box.objects.create(
            name=name,
            internal_length=Decimal(length),
            internal_width=Decimal(width),
            internal_height=Decimal(height),
            max_weight=Decimal(max_weight),
            cost=Decimal(cost),
        )

    def test_product_creation_api(self):
        url = reverse("product-list")

        response = self.client.post(
            url,
            {
                "name": "Laptop",
                "length": "35.00",
                "width": "25.00",
                "height": "3.00",
                "weight": "2.10",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Laptop",
        )

    def test_product_rejects_negative_dimension(self):
        url = reverse("product-list")

        response = self.client.post(
            url,
            {
                "name": "Invalid Product",
                "length": "-10.00",
                "width": "20.00",
                "height": "5.00",
                "weight": "1.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_box_creation_api(self):
        url = reverse("box-list")

        response = self.client.post(
            url,
            {
                "name": "Medium Box",
                "internal_length": "50.00",
                "internal_width": "30.00",
                "internal_height": "15.00",
                "max_weight": "10.00",
                "cost": "70.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Medium Box",
        )

    def test_order_creation_api(self):
        product = self.create_product()

        url = reverse("order-list")

        response = self.client.post(
            url,
            {
                "items": [
                    {
                        "product": product.id,
                        "quantity": 2,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        order_id = response.data["id"]

        self.assertTrue(
            Order.objects.filter(id=order_id).exists()
        )

        self.assertEqual(
            OrderItem.objects.filter(
                order_id=order_id
            ).count(),
            1,
        )

    def test_empty_order_is_rejected(self):
        url = reverse("order-list")

        response = self.client.post(
            url,
            {
                "items": []
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_recommend_box_api_success(self):
        product = self.create_product()

        self.create_box(
            name="Small Box",
            length="20.00",
            width="20.00",
            height="10.00",
            max_weight="5.00",
            cost="40.00",
        )

        suitable_box = self.create_box(
            name="Medium Box",
            length="50.00",
            width="30.00",
            height="15.00",
            max_weight="10.00",
            cost="70.00",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        url = reverse(
            "order-recommend-box",
            kwargs={"pk": order.id},
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["order"]["id"],
            order.id,
        )

        self.assertEqual(
            response.data["recommendation"]["box_id"],
            suitable_box.id,
        )

        self.assertIn(
            "calculations",
            response.data,
        )

        self.assertIn(
            "explanation",
            response.data,
        )

    def test_recommend_box_returns_failure_when_no_box_fits(self):
        product = self.create_product(
            length="100.00",
            width="100.00",
            height="100.00",
        )

        self.create_box(
            name="Small Box",
            length="20.00",
            width="20.00",
            height="20.00",
            max_weight="5.00",
            cost="40.00",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        url = reverse(
            "order-recommend-box",
            kwargs={"pk": order.id},
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

        self.assertFalse(
            response.data["success"]
        )

        self.assertIn(
            "error",
            response.data,
        )

    def test_order_detail_contains_items(self):
        product = self.create_product()

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": order.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

        self.assertEqual(
            response.data["items"][0]["quantity"],
            2,
        )