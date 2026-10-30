"""
问题 3 单元测试: Order

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 Order 对象上的多个属性
（例如 subtotal、discount_amount、tax_amount、shipping_fee、final_total、status）
以验证在各种条件下的状态一致性。

运行测试：
    python -m unittest test_problem3.py -v
"""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    def test_add_items_recalculates_multiple_attributes(self):
        self.regular_order.add_item("Book", 20, 2, "general")
        self.assertEqual(self.regular_order.subtotal, 40.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 3.2)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.final_total, 49.19)
        self.assertEqual(self.regular_order.get_summary()["item_count"], 2)

    def test_tier_and_coupon_discount_with_free_shipping(self):
        self.gold_order.add_item("Laptop accessory", 100, category="general")
        self.gold_order.apply_coupon("save10")
        self.assertEqual(self.gold_order.subtotal, 100.0)
        self.assertEqual(self.gold_order.discount_amount, 19.0)
        self.assertEqual(self.gold_order.tax_amount, 6.48)
        self.assertEqual(self.gold_order.shipping_fee, 0.0)
        self.assertEqual(self.gold_order.final_total, 87.48)
        self.assertEqual(self.gold_order.applied_coupon, "SAVE10")

    def test_grocery_is_not_taxed_and_remove_updates_totals(self):
        self.silver_order.add_item("Groceries", 30, category="grocery")
        self.silver_order.add_item("Notebook", 20, category="general")
        self.silver_order.remove_item("Notebook")
        self.assertEqual(self.silver_order.subtotal, 30.0)
        self.assertEqual(self.silver_order.discount_amount, 1.5)
        self.assertEqual(self.silver_order.tax_amount, 0.0)
        self.assertEqual(self.silver_order.shipping_fee, 5.99)
        self.assertEqual(self.silver_order.final_total, 34.49)
        self.assertEqual(self.silver_order.get_summary()["item_count"], 1)

    def test_checkout_locks_pending_order(self):
        self.regular_order.add_item("Pen", 5)
        self.assertTrue(self.regular_order.checkout())
        self.assertEqual(self.regular_order.status, "PAID")
        self.assertEqual(self.regular_order.get_summary()["status"], "PAID")
        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Paper", 3)
        with self.assertRaises(RuntimeError):
            self.regular_order.cancel()

    def test_invalid_operations_and_cancel(self):
        with self.assertRaises(ValueError):
            Order("BAD", customer_tier="vip")
        with self.assertRaises(ValueError):
            self.regular_order.checkout()
        with self.assertRaises(ValueError):
            self.regular_order.add_item("Bad", 0)
        self.regular_order.add_item("Book", 10)
        with self.assertRaises(ValueError):
            self.regular_order.apply_coupon("INVALID")
        self.assertTrue(self.regular_order.cancel())
        self.assertEqual(self.regular_order.status, "CANCELLED")
        with self.assertRaises(RuntimeError):
            self.regular_order.apply_coupon("SAVE10")


if __name__ == "__main__":
    unittest.main()
