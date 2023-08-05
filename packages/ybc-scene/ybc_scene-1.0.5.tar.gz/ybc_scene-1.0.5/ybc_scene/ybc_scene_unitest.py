import unittest
import os
from ybc_scene import *
from ybc_exception import *


class MyTestCase(unittest.TestCase):
    path_pic = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'test.jpg')

    def test_scene_recog(self):
        self.assertEqual(scene_recog(MyTestCase.path_pic), [{'label_id': '室内', 'label_confd': '66%'}, {'label_id': '物品', 'label_confd': '33%'}])

    def test_object_recog(self):
        self.assertEqual(object_recog(MyTestCase.path_pic), [{'label_id': '杯子', 'label_confd': '54%'}, {'label_id': '茶杯', 'label_confd': '17%'}, {'label_id': '意式浓缩咖啡', 'label_confd': '12%'}, {'label_id': '室内', 'label_confd': '7%'}, {'label_id': '咖啡机', 'label_confd': '7%'}])

    def test_scene_recog_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用scene_recog方法时，'filename'参数不在允许范围内。$"):
            scene_recog('')

    def test_scene_recog_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用scene_recog方法时，'filename'参数类型错误。$"):
            scene_recog(1)

    def test_object_recog_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用object_recog方法时，'filename'参数不在允许范围内。$"):
            object_recog('')

    def test_object_recog_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用object_recog方法时，'filename'参数类型错误。$"):
            object_recog(1)


if __name__ == '__main__':
    unittest.main()
