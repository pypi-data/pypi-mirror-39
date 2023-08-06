import biztime
import unittest
from datetime import date, datetime, time, timedelta


class TestHelperFunctions(unittest.TestCase):

  def test_div_round_RoundsUp(self):
    self.assertEqual(biztime.div_round(5, 2), 3)
    self.assertEqual(biztime.div_round(5, 3), 2)

  def test_div_round_RoundsDown(self):
    self.assertEqual(biztime.div_round(1, 3), 0)
    self.assertEqual(biztime.div_round(5, 4), 1)

  def test_div_round_NoRound(self):
    self.assertEqual(biztime.div_round(4, 2), 2)
    self.assertEqual(biztime.div_round(0, 2), 0)

  def test_div_round_DivideByZeroRaisesError(self):
    with self.assertRaises(ZeroDivisionError):
      biztime.div_round(1, 0)


class TestBizTime(unittest.TestCase):

  def setUp(self):
    self.bt_blank = biztime.BizTime({
      'biz_start': time(0, 0),
      'biz_end': time(23, 59, 59),
    })
    self.bt_basic = biztime.BizTime({
      'biz_start': time(9, 0),
      'biz_end': time(17, 0),
      'weekend': [5, 6],
      'holidays': [
        date(2018, 12, 24),
        date(2018, 12, 25),
        date(2019, 1, 1),
      ]
    })

  def test_is_biz_day_businessDayReturnsTrue(self):
    self.assertTrue(self.bt_blank.is_biz_day(date(2018, 12, 10)))

  def test_is_biz_day_weekendReturnsFalse(self):
    self.assertFalse(self.bt_basic.is_biz_day(date(2018, 12, 9)))

  def test_is_biz_day_holidayReturnsFalse(self):
    self.assertFalse(self.bt_basic.is_biz_day(date(2018, 12, 25)))

  def test_is_biz_day_holidayWeekendReturnsFalse(self):
    bt_loc = biztime.BizTime({'holidays': [date(2018, 12, 10)]})
    self.assertFalse(bt_loc.is_biz_day(date(2018, 12, 10)))

  def test_time_diff_invalidInputsRaisesError(self):
    with self.assertRaises(TypeError):
      self.bt_blank.time_diff(
          datetime(2018, 1, 1, 8, 0, 0), datetime(2018, 1, 2, 8, 0, 0))
    with self.assertRaises(ValueError):
      self.bt_blank.time_diff(time(8, 0, 0), time(3, 0, 0))

  def test_time_diff_validInputReturnsTimedelta(self):
    test_cases = [
      [time(0, 0, 0), time(8, 0, 0), timedelta(hours=8)],
      [time(10, 23, 0), time(15, 11, 0), timedelta(hours=4, minutes=48)],
    ]
    for t in test_cases:
      self.assertEqual(self.bt_blank.time_diff(t[0], t[1]), t[2])

  def test_date_diff_invalidInputsRaisesError(self):
    with self.assertRaises(TypeError):
      self.bt_blank.date_diff(time(8, 0, 0), time(10, 0, 0))
    with self.assertRaises(ValueError):
      self.bt_blank.date_diff(
          datetime(2018, 1, 2, 8, 0, 0), datetime(2018, 1, 1, 8, 0, 0))

  def test_date_diff_validInputReturnsTimedelta_singleDay(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 10, 9, 0, 0),
            datetime(2018, 12, 10, 12, 0, 0)
        ),
        timedelta(hours=3)
    )

  def test_date_diff_validInputReturnsTimedelta_twoDays(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 10, 9, 0, 0),
            datetime(2018, 12, 11, 12, 0, 0)
        ),
        timedelta(hours=11)
    )

  def test_date_diff_validInputReturnsTimedelta_threeDays(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 10, 9, 0, 0),
            datetime(2018, 12, 12, 17, 0, 0)
        ),
        timedelta(hours=24)
    )

  def test_date_diff_validInputReturnsTimedelta_oneWeek(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 9, 8, 0, 0),
            datetime(2018, 12, 16, 8, 0, 0)
        ),
        timedelta(hours=40)
    )

  def test_date_diff_validInputReturnsTimedelta_oneWeekWithHoliday(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 30, 8, 0, 0),
            datetime(2019, 1, 5, 8, 0, 0)
        ),
        timedelta(hours=32)
    )

  def test_date_diff_validInputReturnsTimedelta_incompleteDay(self):
    self.assertEqual(
        self.bt_basic.date_diff(
            datetime(2018, 12, 10, 10, 42, 0),
            datetime(2018, 12, 12, 9, 18, 52)
        ),
        timedelta(hours=14, minutes=36, seconds=52)
    )


if __name__ == '__main__':
  unittest.main(verbosity=2)
