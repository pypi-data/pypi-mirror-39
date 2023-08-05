import os
import ybc_speech as speech
import sys
from pydub import AudioSegment
from ybc_exception import *
os.environ['PATH'] = '/usr/bin'


def analysis(filename):
    """
    功能：分析微信语音内容转换成文字。
    参数 filename: 微信语音文件名。
    返回：转换成的文字
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    try:
        sound = AudioSegment.from_mp3(filename).set_frame_rate(16000)
        sound.export('tmp.wav', format = "wav")
        text = speech.voice2text('tmp.wav')
        return text
    except Exception as e:
        raise InternalError(e, 'ybc_switch')


if __name__ == '__main__':
    print(analysis('1.mp3'))