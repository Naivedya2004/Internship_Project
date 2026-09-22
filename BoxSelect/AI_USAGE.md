# AI Usage Documentation

## 1. Purpose

AI tools were used during the development of this assignment as development assistance.

The AI was used for:
- Project structure planning
- Django and Django REST Framework implementation guidance
- Writing and reviewing code
- Debugging implementation issues
- Improving test coverage
- Reviewing API behavior and error handling
- Preparing project documentation

The final implementation was reviewed and tested locally before being considered complete.

---

## 2. AI Tool Used

**Tool:** ChatGPT

AI assistance was used interactively during development. The developer provided the project requirements, implementation progress, terminal errors, test results, and requested guidance or code where required.

No external AI model is required at runtime by the BoxSelect application.

---

## 3. How AI Was Used

### Project Planning

AI was initially asked to help plan a simple Django-based solution for the box selection problem.

The resulting design was intentionally kept relatively small and explainable:

- Django
- Django REST Framework
- SQLite
- Django ORM
- Django built-in testing framework
- A dedicated service module for box selection logic

The application does not use unnecessary infrastructure such as Redis, Celery, Kafka, microservices, or a separate frontend application.

---

### Backend Implementation

AI assistance was used to create and review:

- Django models
- Django REST Framework serializers
- ViewSets
- API routes
- Admin configuration
- Box selection service logic
- Validation and error handling
- Automated tests

The implementation was then pasted into the local project and executed in the development environment.

---

### Box Selection Logic

AI assistance was used to design the deterministic box selection algorithm.

The implemented logic checks:

1. Total order weight.
2. Maximum supported weight of each box.
3. Product dimensions.
4. Possible rotations of product dimensions.
5. Whether multiple products can fit using the documented simplified packing heuristic.
6. Selection of the smallest suitable box by internal volume.
7. Box cost as the secondary selection criterion.
8. Database ID as the final deterministic tie-breaker.

The implementation intentionally does **not** claim to solve general 3D bin packing or provide mathematically optimal packing.

---

## 4. Actual AI-Assisted Debugging

AI assistance was also used when problems were encountered during development.

### Issue 1 — Django Test Discovery

The initial test package was created under:

```text
shipping/tests/
```

Django test discovery encountered a naming conflict with an installed module named `tests`.

The test package was renamed to:

```text
shipping/shipping_tests/
```

After this change, Django successfully discovered the project tests.

---

### Issue 2 — Order Creation API Response

An API test initially failed because the serializer used to accept order creation data was also being used for the response.

The initial approach was reviewed after the test failure.

The implementation was changed so that:

- `OrderCreateSerializer` handles incoming order creation data.
- `OrderSerializer` handles the returned order representation.
- `OrderViewSet.create()` explicitly controls this input/output serializer flow.

The API was then tested again successfully.

---

## 5. Example Prompts Used

The development process included prompts such as:

> "I will build it here. There is a slight change in plans. Give all codes and I will paste it in VS Code. Be careful and do not make any mistakes."

Other prompts were used to:
- Move to the next implementation stage.
- Debug errors shown by the local environment.
- Review failed tests.
- Correct API behavior.
- Improve documentation and testing.

The prompts and responses in the actual ChatGPT conversation were used as development assistance rather than being treated as automatically correct.

---

## 6. Accepted AI Output

AI-generated suggestions were accepted when they matched the assignment requirements and worked correctly in the local project.

Examples include:

- Django model structure
- REST API structure
- Box selection service organization
- Rotation-aware dimension checking
- Serializer structure
- Automated test structure
- Django admin configuration
- Documentation structure

Accepted code was still run and verified locally.

---

## 7. Rejected or Modified AI Output

AI-generated output was not blindly accepted.

For example, the initial approach to the order serializer/API response did not resolve the failing test. The implementation was reviewed and modified so that the ViewSet explicitly used separate serializers for input and output.

The test-discovery setup was also modified after Django encountered a test-module naming conflict.

These changes demonstrate that AI output was reviewed against actual application behavior rather than being copied without verification.

---

## 8. Verification Process

The generated and modified code was verified using the local Django environment.

The following checks were performed:

```powershell
python manage.py check
```

The Django system check completed successfully.

The automated test suite was also executed:

```powershell
python manage.py test
```

The final test suite contains:

**26 automated tests**

The tests cover:

- Product creation
- Box creation
- Order creation
- Order items
- Box volume calculation
- Total order weight calculation
- Product rotation
- Dimension validation
- Weight limits
- Multiple suitable boxes
- Smallest-volume selection
- Cost tie-breaking
- Orders that cannot fit
- Empty orders
- API success responses
- API validation and failure responses

The final test execution completed successfully with:

```text
Ran 26 tests in 0.239s

OK
```

Detailed test output is documented separately in:

```text
TEST_OUTPUT.md
```

---

## 9. Human Review

AI was used as a development assistant, but the final implementation was reviewed by the developer.

The developer:

- Created and managed the local project environment.
- Pasted and executed the generated code.
- Reported actual errors and test failures.
- Verified fixes by rerunning the application and tests.
- Reviewed the project behavior.
- Made implementation decisions based on the assignment requirements.

AI assistance does not replace the developer's responsibility for understanding and verifying the submitted implementation.

---

## 10. Runtime AI Dependency

The final BoxSelect application does **not** require an AI API or external AI service to run.

The term "AI-Assisted" in this project refers to the development process.

The box recommendation itself is implemented as deterministic business logic so that the result is:

- Explainable
- Reproducible
- Testable
- Easy to verify

---

## 11. Important Note

This document describes the actual role of AI assistance during development.

No AI-generated chat transcript is being presented as an exported conversation.

The required ChatGPT conversation transcript will be exported directly from the actual conversation and included separately with the submission, as required by the assignment.