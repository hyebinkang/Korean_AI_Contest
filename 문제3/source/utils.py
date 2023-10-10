import numpy as np
import os # os 라이브러리 불러오기 (파일 경로 다루기용)

sample_rate = 16000

# 텍스트 파일을 읽어와서 그 내용을 가져오는 함수
def read_audiolist(audiolist_file):
    try:
        with open(audiolist_file, 'r', encoding='utf-8') as file:
            audio_files = file.readlines()
        # 개행 문자 및 공백 제거
        audio_files = [file.strip() for file in audio_files]
        return audio_files
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return []

# 오디오 파일을 처리하는 함수
def process_audio_files(audio_files):
    audio_data_dict = {}  # 오디오 데이터를 파일명(확장자 포함)을 키로 가지는 딕셔너리로 저장

    for file_path in audio_files:
        if os.path.exists(file_path):
            try:
                # 파일명에서 확장자를 포함하여 추출
                file_name = os.path.basename(file_path)

                # PCM 파일을 읽어와 넘파이 배열로 변환하여 딕셔너리에 추가
                audio_data = np.fromfile(file_path, dtype=np.int16)
                audio_data_dict[file_name] = audio_data

                print(f"처리 중인 오디오 파일: {file_path}")
            except Exception as e:
                print(f"오디오 파일을 읽는 중 오류 발생: {str(e)}")
        else:
            print(f"경로가 잘못되었거나 파일이 존재하지 않습니다: {file_path}")

    return audio_data_dict

def normalize_audio(audio_data):
    max_val = np.max(np.abs(audio_data))  # 오디오 데이터의 최댓값을 찾음
    normalized_audio = audio_data / max_val  # 전체 오디오 데이터를 최댓값으로 나눠 정규화
    return normalized_audio

def bandpass_filter_with_smoothing(audio_data, cutoff_freqs=[100, 300], window_size=160):
    nyquist_freq = 0.5 * sample_rate
    
    # FFT를 주파수 영역으로
    audio_fft = np.fft.fft(audio_data)
    
    # 범위 외의 숫자를 0으로 바꾸기
    audio_fft[:int(cutoff_freqs[0] * len(audio_data) / nyquist_freq)] = 0
    audio_fft[int(cutoff_freqs[1] * len(audio_data) / nyquist_freq):] = 0
    
    # IFFT를 도메인 영역으로 전환
    filtered_audio = np.fft.ifft(audio_fft)
    filtered_audio = np.real(filtered_audio)
    
    # 이동 평균 사용해서 신호 부드럽게
    smoothed_audio = np.convolve(filtered_audio, np.ones(window_size)/window_size, mode='same')
    
    return normalize_audio(smoothed_audio)


def detect_silence(audio_data, k=4):
    silence_list = []
    beg, end = 0, 0

    for i in range(1, audio_data.shape[0]):
        # 무음구간 시작
        if audio_data[i-1]==audio_data[i] and audio_data[i-1] == 0:
            if i==1:
                beg = round( i / sample_rate, 2)
            else:
                pass
        # 무음 구간 끝나는 시점
        elif audio_data[i-1]!=audio_data[i] and audio_data[i-1] == 0:
            end = round(i / sample_rate, 2)
            if beg != 0 and end != 0:
                if end - beg >= k:
                    silence_list.append({"beg":beg, "end":end})
                    beg, end = 0, 0
        # 소리구간 진행
        elif audio_data[i-1]==audio_data[i] and audio_data[i-1] == 1:
            if i==1:
                pass
            else:
                pass
        # 소리구간 끝과 무음구간이 시작되는 시점
        elif audio_data[i-1]!=audio_data[i] and audio_data[i-1] == 1:
            beg = round( i / sample_rate, 2)

    return silence_list