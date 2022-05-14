import logging
import unittest
import random
from time import sleep

import requests
from parameterized import parameterized

import app
from api.loginAPI import loginAPI
from utils import assert_utils, read_imgVerify_data, reg_data, read_param_data


class login(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    phone3 = '13033447713'
    phone4 = '13033447714'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    @parameterized.expand(read_param_data("imgVerify.json", "test_get_img_verify_code", "type,status_code"))
    # @parameterized.expand(read_imgVerify_data("imgVerify.json"))
    # @parameterized.expand(read_param_data("imgVerify.json","test_get_img_verify_code","type,status_code"))
    def test01_get_img_verify_code(self, type, status_code):
        # 根据不同的type类型准备不同的参数数据
        r = ''
        if type == 'float':
            r= str(random.random())
        elif type == 'int':
            r = str(random.randint(10000000,90000000))
        elif type == 'char':
            r = ''.join(random.sample("abcdedfhijklmn",8))
        # 发送请求
        response = self.login_api.getImgCode(self.session,r)
        logging.info("r = {} response = {}".format(r,response))
        # 对响应结果进行断言
        self.assertEqual(status_code,response.status_code)

    @parameterized.expand(read_param_data("register.json", "test_register",
                                          "phone,pwd,imgVerifyCode,phoneCode,dyServer,invite_phone,status_code,status,description"))
    # @parameterized.expand(reg_data("register.json"))
    def test10_register(self, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone, status_code, status,
                            description):
        # 1、获取图片验证码成功
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码成功
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、使用参数化的测试数据进行注册，并返回对应的结果
        # 发送注册请求
        response = self.login_api.register(self.session, phone, pwd, imgVerifyCode, phoneCode, dyServer,
                                               invite_phone)
        logging.info("register response = {}".format(response.json()))
        # 对收到的响应进行断言
        assert_utils(self, response, status_code, status, description)

    # 登录成功
    def test17_login_success(self):
        # 准备参数
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        # 对结果进行断言
        assert_utils(self,response,200,200,"登录成功")

    # 登录失败——用户名不存在
    def test18_login_phone_not_exist(self):
        # 准备参数
        Wphone = '13000000000'
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,Wphone,self.pwd)
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self,response,200,100,"用户不存在")

    # 登录失败——密码为空
    def test19_login_pwd_is_null(self):
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,"")
        logging.info("login response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    # 登录失败——密码错误
    # def test20_login_wrong_pwd(self):
    #     wrong_pwd = 'error'
    #     #1、输入错误密码，提示错误一次
    #     response = self.login_api.login(self.session,self.phone1,wrong_pwd)
    #     logging.info("login response = {}".format(response.json()))
    #     #对结果进行断言
    #     assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
    #     # 2、输入错误密码，提示错误两次次
    #     response = self.login_api.login(self.session,self.phone1,wrong_pwd)
    #     logging.info("login response = {}".format(response.json()))
    #     #对结果进行断言
    #     assert_utils(self,response,200,100,"密码错误2次,达到3次将锁定账户")
    #     # 3、输入错误密码，提示错误三次被锁定
    #     response = self.login_api.login(self.session,self.phone1,wrong_pwd)
    #     logging.info("login response = {}".format(response.json()))
    #     #对结果进行断言
    #     assert_utils(self,response,200,100,"由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #     #4、 输入正确密码，提示被锁定
    #     response = self.login_api.login(self.session,self.phone1,self.pwd)
    #     logging.info("login response = {}".format(response.json()))
    #     #对结果进行断言
    #     assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
    #     #5、等待60s，再输入正确密码，提示登录成功
    #     sleep(60)
    #     response = self.login_api.login(self.session,self.phone1,self.pwd)
    #     logging.info("login response = {}".format(response.json()))
    #     #对结果进行断言
    #     assert_utils(self,response,200,200,"登录成功")