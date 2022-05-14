import logging
import unittest
import random
from time import sleep

import requests

from utils import assert_utils
from api.loginAPI import loginAPI


class login(unittest.TestCase):
    phone1 = '13033447888'
    phone2 = '17855555510'
    phone3 = '17855555509'
    phone4 = '17855555508'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 参数为随机小数时获取图片验证码成功
    def test01_get_img_code_random_float(self):
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 参数为随机整数时获取图片验证码成功
    def test02_get_img_code_random_int(self):
        # 定义参数(随机整数)
        r = random.randint(1000000, 5000000)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 参数为空时获取图片验证码失败
    def test03_get_img_code_random_null(self):
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, "")
        # 接收接口的返回结果，进行断言
        self.assertEqual(404, response.status_code)

    # 参数为随机字母时获取图片验证码失败
    def test04_get_img_code_random_char(self):
        # 定义参数(随机字母)
        r = random.sample("abcdefghigklmnopqrst", 8)
        param = ''.join(r)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, param)
        # 接收接口的返回结果，进行断言
        self.assertEqual(400, response.status_code)

    # 获取短信验证码成功--参数正确
    def test05_get_sms_code_session(self):
        # 先请求图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("获取短信验证码成功--参数正确：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")

    # 获取短信验证码失败--图片验证码错误
    def test06_get_sms_code_wrong_code(self):
        # 先请求图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        response = self.login_api.getSmsCode(self.session, self.phone1, 6666)
        logging.info("获取短信验证码失败--图片验证码错误： {}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败--图片验证码为空
    def test07_get_sms_code_null(self):
        # 先请求图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        response = self.login_api.getSmsCode(self.session, self.phone1, "")
        logging.info("获取短信验证码失败--图片验证码为空： {}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码失败--手机号码为空
    def test08_get_sms_code_phone_null(self):
        # 先请求图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        response = self.login_api.getSmsCode(self.session, "", self.imgCode)
        logging.info("获取短信验证码失败--手机号码为空： {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 获取短信验证码失败--未调用获取图片验证码接口
    def test09_get_sms_code_no_code_api(self):
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("获取短信验证码成功--未调用获取图片验证码接口：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 输入必填参数注册成功
    def test10_register_success(self):
        # 成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 成功获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("获取短信验证码成功--参数正确：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")

        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("输入必填参数注册成功：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

        # 输入所有项，注册成功
    def test11_register_success_param_all(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone='13012345678')
        logging.info("输入所有项，注册成功 = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 手机号已存在时，注册失败
    def test12_register_phone_exist(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("输入所有项，注册成功 = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 注册失败——密码为空
    def test13_register_pws_null(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone3, pwd='')
        logging.info("注册失败——密码为空: {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 注册失败——图片验证码错误
    def test14_register_img_code_error(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone4, self.pwd, imgVerifyCode='5555')
        logging.info("注册失败——图片验证码错误: {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "验证码错误!")

    # 注册失败——短信验证码错误
    def test15_register_phone_code_error(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone4, self.pwd, phoneCode='888888')
        logging.info("注册失败——短信验证码错误 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "验证码错误")

    # 注册失败——不同注册协议
    def test16_register_no_agree(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("获取短信验证码成功--参数正确 = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、发送注册请求
        response = self.login_api.register(self.session, self.phone4, self.pwd, dyServer='off')
        logging.info("注册失败——不同注册协议 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "验证码错误")

        # 登录成功
    def test17_login_success(self):
        # 准备参数
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("登录成功 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "登录成功")

    # 登录失败——用户名不存在
    def test18_login_name_no_exist(self):
        # 准备参数
        # 调用接口类中的发送登录的接口
        Wphone = '17777777777'
        response = self.login_api.login(self.session, Wphone, self.pwd)
        logging.info("登录失败——用户名不存在 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "用户不存在")

    # 登录失败——密码为空
    def test19_login_pwd_null(self):
        # 准备参数
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session, self.phone1, pwd='')
        logging.info("登录失败——密码为空 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 登录失败——密码错误
    def test20_login_pwd_error(self):
        # 准备参数
        error = '123'
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session, self.phone1, pwd=error)
        logging.info("登录失败——密码错误一次 : {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        response = self.login_api.login(self.session, self.phone1, pwd=error)
        logging.info("登录失败——密码错误两次 : {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        response = self.login_api.login(self.session, self.phone1, pwd=error)
        logging.info("登录失败——密码错误三次 : {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("登录失败——账号锁定 : {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        sleep(60)
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("登录成功——等待60s : {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
