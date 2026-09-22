from decimal import Decimal

from django.test import TestCase

from shipping.models import Box, Order, OrderItem, Product
from shipping.services.box_selector import (
    EmptyOrderError,
    NoSuitableBoxError,
    calculate_total_weight,
    order_fits_in_box,
    product_fits_in_box,
    select_box,
)


class BoxSelectorTests(TestCase):

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

    def create_order(self, product, quantity=1):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )

        return order

    def test_total_weight_is_calculated_correctly(self):
        product = self.create_product(weight="2.50")
        order = self.create_order(product, quantity=3)

        total_weight = calculate_total_weight(order)

        self.assertEqual(
            total_weight,
            Decimal("7.50"),
        )

    def test_product_can_fit_after_rotation(self):
        product = self.create_product(
            length="30.00",
            width="20.00",
            height="10.00",
        )

        box = self.create_box(
            length="10.00",
            width="30.00",
            height="20.00",
        )

        self.assertTrue(
            product_fits_in_box(product, box)
        )

    def test_product_does_not_fit_when_dimensions_are_too_large(self):
        product = self.create_product(
            length="100.00",
            width="100.00",
            height="100.00",
        )

        box = self.create_box(
            length="50.00",
            width="50.00",
            height="50.00",
        )

        self.assertFalse(
            product_fits_in_box(product, box)
        )

    def test_order_fits_inside_box(self):
        product = self.create_product(
            length="20.00",
            width="10.00",
            height="5.00",
        )

        box = self.create_box(
            length="50.00",
            width="20.00",
            height="10.00",
        )

        order = self.create_order(product, quantity=2)

        self.assertTrue(
            order_fits_in_box(order, box)
        )

    def test_order_does_not_fit_when_total_length_is_too_large(self):
        product = self.create_product(
            length="30.00",
            width="10.00",
            height="5.00",
        )

        box = self.create_box(
            length="50.00",
            width="20.00",
            height="10.00",
        )

        order = self.create_order(product, quantity=2)

        self.assertFalse(
            order_fits_in_box(order, box)
        )

    def test_select_box_rejects_weight_limit(self):
        product = self.create_product(
            weight="15.00",
        )

        box = self.create_box(
            max_weight="10.00",
        )

        order = self.create_order(product)

        with self.assertRaises(NoSuitableBoxError):
            select_box(order)

    def test_select_box_chooses_smallest_volume(self):
        product = self.create_product(
            length="20.00",
            width="10.00",
            height="5.00",
        )

        self.create_box(
            name="Large Box",
            length="60.00",
            width="40.00",
            height="30.00",
            cost="50.00",
        )

        small_box = self.create_box(
            name="Small Box",
            length="30.00",
            width="20.00",
            height="10.00",
            cost="60.00",
        )

        order = self.create_order(product)

        result = select_box(order)

        self.assertEqual(
            result["box"],
            small_box,
        )

    def test_lower_cost_breaks_equal_volume_tie(self):
        product = self.create_product(
            length="20.00",
            width="10.00",
            height="5.00",
        )

        self.create_box(
            name="Box A",
            length="30.00",
            width="20.00",
            height="10.00",
            cost="80.00",
        )

        cheaper_box = self.create_box(
            name="Box B",
            length="30.00",
            width="20.00",
            height="10.00",
            cost="60.00",
        )

        order = self.create_order(product)

        result = select_box(order)

        self.assertEqual(
            result["box"],
            cheaper_box,
        )

    def test_empty_order_raises_error(self):
        order = Order.objects.create()

        with self.assertRaises(EmptyOrderError):
            select_box(order)

    def test_no_suitable_box_raises_error(self):
        product = self.create_product(
            length="100.00",
            width="100.00",
            height="100.00",
        )

        self.create_box(
            length="20.00",
            width="20.00",
            height="20.00",
        )

        order = self.create_order(product)

        with self.assertRaises(NoSuitableBoxError):
            select_box(order)