import wave
import pyaudio
import threading
import socket
import asyncio
import aioconsole
import struct  # 이 줄을 추가합니다


CHUNK = 480  # 30ms at 16kHz
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SERVER_ADDRESS = ('localhost', 43007)  # 서버 주소와 포트

p = pyaudio.PyAudio()
frames = []
recording = False

def record_and_stream_audio():
    global recording, frames
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(SERVER_ADDRESS)
            print("서버에 연결되었습니다.")
            
            while recording:
                data = stream.read(CHUNK)
                frames.append(data)
                # 데이터 길이를 먼저 전송한 후 실제 데이터 전송
                s.sendall(struct.pack('>I', len(data)))
                s.sendall(data)
        except ConnectionRefusedError:
            print("서버 연결에 실패했습니다. 서버가 실행 중인지 확인하세요.")
            recording = False
        except Exception as e:
            print(f"오류 발생: {e}")
            recording = False
    
    stream.stop_stream()
    stream.close()

print("녹음을 시작하려면 엔터 키를 누르세요.")
input()

recording = True
audio_thread = threading.Thread(target=record_and_stream_audio)
audio_thread.start()

print("녹음 및 스트리밍 중... 종료하려면 다시 엔터 키를 누르세요.")
input()

recording = False
audio_thread.join()

p.terminate()

# 녹음된 데이터를 로컬 파일로도 저장
WAVE_OUTPUT_FILENAME = "output.wav"
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"녹음이 {WAVE_OUTPUT_FILENAME}에 저장되었습니다.")