# coding=utf-8
import base64
import requests
import wave
import pyaudio
import os
import time
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__TTS_URL = __PREFIX + ybc_config.uri + '/text2voice'
__ASR_URL = __PREFIX + ybc_config.uri + '/speech'

__RATE = 16000
__FORMAT_TYPE = 2
__SECONDS = 5
__CHANNELS = 1
__CHUNK = 1024
__SPEAKER = 1
__SPEED = 1
__AHT = 0
__APC = 58
__VOLUME = 100
__FORMAT = 2


def voice2text(filename=''):
    """
    功能：把语音文件转换成文字。

    参数 filename 是当前目录下期望转换成文字的语音文件的名字，

    可选参数 rate 是语音文件的采样率，1 代表 16000，0 代表 8000，默认为 1，

    可选参数 format_type 是语音文件的类型，默认 PCM 格式，

    返回：转换成的文字。
    """
    error_msg = "'filename'"
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    if not filename:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        rate = 1
        format_type = 'PCM'

        url = __ASR_URL
        filepath = os.path.abspath(filename)
        data = {}
        data['format'] = format_type
        data['sampleRate'] = rate
        files = {
            'file': open(filepath, 'rb')
        }
        for i in range(3):
            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                res = r.json()
                if res['data']:
                    files['file'].close()
                    return res['data']
                else:
                    files['file'].close()
                    return "无法识别您的语音哦～"
        files['file'].close()
        raise ConnectionError('转换语音文件失败', r._content)

    except Exception as e:
        raise InternalError(e, 'ybc_speech')


def record(filename, seconds=__SECONDS, to_dir="./", rate=__RATE, channels=__CHANNELS, chunk=__CHANNELS):
    """
    功能：录制音频文件。

    参数 filename 是录制生成的语音文件的名字，

    可选参数 seconds 是录制时长（单位：秒），默认 5 秒，

    可选参数 to_dir 是存放语音文件的目录，默认为当前目录，

    可选参数 rate 是录制采样率，1 代表 16000，0 代表 8000，默认为 1，

    可选参数 channels 是声道，默认 1，

    可选参数 chunk 是一次读取的字节数，默认 1024，

    返回：录制的音频文件的路径。
    """
    error_flag = 1
    error_msg = ""
    # 参数类型正确性判断
    if not isinstance(filename, str):
        error_flag = -1
        error_msg = "'filename'"
    if not isinstance(seconds, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'seconds'"
    if not isinstance(to_dir, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'to_dir'"
    if not isinstance(rate, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'rate'"
    if not isinstance(channels, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'channels'"
    if not isinstance(chunk, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'chunk'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    # 参数取值正确性判断
    if not filename:
        error_flag = -1
        error_msg = "'filename'"

    if seconds <= 0:
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'seconds'"
    if error_flag == -1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paInt16,
                         channels=channels,
                         rate=rate,
                         input=True,
                         frames_per_buffer=chunk)

        print("* 开始录制")

        save_buffer = []
        for i in range(0, int(rate / chunk * seconds)):
            audio_data = stream.read(chunk, exception_on_overflow=False)
            save_buffer.append(audio_data)

        print("* 结束录制")

        # stop
        stream.stop_stream()
        stream.close()
        pa.terminate()

        if to_dir.endswith('/'):
            file_path = to_dir + filename
        else:
            file_path = to_dir + "/" + filename

        # save file
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16, ))
        wf.setframerate(rate)
        # join 前的类型
        wf.writeframes(b''.join(save_buffer))
        wf.close()

        return file_path
    except Exception as e:
        raise InternalError(e, 'ybc_speech')


def text2voice(text, filename, speaker=__SPEAKER, speed=__SPEED, aht=__AHT, apc=__APC, volume=__VOLUME,
               _format=__FORMAT):
    """
    功能：把文字转换成语音。

    参数 text 是待转换的文字，

    参数 filename 是生成的语音文件的名字，

    可选参数 speaker 是发音人，1 代表小刚（男声），2 代表小云（女声），默认为1，

    可选参数 speed 是语速，1 代表正常速度，0.5 代表慢速，2 代表快速，默认为1，

    可选参数 aht 是音高，默认为 0，

    可选参数 apc 是音色，默认为 58，

    可选参数 volume 是音量，默认为 100，

    可选参数 _format 是语音文件的格式，1 代表 PCM，2 代表 WAV，3代表 MP3，默认为 2 ，

    返回：生成的语音文件的名字。
    """
    error_flag = 1
    error_msg = ""
    # 参数类型正确性判断
    if not isinstance(text, str):
        error_flag = -1
        error_msg = "'text'"
    if not isinstance(filename, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(speaker, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speaker'"
    if not (isinstance(speed, int) or isinstance(speed, float)):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speed'"
    if not isinstance(aht, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'aht'"
    if not isinstance(apc, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'apc'"
    if not isinstance(volume, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'volume'"
    if not isinstance(_format, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'_format'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    # 参数取值正确性判断
    if not text:
        error_flag = -1
        error_msg = "'text'"
    if not filename:
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'filename'"
    if speaker not in (1, 2):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speaker'"
    if speed not in (0.5, 1, 1.5, 2):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speed'"
    if _format not in (1, 2, 3):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'_format'"
    if error_flag == -1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        if speaker == 1:
            speaker = 'xiaogang'
        elif speaker == 2:
            speaker = 'xiaoyun'
        else:
            speaker = 'xiaogang'

        if speed == 1:
            speed = 0
        elif speed == 0.5:
            speed = -250
        elif speed == 1.5:
            speed = 250
        elif speed == 2:
            speed = 500
        else:
            speed = 0

        if _format == 2:
            _format = 'WAV'
        elif _format == 1:
            _format = 'PCM'
        elif _format == 3:
            _format = 'MP3'
        else:
            _format = 'WAV'

        rate = 1

        url = __TTS_URL

        data = {}
        data['text'] = text
        data['voice'] = speaker
        data['format'] = _format
        data['sampleRate'] = rate
        data['volume'] = volume
        data['speechRate'] = speed
        data['pitchRate'] = aht

        headers = {'content-type': "application/json"}

        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.json()
                if res['data']:
                    b64_data = base64.b64decode(res['data'])
                    with open(filename, 'wb') as f:
                        f.write(b64_data)
                    return filename

        raise ConnectionError('获取音频失败，无法播放', r._content)
    except Exception as e:
        raise InternalError(e, 'ybc_speech')


def speak(text='', speaker=__SPEAKER, speed=__SPEED, aht=__AHT, apc=__APC):
    """
    功能：朗读一段文字。

    参数 text 是待朗读的文字，

    可选参数 speaker 是发音人，1 代表小刚（男声），2 代表小云（女声），默认为1，

    可选参数 speed 是语速，1 代表正常速度，0.5 代表慢速，2 代表快速，默认为1，

    可选参数 aht 是音高，默认为 0，

    可选参数 apc 是音色，默认为 58，

    返回：无。
    """
    error_flag = 1
    error_msg = ""
    # 参数类型正确性判断
    if not isinstance(text, str):
        error_flag = -1
        error_msg = "'text'"
    if not isinstance(speaker, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speaker'"
    if not isinstance(speed, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speed'"
    if not isinstance(aht, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'aht'"
    if not isinstance(apc, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'apc'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    # 参数取值正确性判断
    if not text:
        error_flag = -1
        error_msg = "'text'"
    if speaker not in (1, 2):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speaker'"
    if speed not in (0.5, 1, 1.5, 2):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'speed'"
    if error_flag == -1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        if text:
            filename = str(int(time.time())) + '_tmp.wav'
            res1 = text2voice(text, filename, speaker, speed, aht, apc)
        os.system(filename)
        if len(text) <= 10:
            time.sleep(4)
        elif len(text) <= 20:
            time.sleep(5)
        elif len(text) <= 30:
            time.sleep(6)
        elif len(text) <= 40:
            time.sleep(7)
    except Exception as e:
        raise InternalError(e, 'ybc_speech')


def main():
    # text2voice('猿辅导你好', 'test.wav')
    # voice2text('test.wav')
    speak('猿辅导你好')


if __name__ == '__main__':
    main()
