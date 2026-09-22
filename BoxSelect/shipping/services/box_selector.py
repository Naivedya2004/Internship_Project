from decimal import Decimal
from itertools import permutations

from shipping.models import Box, Order


class BoxSelectionError(Exception):
    """Base exception for box selection errors."""


class EmptyOrderError(BoxSelectionError):
    """Raised when an order has no items."""


class NoSuitableBoxError(BoxSelectionError):
    """Raised when no available box can contain the order."""


def calculate_total_weight(order):
    """
    Calculate the total weight of all products in the order.

    Total weight =
        sum(product weight × quantity)
    """

    total_weight = Decimal("0.00")

    for item in order.items.select_related("product").all():
        total_weight += item.product.weight * item.quantity

    return total_weight


def get_product_orientations(product):
    """
    Return all unique rotations of a product's dimensions.

    A product can be rotated in three-dimensional space, so all
    permutations of length, width and height are considered.
    """

    dimensions = (
        product.length,
        product.width,
        product.height,
    )

    return list(set(permutations(dimensions, 3)))


def product_fits_in_box(product, box):
    """
    Check whether one unit of a product can fit inside a box.

    Every possible orientation is checked.
    """

    box_dimensions = (
        box.internal_length,
        box.internal_width,
        box.internal_height,
    )

    for orientation in get_product_orientations(product):
        product_length, product_width, product_height = orientation

        if (
            product_length <= box_dimensions[0]
            and product_width <= box_dimensions[1]
            and product_height <= box_dimensions[2]
        ):
            return True

    return False


def order_fits_in_box(order, box):
    """
    Check whether all products in an order can be placed inside a box.

    This project intentionally uses a simple and explainable packing
    heuristic rather than claiming to solve general 3D bin packing.

    For each order item, we choose an orientation where:
      - width fits within the box width
      - height fits within the box height

    The lengths of all units are then added together and must fit
    within the box length.

    This provides a deterministic single-row packing approximation.
    """

    items = list(
        order.items.select_related("product").all()
    )

    if not items:
        return False

    box_length = box.internal_length
    box_width = box.internal_width
    box_height = box.internal_height

    total_required_length = Decimal("0.00")

    for item in items:
        product = item.product

        best_length = None

        for orientation in get_product_orientations(product):
            product_length, product_width, product_height = orientation

            if (
                product_width <= box_width
                and product_height <= box_height
            ):
                if best_length is None or product_length < best_length:
                    best_length = product_length

        if best_length is None:
            return False

        total_required_length += best_length * item.quantity

    return total_required_length <= box_length


def calculate_box_volume(box):
    """Return the internal volume of a box."""

    return (
        box.internal_length
        * box.internal_width
        * box.internal_height
    )


def get_suitable_boxes(order):
    """
    Return all boxes capable of handling the order.

    Eligibility requires both:
      1. total order weight <= box maximum weight
      2. order dimensions fit according to the packing heuristic
    """

    total_weight = calculate_total_weight(order)

    suitable_boxes = []

    for box in Box.objects.all():
        if total_weight > box.max_weight:
            continue

        if not order_fits_in_box(order, box):
            continue

        suitable_boxes.append(box)

    return suitable_boxes


def select_box(order):
    """
    Select the smallest suitable box.

    Selection priority:
      1. Smallest internal volume
      2. Lowest cost
      3. Lowest database ID

    The function returns both the selected box and useful
    calculation details for the API response.
    """

    if not order.items.exists():
        raise EmptyOrderError(
            "The order does not contain any products."
        )

    total_weight = calculate_total_weight(order)

    suitable_boxes = get_suitable_boxes(order)

    if not suitable_boxes:
        raise NoSuitableBoxError(
            "No available box can safely contain this order."
        )

    selected_box = min(
        suitable_boxes,
        key=lambda box: (
            calculate_box_volume(box),
            box.cost,
            box.id,
        ),
    )

    return {
        "box": selected_box,
        "total_weight": total_weight,
        "suitable_box_count": len(suitable_boxes),
        "suitable_box_ids": [box.id for box in suitable_boxes],
        "box_volume": calculate_box_volume(selected_box),
    }