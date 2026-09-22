from decimal import Decimal
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ValidationError
from django.test import TestCase

from shipping.models import Box, Order, OrderItem, Product


class ProductModelTests(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            name="Laptop",
            length=Decimal("35.00"),
            width=Decimal("25.00"),
            height=Decimal("3.00"),
            weight=Decimal("2.10"),
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.weight, Decimal("2.10"))

    def test_product_string_representation(self):
        product = Product.objects.create(
            name="Laptop",
            length=Decimal("35.00"),
            width=Decimal("25.00"),
            height=Decimal("3.00"),
            weight=Decimal("2.10"),
        )

        self.assertEqual(str(product), "Laptop")


class BoxModelTests(TestCase):

    def test_box_creation(self):
        box = Box.objects.create(
            name="Medium Box",
            internal_length=Decimal("50.00"),
            internal_width=Decimal("30.00"),
            internal_height=Decimal("15.00"),
            max_weight=Decimal("10.00"),
            cost=Decimal("70.00"),
        )

        self.assertEqual(box.name, "Medium Box")

    def test_box_volume(self):
        box = Box.objects.create(
            name="Medium Box",
            internal_length=Decimal("50.00"),
            internal_width=Decimal("30.00"),
            internal_height=Decimal("15.00"),
            max_weight=Decimal("10.00"),
            cost=Decimal("70.00"),
        )

        self.assertEqual(
            box.volume,
            Decimal("22500.000000"),
        )


class OrderModelTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            length=Decimal("35.00"),
            width=Decimal("25.00"),
            height=Decimal("3.00"),
            weight=Decimal("2.10"),
        )

    def test_order_creation(self):
        order = Order.objects.create()

        self.assertIsNotNone(order.id)

    def test_order_item_creation(self):
        order = Order.objects.create()

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product, self.product)

    def test_order_item_string_representation(self):
        order = Order.objects.create()

        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(
            str(item),
            "2 x Laptop",
        )

    def test_product_protects_existing_order_items(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )

        with self.assertRaises(Exception):
            self.product.delete()