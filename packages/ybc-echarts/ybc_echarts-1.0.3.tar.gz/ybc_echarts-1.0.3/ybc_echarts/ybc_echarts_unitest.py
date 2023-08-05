# coding=utf-8
import unittest
import ybc_browser as browser
from ybc_echarts import *


class MyTestCase(unittest.TestCase):
    def test_get_province_typeError(self):
        with self.assertRaises(ParameterTypeError):
            Geo(123, 123)


def main():
    geo = Geo('地图主标题', '地图副标题', title_pos='center', width=1600, height=800)
    geo.add(['北京朝阳', '吉林长春'], [7, 2], geo_cities_coords={'北京朝阳': [116.44, 39.92], '吉林长春': [125.32, 43.9]})
    file_name = 'my.html'
    geo.render(file_name)
    browser.open_local_page(file_name)


if __name__ == '__main__':
    main()
    unittest.main()