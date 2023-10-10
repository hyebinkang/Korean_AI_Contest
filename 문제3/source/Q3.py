import argparse         # argparse 라이브러리 불러오기 (커맨드라인 인자 처리용)
import json             # json 라이브러리 불러오기 (JSON 파일 다루기용)
import numpy as np      # numpy 라이브러리 불러오기 (수학 연산용)
from utils import read_audiolist, process_audio_files, detect_silence
from utils import bandpass_filter_with_smoothing


# 샘플링 레이트를 16kHz로 설정
sample_rate = 16000

# 커맨드라인 인자를 처리하는 함수
def arg_parse():
    parser = argparse.ArgumentParser(description='Detect silence intervals in PCM audio files')
    parser.add_argument('audiolist', type=str, help='Path to the text file containing list of PCM files')
    parser.add_argument('outfile', type=str, help='Path to the output JSON file')
    args = parser.parse_args()
    return args

# 실제 작동하는 메인 함수
def main(audiolist, outfile):
    # audiolist 파일에서 오디오 파일 목록을 가져온다
    audio_files = read_audiolist(audiolist)
    audio_names = []
    # 가져온 목록을 출력
    # print("오디오 파일 목록:")

    for file in audio_files:
        print(file)
        audio_names.append(file.split('/')[-1])

    # print(audio_names)
    # 오디오 파일을 처리
    data = process_audio_files(audio_files)
    # print(data)

    for file_name, audio_data in data.items():
        # 필터 적용
        data[file_name] = bandpass_filter_with_smoothing(audio_data)

        # 불리언 인덱싱과 무음 구간 구분
        data[file_name] = np.abs(data[file_name])
        mean_arr = np.mean(data[file_name]) * 4
        data[file_name] = data[file_name] >= mean_arr

        # 4초 지속 구간 탐지 : k로 원하는 초 정하기
        data[file_name] = detect_silence(data[file_name], k=4)

    # silence_list를 JSON 파일로 저장
    with open(outfile, 'w', encoding='utf-8') as json_file: # 저장할 파일 경로 및 이름
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# 코드를 실제로 실행하려면 아래 주석을 해제
if __name__ == '__main__':
    args = arg_parse()
    main(args.audiolist, args.outfile)
