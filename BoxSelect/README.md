# BoxSelect — AI-Assisted Box Selection System

A Django REST API that recommends a suitable ecommerce shipping box for an order based on product dimensions, product weight, box dimensions, box weight capacity, and box cost.

The project was built as a hiring assignment with a focus on clean Django architecture, explainable business logic, validation, automated testing, and transparent AI-assisted development.

---

## 1. Problem Statement

Ecommerce warehouses need to select an appropriate shipping box for every order.

A box must:

- Be large enough to contain the products.
- Support the total weight of the order.
- Avoid unnecessary excess space where possible.
- Have a reasonable cost.

The system accepts product and box information and recommends the smallest suitable box according to a deterministic selection strategy.

---

## 2. Solution

BoxSelect provides REST APIs for managing:

- Products
- Shipping boxes
- Orders
- Order items

The main recommendation endpoint evaluates an order against all available boxes.

A box is considered suitable when:

1. The total order weight does not exceed the box's maximum supported weight.
2. The products can fit within the box using the project's dimension-fitting heuristic.

Among all suitable boxes, the system selects:

1. Smallest internal volume
2. Lowest cost when volumes are equal
3. Lowest database ID as the final tie-breaker

The API also returns the calculations and explanation behind the recommendation.

---

## 3. Key Features

### Product Management

Products contain:

- Name
- Length
- Width
- Height
- Weight

Product dimensions and weight must be greater than zero.

### Box Management

Boxes contain:

- Name
- Internal length
- Internal width
- Internal height
- Maximum supported weight
- Cost

The system also calculates the internal box volume.

### Order Management

An order can contain multiple products with quantities.

The system calculates the total order weight using:

```text
Total Order Weight =
Σ(Product Weight × Quantity)
Rotation-Aware Dimension Checking
Products can be rotated inside a box.
The system considers all possible three-dimensional orientations of a product when checking whether it can fit.
Weight Validation
A box is rejected when:
Total Order Weight > Box Maximum Weight
Box Recommendation
The system evaluates available boxes and chooses the smallest suitable internal volume.
Explainable Recommendation
The recommendation API returns:
- Order information
- Order items
- Product dimensions
- Product weights
- Total order weight
- Recommended box
- Recommended box dimensions
- Maximum supported weight
- Box cost
- Box volume
- Suitable boxes
- Selection strategy
- Explanation
Validation and Error Handling
The API handles cases such as:
- Negative dimensions
- Zero dimensions
- Negative weight
- Invalid quantity
- Empty orders
- Nonexistent products
- Orders that cannot fit into any available box
4. Technology Stack
Technology	Purpose
Python	Programming language
Django	Backend web framework
Django REST Framework	REST API development
SQLite	Development database
Django Test Framework	Automated testing
Git	Version control


No external AI model is required at runtime.
The recommendation logic is deterministic and explainable.
5. Project Architecture
BoxSelect/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── AI_USAGE.md
├── TEST_OUTPUT.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── shipping/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    │
    ├── services/
    │   ├── __init__.py
    │   └── box_selector.py
    │
    ├── migrations/
    │   └── 0001_initial.py
    │
    └── shipping_tests/
        ├── __init__.py
        ├── test_models.py
        ├── test_box_selector.py
        └── test_api.py
6. Data Model
Product
Product
---------
id
name
length
width
height
weight
created_at
Box
Box
---------
id
name
internal_length
internal_width
internal_height
max_weight
cost
created_at
Order
Order
---------
id
created_at
OrderItem
OrderItem
---------
id
order
product
quantity
Relationship:
Order
  │
  └── OrderItem ─── Product
An order can contain multiple order items, and each order item references a product and its quantity.

7. Box Selection Logic

The recommendation process follows these steps.
Step 1 — Calculate Total Order Weight
For every order item:
item weight = product weight × quantity
Then:
total order weight =
sum of all item weights
Step 2 — Check Box Weight Capacity
A box is rejected when:
total order weight > box.max_weight
Otherwise it remains eligible for dimension checking.
Step 3 — Check Product Dimensions
The system considers rotations of each product.
For example, a product with:
10 × 20 × 30 cm
can be considered in different orientations such as:
10 × 20 × 30
10 × 30 × 20
20 × 10 × 30
20 × 30 × 10
30 × 10 × 20
30 × 20 × 10
Duplicate orientations are removed automatically when dimensions are repeated.
Step 4 — Multi-Product Packing Heuristic
For orders containing multiple products, the project uses a deterministic single-row packing heuristic.
For every order item, the algorithm finds an orientation where:
product width  <= box width
product height <= box height
The required lengths are then added:
Required Length =
Σ(Best Product Length × Quantity)
The order fits when:
Required Length <= Box Length
This approach was intentionally chosen because it is:
- Deterministic
- Easy to understand
- Easy to test
- Appropriate for a small hiring assignment
Important Limitation
This is not a general 3D bin-packing algorithm.
The project does not claim to calculate an optimal physical arrangement for arbitrary products.
A production system could use a more advanced packing algorithm or optimization approach.
8. Box Selection Strategy
After filtering unsuitable boxes, the system sorts candidates using:
1. Internal volume — ascending
2. Cost — ascending
3. Database ID — ascending
Therefore:
Selected Box =
smallest suitable volume
        ↓
lowest cost if tied
        ↓
lowest ID if still tied
This makes the selection deterministic.

9. API Endpoints

Base URL:
/api/
Products
List Products
GET /api/products/
Create Product
POST /api/products/
Example:
{
    "name": "Laptop",
    "length": 35,
    "width": 25,
    "height": 3,
    "weight": 2.5
}
Boxes
List Boxes
GET /api/boxes/
Create Box
POST /api/boxes/
Example:
{
    "name": "Medium Box",
    "internal_length": 40,
    "internal_width": 30,
    "internal_height": 15,
    "max_weight": 10,
    "cost": 80
}
Orders
List Orders
GET /api/orders/
Create Order
POST /api/orders/
Example:
{
    "items": [
        {
            "product": 1,
            "quantity": 2
        }
    ]
}
Get Order
GET /api/orders/<id>/
Box Recommendation
POST /api/orders/<id>/recommend-box/
This is the main business endpoint.
It evaluates the order against available boxes and returns the recommended box along with the supporting calculations and explanation.

10. Example Recommendation Flow

Create Products
      │
      ▼
Create Shipping Boxes
      │
      ▼
Create Order
      │
      ▼
POST /api/orders/<id>/recommend-box/
      │
      ▼
Calculate Total Weight
      │
      ▼
Check Box Weight Capacity
      │
      ▼
Check Product Dimensions
      │
      ▼
Find Suitable Boxes
      │
      ▼
Compare Internal Volumes
      │
      ▼
Apply Cost Tie-Breaker
      │
      ▼
Return Recommended Box

11. Running the Project Locally

1. Clone the Repository
git clone :https://github.com/Naivedya2004/Internship_Project
cd BoxSelect
2. Create a Virtual Environment
Windows PowerShell:
python -m venv venv
Activate it:
venv\Scripts\Activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Run Django Checks
python manage.py check
Expected result:
System check identified no issues
6. Start the Development Server
python manage.py runserver
The API will be available at:
http://127.0.0.1:8000/

12. Django Admin

The project includes Django Admin for managing:
- Products
- Boxes
- Orders
- Order items
Create an administrator account:
python manage.py createsuperuser
Then start the server:
python manage.py runserver
Open:
http://127.0.0.1:8000/admin/

13. Testing

The project uses Django's built-in testing framework.
Run all tests:
python manage.py test
Run tests with detailed output:
python manage.py test -v 2
The current verified test suite contains:
26 tests
26 passed
0 failures
0 errors
The detailed test output is preserved in:
TEST_OUTPUT.md
Test Categories
Model Tests
Tests include:
- Product creation
- Product string representation
- Box creation
- Box volume calculation
- Order creation
- Order item creation
- Order item string representation
- Product deletion protection
Business Logic Tests

Tests include:

- Total order weight
- Product rotation
- Product dimension failure
- Order dimension fitting
- Excessive total length
- Box weight limitation
- Smallest-volume selection
- Cost tie-breaking
- Empty order handling
- No suitable box handling
API Tests
Tests include:
- Product creation
- Box creation
- Order creation
- Order detail
- Invalid product dimensions
- Successful box recommendation
- No suitable box response
- Empty order rejection

14. AI-Assisted Development

AI tools were used during development for assistance with:
- Project structure
- Django implementation
- Serializer and API design
- Business-logic implementation
- Test design
- Debugging
- Documentation structure
AI-generated suggestions were reviewed and tested locally before being accepted.
The development process included identifying and fixing an API serialization issue where the order creation endpoint attempted to serialize Django's reverse RelatedManager using the write serializer.
The final implementation separates:
OrderCreateSerializer
for input validation and creation from:
OrderSerializer
for returning created order data.
Further details are documented in:
AI_USAGE.md
The exported AI conversation transcript should be included separately in the repository as required by the assignment.

15. Design Decisions

Why Django REST Framework?
Django REST Framework provides:
- Serializers
- ViewSets
- Validation
- RESTful routing
- API testing support
This keeps the implementation compact while maintaining clear separation between API and business logic.
Why SQLite?
SQLite is sufficient for this assignment because the focus is the recommendation logic and API implementation.
The application structure can be migrated to PostgreSQL for production deployment without changing the core box-selection algorithm.
Why deterministic logic instead of an AI model?
The recommendation is fundamentally a constraint and optimization problem.
The required decision can be explained using:
- Dimensions
- Weight
- Volume
- Cost
A deterministic approach makes every recommendation reproducible and explainable.
AI was therefore used as a development assistant rather than as an opaque runtime decision-maker.

16. Assumptions

The implementation makes the following assumptions:
1. Product dimensions are measured in centimeters.
2. Product weight is measured in kilograms.
3. Box dimensions represent internal usable dimensions.
4. Box maximum weight is measured in kilograms.
5. Box cost is represented in INR.
6. Products can be rotated.
7. Products are treated as rectangular cuboids.
8. The multi-product packing strategy uses the documented single-row heuristic.
9. The system selects the smallest suitable box by internal volume.
10. Lower cost is used as the first tie-breaker.
11. Database ID is used as the final deterministic tie-breaker.

17. Error Handling

The API returns appropriate error responses for invalid or impossible requests.
Examples include:
Invalid Product
Negative dimensions
Zero dimensions
Negative weight
Invalid Order
Empty item list
Quantity less than 1
Invalid product ID
No Suitable Box
When no available box satisfies both:
Dimension requirements
+
Weight requirements
the recommendation endpoint returns an error response instead of returning an invalid recommendation.
18. Current Limitations
This project is intentionally scoped for a small hiring assignment.
Current limitations include:
- No authentication or authorization layer
- SQLite used for local development
- No background job processing
- No external warehouse/inventory integration
- No advanced 3D packing optimization
- No dynamic shipping carrier pricing
- No persistent recommendation history
- No frontend application
The most important algorithmic limitation is that multi-product packing uses a deterministic single-row heuristic rather than solving general 3D bin packing.

19. Future Improvements

Possible production improvements include:
- PostgreSQL
- Authentication and role-based access
- Advanced 3D bin-packing optimization
- Multiple-box recommendations
- Shipping carrier API integration
- Warehouse inventory integration
- Recommendation history
- Packaging material optimization
- Shipping-cost estimation
- API documentation with OpenAPI/Swagger
- Docker-based deployment
- CI/CD pipeline
- Monitoring and logging

20. Submission Files

The assignment submission should contain:
BoxSelect/
│
├── Source code
├── README.md
├── AI_USAGE.md
├── TEST_OUTPUT.md
├── Test cases
└── Exported AI chat transcript
The final project should be submitted as a single ZIP archive as requested by the assignment.

21. Learning Reflection

I learned how to make a project with proper AI Usage and how to make it efficent and i also got to showcase
my skills which will be of good use to your organization.


22. Author

Naivedya Dubey
B.Tech — Computer Science Engineering
Specialization: Artificial Intelligence & Machine Learning
GitHub:
https://github.com/Naivedya2004
23. License
This project was developed as part of a technical hiring assignment.

### Important

There is one deliberate placeholder:

```text
https://github.com/Naivedya2004/Internship_Project
