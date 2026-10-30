"""
问题 4 单元测试: MeetingRoom

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 MeetingRoom 对象上的多个属性
（例如 bookings 列表、total_hours_booked、free slots、utilization rate）
以验证会议室状态和冲突管理。

运行测试：
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        验证空会议室的初始状态。
        """
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertListEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)
        self.assertEqual(self.room.get_free_slots(), [(8, 18)])
        self.assertEqual(self.room.get_utilization_rate(), 0.0)

    def test_single_booking_multi_attributes(self):
        """
        测试创建一个有效预订。
        验证 bookings 列表、total_hours_booked、utilization rate 和 free slots。
        """
        self.assertTrue(self.room.book("B01", "Planning", 10, 12, 5))
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["title"], "Planning")
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_utilization_rate(), 0.2)
        self.assertEqual(self.room.get_free_slots(), [(8, 10), (12, 18)])

    def test_back_to_back_meetings_allowed(self):
        """
        测试有效的连续/背靠背会议 (例如 9-10 和 10-12) 不会引发冲突错误。
        验证两个预订成功后的多属性状态。
        """
        self.assertTrue(self.room.book("B01", "Standup", 9, 10, 4))
        self.assertTrue(self.room.book("B02", "Review", 10, 12, 6))
        self.assertEqual([b["booking_id"] for b in self.room.bookings], ["B01", "B02"])
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.get_free_slots(), [(8, 9), (12, 18)])

    def test_overlapping_booking_rejected(self):
        """
        测试重叠预订（例如 9-11 与 10-12, 或完全包含在 9-12 与 10-11 之间）
        应抛出 ValueError, 并保持会议室状态不变。
        """
        self.room.book("B01", "First", 9, 12, 5)
        with self.assertRaises(ValueError):
            self.room.book("B02", "Overlap", 10, 11, 5)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")

    def test_cancel_booking_updates_all_attributes(self):
        """
        测试取消预订是否能正确从 bookings 中移除，
        减少 total_hours_booked, 并恢复 free slots。
        """
        self.room.book("B01", "Morning", 9, 11, 4)
        self.room.book("B02", "Afternoon", 13, 15, 6)
        self.assertTrue(self.room.cancel("B01"))
        self.assertEqual([b["booking_id"] for b in self.room.bookings], ["B02"])
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_utilization_rate(), 0.2)
        self.assertEqual(self.room.get_free_slots(), [(8, 13), (15, 18)])

    def test_capacity_and_validation_exceptions(self):
        """
        测试边界情况和异常：
        - 参与人数超过容量 (ValueError)
        - 开始时间 >= 结束时间 (ValueError)
        - 预订 ID 重复 (ValueError)
        - 会议室处于维护状态时预订 (RuntimeError)
        - 取消不存在的预订 (KeyError)
        """
        with self.assertRaises(ValueError):
            self.room.book("BIG", "Too many", 9, 10, 11)
        with self.assertRaises(ValueError):
            self.room.book("BAD", "Bad time", 10, 10, 1)
        self.room.book("B01", "Valid", 9, 10, 1)
        with self.assertRaises(ValueError):
            self.room.book("B01", "Duplicate", 11, 12, 1)
        self.room.is_maintenance = True
        with self.assertRaises(RuntimeError):
            self.room.book("B02", "Closed", 11, 12, 1)
        with self.assertRaises(KeyError):
            self.room.cancel("MISSING")


if __name__ == "__main__":
    unittest.main()
