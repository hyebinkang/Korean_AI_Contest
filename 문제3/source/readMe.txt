# 문제3. 무음 구간 찾기

1. requirements.txt
	argparse
	utils
    numpy
    json
	os

2. how to start
   python3 Q3.py pcmlist.txt ../output/Q3.json

3. Guideline
    1. 데이터를 가져와 실행합니다. [실행경로는 Q3.py가 있는 source에 위치해야 함]
        python3 Q3.py pcmlist.txt ../output/Q3.json
    2. audiolist 파일의 목록을 utils.py의 read_audiolist 함수에서 리스트로 만들고 process_audio_files 함수에서 넘파이 배열로 변환하여
       딕셔너리에 저장합니다.
    3. audiolist의 목록을 for문으로 가져옵니다.
        3-1. utils.py의 bandpass_filter_with_smoothing 함수에 numpy 배열을 넣으면 필터가 적용되어 소음이 제거됩니다.
        3-2. 0,1로 나타내 주기 위해 불리언 인덱싱을 진행합니다. (무음 부분: 0, 소리 부분: 1)
        3-3. 4초 동안 무음이 지속되는 부분을 탐색합니다.
    4. 저장된 무음 구간을 JSON 파일로 추출합니다.
