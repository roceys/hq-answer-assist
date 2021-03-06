# coding=utf-8
from aip import AipOcr
import re

opt_aux_word = ['《', '》']


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def image_to_str(name, client):
    image = get_file_content(name)
    text_result = client.basicGeneral(image)
    print(text_result)
    result = get_question_and_options(text_result)
    return result


def init_baidu_ocr(baidu_ocr_config):
    app_id, api_key, secret_key = baidu_ocr_config
    client = AipOcr(app_id, api_key, secret_key)
    return client


# {'words_result': [{'words': '11.代表作之一是《蒙娜丽莎的眼'},
#                   {'words': '泪》的歌手是?'}, {'words': '林志颖'},
#                   {'words': '林志炫'}, {'words': '林志玲'}],
#  'log_id': 916087026228727188, 'words_result_num': 5}

def get_question_and_options(text):
    if 'error_code' in text:
        print('请确保百度OCR配置正确')
        exit(-1)
    if text['words_result_num'] == 0:
        return '', []
    result_arr = text['words_result']
    option_arr = []
    question_str = ''
    question_obj, options_obj = get_question(result_arr)
    for question in question_obj:
        word = question['words']
        word = re.sub('^\d+\.*', '', word)
        question_str += word
    for option in options_obj:
        word = option['words']
        if word.startswith('《'):
            word = word[1:]
        if word.endswith('》'):
            word = word[:-1]
        print(word)
        option_arr.append(word)

    print(question_str)
    print(option_arr)
    return question_str, option_arr


# 先按'？'分割问题和答案，若无问号，用索引分割
def get_question(result_arr):
    result_num = len(result_arr)
    index = -1
    question_obj, options_obj = [], []
    for i, result in enumerate(result_arr):
        if '?' in result['words']:
            index = i
            break
    if index > -1:
        question_obj = result_arr[:index + 1]
        options_obj = result_arr[index + 1:]
        return question_obj, options_obj
    else:
        # 按照经验，4个结果为1行问题，5、6个为2行问题，8个以上为公布答案
        if result_num <= 4:
            question_obj = result_arr[:1]
            options_obj = result_arr[1:]
        elif result_num == 5:
            question_obj = result_arr[:2]
            options_obj = result_arr[2:]
        elif result_num == 6:  # 暂时
            question_obj = result_arr[:2]
            options_obj = result_arr[2:]
        elif result_num == 7 or result_num == 8:
            question_obj = result_arr[:3]
            options_obj = result_arr[3:]
        return question_obj, options_obj
