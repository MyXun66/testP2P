import time
import unittest

import app
from scripts.approver import approver
from scripts.login import login
from scripts.tender import tender
from scripts.trust import trust

from tools import HTMLTestRunner_PY3

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(approver))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))

# report_file = app.BASE_DRL + "/reports/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
report_file = app.BASE_DRL + "/reports/report.html"
with open(report_file, mode='wb') as f:
    runner = HTMLTestRunner_PY3.HTMLTestRunner(f, title="P2P金融的接口测试报告", description="test")
# 运行测试套件
    runner.run(suite)
