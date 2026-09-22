# Test Output

## Test Summary

- Test framework: Django built-in test runner
- Total tests: 26
- Passed: 26
- Failed: 0
- Errors: 0
- Django system check: No issues
- Test execution time: 0.162 seconds

## Command

python manage.py test -v 2

## Full Output

(venv) PS C:\Users\dubey\OneDrive\Desktop\Internship_Project\BoxSelect> python manage.py test -v 2
Found 26 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, shipping
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length...OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying shipping.0001_initial... OK
System check identified no issues (0 silenced).
test_box_creation_api (shipping.shipping_tests.test_api.ShippingAPITests.test_box_creation_api) ... ok
test_empty_order_is_rejected (shipping.shipping_tests.test_api.ShippingAPITests.test_empty_order_is_rejected) ... ok
test_order_creation_api (shipping.shipping_tests.test_api.ShippingAPITests.test_order_creation_api) ... ok
test_order_detail_contains_items (shipping.shipping_tests.test_api.ShippingAPITests.test_order_detail_contains_items) ... ok
test_product_creation_api (shipping.shipping_tests.test_api.ShippingAPITests.test_product_creation_api) ... ok
test_product_rejects_negative_dimension (shipping.shipping_tests.test_api.ShippingAPITests.test_product_rejects_negative_dimension) ... ok
test_recommend_box_api_success (shipping.shipping_tests.test_api.ShippingAPITests.test_recommend_box_api_success) ... ok
test_recommend_box_returns_failure_when_no_box_fits (shipping.shipping_tests.test_api.ShippingAPITests.test_recommend_box_returns_failure_when_no_box_fits) ... ok
test_empty_order_raises_error (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_empty_order_raises_error) ... ok
test_lower_cost_breaks_equal_volume_tie (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_lower_cost_breaks_equal_volume_tie) ... ok
test_no_suitable_box_raises_error (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_no_suitable_box_raises_error) ... ok
test_order_does_not_fit_when_total_length_is_too_large (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_order_does_not_fit_when_total_length_is_too_large) ... ok
test_order_fits_inside_box (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_order_fits_inside_box) ... ok
test_product_can_fit_after_rotation (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_product_can_fit_after_rotation) ... ok
test_product_does_not_fit_when_dimensions_are_too_large(shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_product_does_not_fit_when_dimensions_are_too_large) ... ok
test_select_box_chooses_smallest_volume (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_select_box_chooses_smallest_volume) ... ok
test_select_box_rejects_weight_limit (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_select_box_rejects_weight_limit) ... ok
test_total_weight_is_calculated_correctly (shipping.shipping_tests.test_box_selector.BoxSelectorTests.test_total_weight_is_calculated_correctly) ... ok
test_box_creation (shipping.shipping_tests.test_models.BoxModelTests.test_box_creation) ... ok
test_box_volume (shipping.shipping_tests.test_models.BoxModelTests.test_box_volume) ... ok
test_order_creation (shipping.shipping_tests.test_models.OrderModelTests.test_order_creation) ... ok
test_order_item_creation (shipping.shipping_tests.test_models.OrderModelTests.test_order_item_creation) ... ok
test_order_item_string_representation (shipping.shipping_tests.test_models.OrderModelTests.test_order_item_string_representation) ... ok
test_product_protects_existing_order_items (shipping.shipping_tests.test_models.OrderModelTests.test_product_protects_existing_order_items) ... ok
test_product_creation (shipping.shipping_tests.test_models.ProductModelTests.test_product_creation) ... ok
test_product_string_representation (shipping.shipping_tests.test_models.ProductModelTests.test_product_string_representation) ... ok

----------------------------------------------------------------------
Ran 26 tests in 0.162s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
(venv) PS C:\Users\dubey\OneDrive\Desktop\Internship_Project\BoxSelect> 