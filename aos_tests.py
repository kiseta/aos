import unittest
import aos_methods as methods


class AOSPositiveTestCases(unittest.TestCase):

    @staticmethod
    def test_aos():
        methods.setup()
        methods.create_new_user()
        methods.checkout_shopping_cart()
        methods.validate_order()
        methods.log_out()
        methods.log_in()
        methods.validate_user_login()
        methods.delete_account()
        methods.log_in()
        methods.validate_user_deleted()
        methods.teardown()