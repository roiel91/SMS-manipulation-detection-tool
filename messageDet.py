import os
import re, csv, sys
import datetime
import pandas as pd
from openpyxl.styles import PatternFill
from openpyxl import Workbook
import openpyxl
import subprocess
import time

from ppadb.client import Client

def connect():
    client = Client(host="127.0.0.1", port=5037)
    devices = client.devices()

    if len(devices) == 0:
        print('No devices.')
        quit()
    elif len(devices) >= 2:
        print('More than one device/emulator.')
        quit()

    device = devices[0]
    print(f'Connected to {device}')
    return device, client

def get_sms(device, start_date, end_date):
    sms = re.split('Row: ', device.shell("content query --uri content://sms/"))
    mms = re.split('Row: ', device.shell("content query --uri content://mms/"))
    sms_list = list()
    for tmp in sms:
        if len(tmp) == 0:
            continue

        tmp_dict = dict()

        start_offset = tmp.find('address=') + 8
        end_offset = tmp.find(',', start_offset)
        tmp_dict['address'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('date=') + 5
        end_offset = tmp.find(',', start_offset)
        tmp_dict['date'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('protocol=') + 9
        end_offset = tmp.find(',', start_offset)
        tmp_dict['protocol'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('body=') + 5
        end_offset = tmp.find(',', start_offset)
        tmp_dict['body'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('sub_id=') + 7
        end_offset = tmp.find(',', start_offset)
        tmp_dict['sub_id'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('creator=') + 8
        end_offset = tmp.find(',', start_offset)
        tmp_dict['creator'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('sim_imsi=') + 9
        end_offset = tmp.find(',', start_offset)
        tmp_dict['sim_imsi'] = tmp[start_offset: end_offset]

        start_offset = tmp.find('correlation_tag=') + 16
        end_offset = tmp.find(',', start_offset)
        tmp_dict['correlation_tag'] = tmp[start_offset: end_offset]

        # Unix 타임스탬프를 datetime 객체로 변환하기
        date = datetime.datetime.fromtimestamp(int(tmp_dict['date'])/1000.0)
        tmp_start_date = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]), int(start_date[8:10]), int(start_date[10:12]), int(start_date[12:14]))
        tmp_end_date = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]),
                                           int(end_date[8:10]), int(end_date[10:12]), int(end_date[12:14]))


        if date >= tmp_start_date and date <= tmp_end_date:
            tmp_dict['date'] = date.strftime('%Y-%m-%d %H:%M:%S')
            sms_list.append(tmp_dict)

    return sms_list


def extract_to_excel(sms_list):

    df = pd.DataFrame(sms_list)
    # CSV 파일로 저장
    csv_file = 'sms_list.csv'
    df.to_csv(csv_file, encoding='utf-8-sig', index=False)

    # CSV 파일을 읽어서 DataFrame으로 변환
    df_excel = pd.read_csv(csv_file)

    # 'creator' 필드에 'fake'를 포함하는 행을 빨간색 음영으로 표시하는 스타일 함수
    def highlight_fake(value):
        return 'background-color: red' if 'fake' in str(value).lower() else ''

    # 스타일 적용
    styled_df = (df_excel.style.map(highlight_fake, subset=['creator']))  # Deprecated

    # 스타일이 적용된 DataFrame을 Excel 파일로 저장
    output_excel_path = 'highlighted_sms_list.xlsx'
    styled_df.to_excel(output_excel_path, index=False, engine='openpyxl', sheet_name='Sheet1')

    print(f"DataFrame이 {output_excel_path}로 저장되었습니다.")
    print('문자메시지 추출이 완료되었습니다.')

if __name__ == '__main__':
    try:
        if len(sys.argv[1]) != 14 or len(sys.argv[2]) != 14:
            print("검색하고자 하는 시작 시간과 종료 시간을 입력해주세요.(UTC+9 기준)\n입력 예시) 20231015125400 20231213152100")
        else:
            device, client = connect()
            sms_list = get_sms(device, start_date=sys.argv[1], end_date=sys.argv[2])
            extract_to_excel(sms_list)
    except IndexError:
        print("검색하고자 하는 시작 시간과 종료 시간을 입력해주세요.(UTC+9 기준)\n입력 예시) 20231015125400 20231213152100")



