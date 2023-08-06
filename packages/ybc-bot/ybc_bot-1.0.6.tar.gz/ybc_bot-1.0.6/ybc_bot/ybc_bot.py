import pyaudio
import requests
import webrtcvad
import ybc_config
import ybc_speech
from ybc_exception import *
import collections
import sys
import time
import wave
from array import array
from struct import pack

__PREFIX = ybc_config.config['prefix']
__IDIOM_URL = __PREFIX + ybc_config.uri + '/bot'


def listen(filename=''):
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")
    if filename == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")

    try:
        __FORMAT = pyaudio.paInt16
        __CHANNELS = 1
        __RATE = 16000
        __CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
        __PADDING_DURATION_MS = 1500  # 1 sec judgement
        __CHUNK_SIZE = int(__RATE * __CHUNK_DURATION_MS / 1000)  # chunk to read
        __CHUNK_BYTES = __CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
        __NUM_PADDING_CHUNKS = int(__PADDING_DURATION_MS / __CHUNK_DURATION_MS)
        __NUM_WINDOW_CHUNKS = int(400 / __CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge
        __NUM_WINDOW_CHUNKS_END = __NUM_WINDOW_CHUNKS * 2
        __START_OFFSET = int(__NUM_WINDOW_CHUNKS * __CHUNK_DURATION_MS * 0.5 * __RATE)

        def _record_to_file(path, data, sample_width):
            """Records from the microphone and outputs the resulting data to 'path'"""
            data = pack('<' + ('h' * len(data)), *data)
            wf = wave.open(path, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)
            wf.setframerate(__RATE)
            wf.writeframes(data)
            wf.close()

        def _normalize(snd_data):
            """Average the volume out"""
            maximum = 32767  # 16384
            times = float(maximum) / max(abs(i) for i in snd_data)
            r = array('h')
            for i in snd_data:
                r.append(int(i * times))
            return r

        vad = webrtcvad.Vad(1)
        pa = pyaudio.PyAudio()
        stream = pa.open(format=__FORMAT, channels=__CHANNELS, rate=__RATE, input=True, start=False,
                         frames_per_buffer=__CHUNK_SIZE)
        got_a_sentence = False
        leave = False

        while not leave:
            ring_buffer = collections.deque(maxlen=__NUM_PADDING_CHUNKS)
            triggered = False
            ring_buffer_flags = [0] * __NUM_WINDOW_CHUNKS
            ring_buffer_index = 0
            ring_buffer_flags_end = [0] * __NUM_WINDOW_CHUNKS_END
            ring_buffer_index_end = 0
            raw_data = array('h')
            index = 0
            start_point = 0
            start_time = time.time()
            print("小猿正在倾听...", end='')
            stream.start_stream()
            while not got_a_sentence and not leave:
                chunk = stream.read(__CHUNK_SIZE)
                # add WangS
                raw_data.extend(array('h', chunk))
                index += __CHUNK_SIZE
                time_use = time.time() - start_time
                active = vad.is_speech(chunk, __RATE)
                if start_point != 0:
                    sys.stdout.write('~' if active else ' ')
                ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                ring_buffer_index += 1
                ring_buffer_index %= __NUM_WINDOW_CHUNKS
                ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                ring_buffer_index_end += 1
                ring_buffer_index_end %= __NUM_WINDOW_CHUNKS_END

                # start point detection
                if not triggered:
                    ring_buffer.append(chunk)
                    num_voiced = sum(ring_buffer_flags)
                    if num_voiced > 0.80 * __NUM_WINDOW_CHUNKS:
                        sys.stdout.write("\nStart: ")
                        triggered = True
                        start_point = index - __CHUNK_SIZE * 20  # start point
                        ring_buffer.clear()
                # end point detection
                else:
                    ring_buffer.append(chunk)
                    num_unvoiced = __NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                    if num_unvoiced > 0.85 * __NUM_WINDOW_CHUNKS_END or time_use > 10:
                        sys.stdout.write("\nEnd.\n")
                        triggered = False
                        got_a_sentence = True
                sys.stdout.flush()
            stream.stop_stream()
            got_a_sentence = False

            # write to file
            raw_data.reverse()
            for index in range(start_point):
                raw_data.pop()
            raw_data.reverse()
            raw_data = _normalize(raw_data)
            _record_to_file(filename, raw_data, 2)
            leave = True
        stream.close()
    except Exception as e:
        raise InternalError(e, 'ybc_bot')


def analysis(filename=''):
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")
    if filename == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")

    try:
        text = ybc_speech.voice2text(filename)
        return chat(text)
    except Exception as e:
        raise InternalError(e, 'ybc_bot')


def chat(text=''):
    error_msg = "'text'"
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    if text == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        data = {
            'text': text
        }
        url = __IDIOM_URL
        for i in range(3):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                res = r.json()
                if res['results'] and res['results'][0]['values']:
                    res = res['results'][0]['values']['text']
                    return res

        raise ConnectionError('获取机器人对话失败', r._content)

    except Exception as e:
        raise InternalError(e, 'ybc_bot')


def main():
    filename = "test.wav"
    listen(filename)
    print(analysis(filename))


if __name__ == '__main__':
    main()
