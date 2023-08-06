import unittest
from ybc_speech import *


class MyTestCase(unittest.TestCase):
    def test_voice2text(self):
        self.assertEqual('原辅导你好', voice2text('test.wav'))

    def test_text2voice(self):
        filename = text2voice('欢迎参加编程课', 'temp.wav')
        self.assertEqual('欢迎参加编程课', voice2text(filename))

    def test_voice2text_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用voice2text方法时，'filename'参数类型错误。$"):
            voice2text(1)

    def test_voice2text_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用voice2text方法时，'filename'参数不在允许范围内。$"):
            voice2text('')

    def test_record_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError,
                                    "^参数类型错误 : 调用record方法时，'filename'、'seconds'、'to_dir'、'rate'、'channels'、'chunk'参数类型错误。$"):
            record(1, '2', 1, 'a', 'a', 'a')

    def test_record_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用record方法时，'filename'、'seconds'参数不在允许范围内。$"):
            record('', 0)

    def test_text2voice_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError,
                                    "^参数类型错误 : 调用text2voice方法时，'text'、'filename'、'speaker'、'speed'、'aht'、'apc'、'volume'、'_format'参数类型错误。$"):
            text2voice(1, 1, 'specker', 'speed', 'aht', 'apc', 'volume', '_format')

    def test_text2voice_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError,
                                    "^参数数值错误 : 调用text2voice方法时，'text'、'filename'、'speaker'、'speed'参数不在允许范围内。$"):
            text2voice('', '', 3, 3, 4)


if __name__ == '__main__':
    unittest.main()
