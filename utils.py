import json
import logging
import pymysql

import requests
from bs4 import BeautifulSoup

import app


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))


def request_third_api(form_data):
    # 解析响应中form表单的数据，并提取为后续第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    url = soup.form['action']
    logging.info("第三方请求的url{}".format(url))
    # 定义字典
    data = {}
    for inputs in soup.find_all('input'):
        # 循环为字典赋值
        data.setdefault(inputs['name'], inputs['value'])
    logging.info("第三方请求的data{}".format(data))
    response = requests.post(url, data)
    return response


def read_imgVerify_data(file_name):
    # 文件位置
    file = app.BASE_DRL + "/data/" + file_name
    test_case_data = []
    # 打开文件
    with open(file, encoding="utf-8") as f:
        # 转为字典
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        # 循环加入 test_case_data
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"), test_data.get("status_code")))
    print("json data={}".format(test_case_data))
    return test_case_data

def reg_data(file_name):
    #注册的测试数据的文件路径
    file = app.BASE_DRL + "/data/" + file_name
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json的数据格式，转化为字典的数据格式
        register_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = register_data.get("test_register")
        #依次读取测试数据列表中的每一条数据，并进行相应字段的提取
        for test_data in test_data_list:
            test_case_data.append((test_data.get("phone"),test_data.get("pwd"),test_data.get("imgVerifyCode"),test_data.get("phoneCode"),test_data.get("dyServer"),test_data.get("invite_phone"),test_data.get("status_code"),test_data.get("status"),test_data.get("description")))
        print("test_case_data = {}".format(test_data_list))
    return test_case_data


def read_param_data(filename, method_name, param_names):
    # filename： 参数数据文件的文件名
    # method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    # param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"

    # 获取测试数据文件的文件路径
    file = app.BASE_DRL + "/data/" + filename
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        # 将json字符串转换为字典格式
        file_data = json.load(f)
        # 获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            # 先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                # 依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            # 每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data

