"""
问题 2单元测试: BankAccount

说明：
使用 Python 的 unittest 框架补全下面的测试方法。
你的测试方法必须断言 BankAccount 对象上的多个属性
（例如 balance、status、transaction_history、summary）以验证状态一致性。

运行测试：
    python -m unittest test_problem2.py -v
"""
import unittest
from problem2 import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """
        Set up test fixtures before each test method.
        在每个测试方法执行前设置测试夹具（test fixtures）。
        """
        self.account_empty = BankAccount("ACC001", "Alice", initial_balance=0.0, overdraft_limit=100.0)
        self.account_funded = BankAccount("ACC002", "Bob", initial_balance=200.0, overdraft_limit=50.0)

    def test_initial_state_multi_attributes(self):
        """
        验证新创建的账户是否正确初始化所有属性。
        检查 balance、owner、status、overdraft_limit、transaction_history 和 summary。
        """
        # 测试空账户
        self.assertEqual(self.account_empty.account_id, "ACC001")
        self.assertEqual(self.account_empty.owner, "Alice")
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.overdraft_limit, 100.0)
        self.assertListEqual(self.account_empty.transaction_history, [])
        self.assertEqual(self.account_empty.get_summary()["transaction_count"], 0)

        # 测试存款账户
        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 1)
        self.assertEqual(self.account_funded.transaction_history[0]["type"], "INITIAL_DEPOSIT")
        self.assertEqual(self.account_funded.get_summary()["owner"], "Bob")

    def test_deposit_updates_multiple_attributes(self):
        """
        测试存款是否正确更新 balance、transaction_history 和 summary
        """
        self.assertTrue(self.account_empty.deposit(150))
        self.assertEqual(self.account_empty.balance, 150.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account_empty.transaction_history[-1]["balance_after"], 150.0)
        self.assertEqual(self.account_empty.get_summary()["transaction_count"], 1)

    def test_withdrawal_within_balance_multi_attributes(self):
        """
        测试当余额充足时提款是否正确
        """
        self.assertTrue(self.account_funded.withdraw(50, fee=2.5))
        self.assertEqual(self.account_funded.balance, 147.5)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        transaction = self.account_funded.transaction_history[-1]
        self.assertEqual(transaction["type"], "WITHDRAWAL")
        self.assertEqual(transaction["fee"], 2.5)
        self.assertEqual(self.account_funded.get_summary()["transaction_count"], 2)

    def test_overdraft_withdrawal_and_status_transition(self):
        """
        测试使用透支保护的提款 (余额变为负数，但仍 >= -overdraft_limit)
        """
        self.assertTrue(self.account_empty.withdraw(50))
        self.assertEqual(self.account_empty.balance, -50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")
        self.assertEqual(self.account_empty.transaction_history[-1]["balance_after"], -50.0)
        self.assertEqual(self.account_empty.get_summary()["status"], "OVERDRAWN")

    def test_deposit_recovering_from_overdrawn_status(self):
        """
        测试当存款足以使余额 >= 0 时，状态从 OVERDRAWN 转回 ACTIVE。
        """
        self.account_empty.withdraw(50)
        self.account_empty.deposit(60)
        self.assertEqual(self.account_empty.balance, 10.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account_empty.get_summary()["transaction_count"], 2)

    def test_transfer_between_accounts_multi_attributes(self):
        """
        测试两个账户之间的资金转账。
        """
        self.assertTrue(self.account_funded.transfer_to(self.account_empty, 50, transfer_fee=5))
        self.assertEqual(self.account_funded.balance, 145.0)
        self.assertEqual(self.account_empty.balance, 50.0)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_funded.transaction_history[-1]["type"], "WITHDRAWAL")
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")

    def test_frozen_account_restrictions(self):
        """
        测试 FROZEN 账户在存款、取款和转账时会抛出 RuntimeError。
        """
        self.account_empty.freeze()
        self.assertEqual(self.account_empty.status, "FROZEN")
        with self.assertRaises(RuntimeError):
            self.account_empty.deposit(1)
        with self.assertRaises(RuntimeError):
            self.account_empty.withdraw(1)
        with self.assertRaises(RuntimeError):
            self.account_empty.transfer_to(self.account_funded, 1)
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertListEqual(self.account_empty.transaction_history, [])

    def test_invalid_operations_raise_exceptions(self):
        """
        测试异常处理。
        """
        with self.assertRaises(ValueError):
            BankAccount("BAD", "Alice", initial_balance=-1)
        with self.assertRaises(ValueError):
            self.account_empty.deposit(0)
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(-1)
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(1, fee=-1)
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(101)
        with self.assertRaises(TypeError):
            self.account_empty.transfer_to("not an account", 1)


if __name__ == "__main__":
    unittest.main()
