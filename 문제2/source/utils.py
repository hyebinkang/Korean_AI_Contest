import numpy as np

def load_data(file):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            audio_files = file.readlines()
        # 개행 문자 및 공백 제거
        wave_files = [file.strip() for file in audio_files]
        # 각 wav 파일 처리
        wave_zip = {}
        for path in wave_files:
            with open(path, "rb") as f:
                header = f.read(44)
                data = np.frombuffer(f.read(), dtype=np.int16)
                wave_zip[path] = (header, data)

        return wave_zip

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return []


# RMS (Root Mean Square)를 이용해서 '노이즈만 있는 경우'도 판별
def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data)))

# RIFF 가 없는 파일을 찾아냄
def detect_wav_header(header):
    return False if header[:4] == b'RIFF' else True

def check_error(wave_zip):
    errors = {"error_list": []}
    rms_threshold = 0.1  # 가장 작은 임의의 값

    if not wave_zip:
        print("파일이 없어서 체크할 수 없어.")
        return errors

    for file_name, data in wave_zip.items():
        rms_value = calculate_rms(data[1])
        if detect_wav_header(data[0]):
            errors["error_list"].append(file_name)          # RIFF가 없는 경우

        elif not detect_wav_header(data[0]) and not np.any(data[1]):
            errors["error_list"].append(file_name)      # RIFF없고 데이터도 없음

        elif not data[0] and not np.any(data[1]):
            errors["error_list"].append(file_name)   # 헤더가 아얘 존재하지 않고 데이터도 없음"

        elif data[0] and not np.any(data[1]):
            errors["error_list"].append(file_name)      # 헤더가 존재하지만 데이터가 없음

        elif not data[0] and np.any(data[1]):
            errors["error_list"].append(file_name)      # 헤더가 없지만 데이터는 있음"

        elif np.all(data[1] == 0):
            errors["error_list"].append(file_name)      # 데이터가 있지만 데이터 값이 0인 경우

        elif np.max(data[1]) >= 32767 or np.min(data[1]) <= -32768:
            errors["error_list"].append(file_name)      # 클리핑 에러

        elif rms_value < rms_threshold:
            errors["error_list"].append(file_name)      # 묵음 노이즈의 데이터인 경우

    return errors



