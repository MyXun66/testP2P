import logging
import random

import requests
import unittest

from bs4 import BeautifulSoup
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from utils import assert_utils
from utils import request_third_api


class trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户请求
    def test01_trust_request(self):
        # 1、认证通过的账号登录
        response = self.login_api.login(self.session)
        logging.info("认证通过的账号登录 = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("发送开户请求 = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        form_data = response.json().get("description").get("form")
        logging.info("开户请求返回{}".format(form_data))
        # 调用抽象出的第三方接口类
        response = request_third_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    # 充值成功
    def test02_recharge(self):
        # 1、认证通过的账号登录
        response = self.login_api.login(self.session)
        logging.info("认证通过的账号登录 = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2 获取验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 3.发送充值请求
        response = self.trust_api.recharge(self.session, '10000')
        logging.info("发送充值请求：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4、 发送第三方充值请求
        # 获取响应中form表单的数据，并提取为后续第三方请求的参数
        form_data = response.json().get("description").get("form")
        logging.info('获取响应中form表单的数据{}'.format(form_data))
        # 调用第三方请求的接口
        response = request_third_api(form_data)
        logging.info('充值成功：{}'.format(response))
        # 断言response是否正确
        self.assertEqual('NetSave OK', response.text)


