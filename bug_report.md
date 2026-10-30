# 问题/错误报告 Bug Report

该报告记录了在有错误程序中发现的问题（bugs），包括失败的测试用例、根本原因分析（root cause analysis）以及已应用的修复方案。

---

## 问题/错误报告 1：会议室背靠背预订被错误拒绝

### 1. 测试程序 Program Under Test
- **File:** `problem4.py`
- **Class / Function:** `MeetingRoom.book()`

### 2. 失败的测试用例 Failing Test Case
```python
def test_back_to_back_meetings_allowed(self):
    self.room.book("B01", "Standup", 9, 10, 4)
    self.room.book("B02", "Review", 10, 12, 6)
```

**测试输出 / 错误信息：**
```text
ValueError: Time slot [10, 12] conflicts with booking 'B01' [9, 10]
```

### 3. 根本原因分析 Root Cause Analysis
- **预期行为：** 时间区间 `[9, 10)` 和 `[10, 12)` 只是端点相接，应允许连续预订。
- **实际行为：** 原逻辑将 `end_time == existing_start_time` 或 `start_time == existing_end_time` 也视为冲突。
- **根本原因：** 冲突判断使用了严格的“完全不相交”条件，未采用半开区间的重叠判断。

### 4. 代码修复与差异 Code Fix & Diff
```diff
- if not (end_time < b["start_time"] or start_time > b["end_time"]):
+ if start_time < b["end_time"] and end_time > b["start_time"]:
```

## 问题/错误报告 2：数据聚合的最小值和最大值相反

### 1. 测试程序 Program Under Test
- **File:** `problem5.py`
- **Class / Function:** `clean_and_aggregate()`

### 2. 失败的测试用例 Failing Test Case
```python
min_result = clean_and_aggregate(sample_sales, "region", "sales", "min")
max_result = clean_and_aggregate(sample_sales, "region", "sales", "max")
assert min_result["North"] == 100.0
assert max_result["North"] == 200.0
```

**测试输出 / 错误信息：**
```text
AssertionError: 200.0 != 100.0 within 7 places (100.0 difference)
```

### 3. 根本原因分析 Root Cause Analysis
- **预期行为：** `min` 返回组内最小值，`max` 返回组内最大值。
- **实际行为：** `min` 调用了 `max(values)`，而 `max` 调用了 `min(values)`。
- **根本原因：** 两个聚合分支的内置函数被写反。

### 4. 代码修复与差异 Code Fix & Diff
```diff
- elif agg_op == "min": val = max(values)
- elif agg_op == "max": val = min(values)
+ elif agg_op == "min": val = min(values)
+ elif agg_op == "max": val = max(values)
```

## 问题/错误报告 3：空数据集未按契约报错

### 1. 测试程序 Program Under Test
- **File:** `problem5.py`
- **Class / Function:** `clean_and_aggregate()`

### 2. 失败的测试用例 Failing Test Case
```python
with self.assertRaises(ValueError):
    clean_and_aggregate([], group_by="region", metric="sales")
```

**测试输出 / 错误信息：**
```text
AssertionError: ValueError not raised
```

### 3. 根本原因分析 Root Cause Analysis
- **预期行为：** 函数文档声明空 `records` 应抛出 `ValueError`。
- **实际行为：** 原实现返回空字典 `{}`。
- **根本原因：** 进入记录循环前没有验证 `records` 的类型和非空性。

### 4. 代码修复与差异 Code Fix & Diff
```diff
+ if not isinstance(records, list):
+     raise TypeError("records must be a list")
+ if not records:
+     raise ValueError("records cannot be empty")
```
