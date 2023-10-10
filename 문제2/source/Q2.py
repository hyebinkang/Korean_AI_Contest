import argparse
from utils import load_data, check_error
import json

def arg_parse():
    parser = argparse.ArgumentParser(description='Korean SR Contest 2023')
    parser.add_argument('audiolist', type=str, help='Path to the text file containing list of WAV files')
    parser.add_argument('outfile', type=str, help='Path to the output JSON file')

    args = parser.parse_args()

    return args


def main(audio_list, outfile):
    data = load_data(audio_list)
    data = check_error(data)

    with open(outfile, 'w', encoding='utf-8') as json_file: # 저장할 파일 경로 및 이름
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    args = arg_parse()
    main(args.audiolist, args.outfile)