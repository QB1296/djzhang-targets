# coding=utf-8
import logging
import time

from cwharaj.parser.utils.timer_util import TimerUtil


class OpensooqCommentDateItem(object):
    """
    Converting the string date to time using 'GMT'.
    """
    tm_minute = 0
    tm_hour = 0
    tm_day = 0
    tm_week = 0
    tm_month = 0
    tm_year = 0

    lang = [
        'دقيقة',  # ___Three minutes ago___
        'ساعة',  # ___Three hours ago___
        ' ساعات',  # __3 hours ago__
        'أيام',  # __3 days ago__
        'اسابيع',  # __Since 3(x) weeks__
        'أشهر',  # __3 months ago__
    ]

    value = [
        60,  # => $lang['minute'],
        60 * 60,  # => $lang['hour'],
        60 * 60,  # => $lang['hour'],
        24 * 60 * 60,  # => $lang['day'],
        24 * 60 * 60 * 7,  # => $lang['week'],
        30 * 24 * 60 * 60,  # => $lang['month'],
    ]

    def __init__(self):
        super(OpensooqCommentDateItem, self).__init__()

    def maketime(self, split):
        time_type = split[1]
        time_value = int(split[0])

        if time_type in self.lang:
            index = self.lang.index(time_type)

            if index == 0:
                self.tm_minute = time_value
            elif index == 1:
                self.tm_hour = time_value
            elif index == 2:
                self.tm_hour = time_value
            elif index == 3:
                self.tm_day = time_value
            elif index == 4:
                self.tm_week = time_value
            elif index == 5:
                self.tm_month = time_value

            logging.debug("  make time {} for opensooq sucessfully".format(split))

        return self._make_time()

    def _make_time(self):
        seconds = self.tm_minute * self.value[0] + \
                  self.tm_hour * self.value[1] + \
                  self.tm_day * self.value[2] + \
                  self.tm_month * self.value[3] + \
                  self.tm_year * self.value[4]

        return int(time.time()) - seconds


class OpensooqCommentDateUtil(TimerUtil):
    def __init__(self):
        super(OpensooqCommentDateUtil, self).__init__()

    def get_time_for_opensooq_comment(self, comment_date):
        """
        Converting string time to int.
        :param comment_date is 'منذ 6 أشهر'
        :                     6 months ago
        :return:
        """

        if comment_date == '':
            return self._get_default_time()

        comment_date = OpensooqCommentDateUtil.get_comment_date(comment_date)
        _offset = self._get_special_comment_date(comment_date)
        if _offset:
            return int(time.time()) - _offset

        split = comment_date.split(' ')
        if len(split) == 1:
            logging.debug("  make time {} for harajs failure".format(split))
            return int(time.time()) + self._get_utc_offset()

        return OpensooqCommentDateItem().maketime(split)

    def _get_special_comment_date(self, comment_date):
        _special_comment_date = {
            "ساعة": 60 * 60,  # About an hour ago
            "ساعتين": 60 * 60 * 2,  # Two hours ago
            # "3 ساعة": -1,  # ___Three hours ago___
            # "3 ساعات": -1,  # __3 hours ago__
            "يوم": 24 * 60 * 60,  # one day ago
            "يومين": 24 * 60 * 60 * 2,  # Two days ago
            # "3 أيام": -1,  # __3 days ago__
            "أسبوع": 24 * 60 * 60 * 7,  # a week ago
            "أسبوعين": 24 * 60 * 60 * 7 * 2,  # Two weeks ago
            # "3 اسابيع": -1,  # __Since 3(x) weeks__
            "شهر": 30 * 24 * 60 * 60,  # About a month ago
            "شهرين": 30 * 24 * 60 * 60 * 2,  # Two months ago
            # "3 أشهر": -1,  # __3 months ago__
            "سنة": 365 * 24 * 60 * 60,  # A year ago
            "سنتين": 365 * 24 * 60 * 60 * 2,  # Two years ago
        }
        if comment_date in _special_comment_date.keys():
            return _special_comment_date[comment_date]

    @classmethod
    def get_comment_date(self, text):
        return text.replace('منذ', '').replace("\n", "").replace("\r", "").strip()

    def get_time_for_opensooq_member_timeregister(self, _member_timeregister):
        """
        Converting string time to int.
        :param _member_timeregister is 'تاريخ الانضمام  19/07/2013'('Join date 19/07/2013')
        :return:
        """

        if _member_timeregister == '':
            return self._get_default_time()

        _member_timeregister = _member_timeregister.strip()

        today = time.strptime(_member_timeregister, "%d/%m/%Y")
        time.tzset()
        int_time = time.mktime(today)

        return int_time + self._get_utc_offset()

    def get_time_for_opensooq_time_added(self, _time_added):
        """
        Converting string time to int.
        :param _time_added is 'تاريخ النشر: 2016.06.28'('Published: 2016.06.28')
        :return:
        """

        if _time_added == '':
            return self._get_default_time()

        _time_added = _time_added.replace("\n", "").replace("\r", "").strip()

        today = time.strptime(_time_added, "%Y.%m.%d")
        time.tzset()
        int_time = time.mktime(today)

        return int_time + self._get_utc_offset()
