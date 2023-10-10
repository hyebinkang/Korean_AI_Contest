# 문제2. 에러 음성파일 찾기

1. requirements.txt
	argparse
	utils
	numpy
	json

2. how to start
   python3 Q2.py wavlist.txt ../output/Q2.json

3. Guideline
    1. 데이터를 가져와 실행합니다. [실행경로는 Q2.py가 있는 source에 위치해야 함]
        python3 Q2.py wavlist.txt ../output/Q2.json
    2. audio_list를 utils.py의 load_data를 통해 wave_zip 를 형성합니다.
    3. check_error 함수를 통해 각 오디오의 에러 유형을 확인합니다.
        3-1. calculated_rms로 노이즈의 값을 계산합니다.
        3-2. detect_wav_header로 RIFF 의 여부와 데이터가 없는 경우를 확인합니다.
        3-3. 헤더가 아예 존재하지 않고 데이터가 없는 경우, 존재하지만 데이터가 있는경우, 없지만 데이터가 있는경우 각각을 구별하여
             에러리스트로 저장합니다.
        3-4. 데이터가  32767을 이상이거나 -32768 이하인 경우 클리핑 에러로 분류합니다. (이 숫자는 16비트의 정수형 데이터 타입의 범위임)
        3-5. 노이즈 값을 저장한 변수를 불러와 rms_threshold(=0.1) 값 보다 작으면 0에 가까운 노이즈로 묵음에 가까운 데이터로 분류되어
             에러리스트로 저장합니다.
    4. 저장된 오류 리스트를 JSON 파일로 추출합니다.


