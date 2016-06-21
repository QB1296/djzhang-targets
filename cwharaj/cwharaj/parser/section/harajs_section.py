# coding=utf-8
from cwharaj.parser.section.section_item import SectionItem, TagItem
import logging


class HarajsSection(object):
    def __init__(self, sections, item_db):
        super(HarajsSection, self).__init__()
        self.sections = sections
        self.item_db = item_db
        self.section_item = SectionItem(self.item_db)
        self.tag_item = TagItem()

    def get_section_item(self):
        if len(self.sections) >= 4:
            logging.debug("special sections, count: {}".format(len(self.sections)))
            return None

        """
        length is only 1, that the section is tag_R.
        """
        if len(self.sections) == 1:
            self._get_tag_r(self.sections[0])
            pass

        """
        length is 3 or 2.
        """
        self.get_common_tag_item()

        """
        finally,generate section item.
        """
        self.section_item.set_item(self.tag_item)

        return self.section_item

    def _get_tag_r(self, name):
        _item = self.item_db.get_section(name)
        self.tag_item.tag_R = _item['id']
        self.section_item.type_ads_other_final = _item['Contents']

    def get_common_tag_item(self):
        self.get_tag_FF()

        if self.tag_item.tag_FF:
            if len(self.sections) == 2:
                pass
            elif len(self.sections) == 3:
                pass

        for x in xrange(len(self.sections) - 1, -1, -1):
            _split = self.sections[x].split(' ')
            _pre_x = x - 1
            if (len(_split) == 2) and (x != 0):
                _tag_FF = self.parse_tagFF(_split, _pre_x)
                # if _tag_FF:

    def get_tag_FF(self):
        for x in xrange(len(self.sections) - 1, -1, -1):
            _split = self.sections[x].split(' ')
            _pre_x = x - 1
            if (len(_split) == 2) and (x != 0):
                _tag_FF = self.parse_tagFF(_split, _pre_x)
                self.tag_item.tag_FF_index = x
                self.tag_item.tag_FF = _tag_FF
                break

    def parse_tagFF(self, _split, pre_index):
        """
        :param self.sections:  section list
        :param _split:     such as "كامري 2016"
        :param pre_index:  if split's index is 3, pre_index is 2
        :param item_db:    database that implements query.
        :return:           the table year's id on the databse
        """
        _pre_section = self.sections[pre_index]
        _pre_split = _pre_section.split(' ')
        if len(_pre_split) != 1:
            return None

        _year_index = self.get_year_index(_split)
        _name_index = 0
        if _year_index == 0:
            _name_index = 1

        _year = _split[_year_index]
        _tag_f_name = _split[_name_index]

        _pre_tag_f_name = _pre_split[0]
        if _tag_f_name != _pre_tag_f_name:
            return None

        _tags_FF = self.item_db.get_year_id(_year)
        return _tags_FF

    def get_year_index(self, _split):
        for index, item in enumerate(_split):
            if len(item) == 4 and item.isdigit():
                return index
