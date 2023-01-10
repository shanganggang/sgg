'''
author: Zhuangting
createTime: 2022-11-18
'''
import time

import pytest
from services.merchandise.Validity.api import Api
import allure
from selenium import webdriver

"""
   前置条件：用户登录
      执行步骤：
      1.进入库存中心
      2.选择餐厅进入库存中心
      3.进入效期一栏
      4.查看菜库货品——同一品项多批次
      5.查看菜库半成品——同一品项多批次
      6.查看干货库货品——同一品项多批次
      7.查看干货库半成品——同一品项多批次
      8.效期计算——干货库进货流水
      9.效期计算——干货库调拨流水
      10.新零售品项
      11.搜索
      12.修改
      13.删除
     """


@pytest.mark.usefixtures('init_driver')
@allure.feature('库存中心')
class TestCase:

    @allure.title('登录库存中心')
    def test_Validity_Sign001(self, init_driver):
        my_web_driver = init_driver
        # my_web_driver.get("http://10.218.223.214:8081/IH_WEB/#/login")
        Validity = Api(my_web_driver)
        Validity.Validity_Sign_in()

    @allure.title('选择品牌餐厅进入库存中心')
    def test_Validity_sys002(self, init_driver):
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        Validity.Validity_Choose_kfc()  # 选择品牌
        Validity.Validity_Sign_in()  # 登录
        Validity.Validity_Choose_kfc()  # 选择品牌

    @allure.title('点击效期一栏输入餐厅编码')
    def test_Validity_sys003(self, init_driver):
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in() #登录
        # Validity.Validity_Choose_kfc() #选择品
        Validity.Validity_Choose_store()

    @allure.title("查看冷藏菜库货品——同一品项多批次")
    def test_Validity_sys004(self, init_driver):
        # 已过期未报废TAB页面冷藏菜库查询
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_ExpiredVegetable()

    @allure.title("查看菜库半成品——同一品项多批次")
    def test_Validity_sys005(self, init_driver):
        # 本月即将到期tab，冷藏菜库查询
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in() #登录
        # Validity.Validity_Choose_kfc() #选择品牌
        # Validity.Validity_Sign_in() #登录
        # Validity.Validity_Choose_kfc() #选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_expiringVegetable()

    @allure.title("查看干货库货品——同一品项多批次")
    def test_Validity_sys006(self, init_driver):
        # 今日即将到期TAB页面
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_TodayExpiringDry()

    @allure.title("查看干货库半成品——同一品项多批次")
    def test_Validity_sys007(self, init_driver):
        # 自定义查看TAB页面
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in() #登录
        # Validity.Validity_Choose_kfc() #选择品牌
        # Validity.Validity_Sign_in() #登录
        # Validity.Validity_Choose_kfc() #选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_SelfDefiningVegetable()

    @allure.title("效期计算——干货库进货流水")
    def test_Validity_sys008(self, init_driver):
        # 已过期未报废的干货库
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_expiredDry()

    @allure.title("效期计算——干货库调拨流水")
    def test_Validity_sys009(self, init_driver):
        # 已过期未报废的干货库
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_expiredDryProduction()

    @allure.title("新零售品项")
    def test_Validity_sys010(self, init_driver):
        # 新零售临期品tab
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_Inq_newRetailingProduct()

    @allure.title("搜索")
    def test_Validity_sys0011(self, init_driver):
        # 本月即将到期TAB页面
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_InqByItemCode()

    @allure.title("修改")
    def test_Validity_sys0012(self, init_driver):
        # 本月即将到期TAB页面
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_ModifyByItemCode()

    @allure.title("删除")
    def test_Validity_sys0013(self, init_driver):
        # 本月即将到期TAB页面
        my_web_driver = init_driver
        Validity = Api(my_web_driver)
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Sign_in()  # 登录
        # Validity.Validity_Choose_kfc()  # 选择品牌
        # Validity.Validity_Choose_store()
        Validity.Validity_delete()


if __name__ == '__main__':
    pytest.main(["validity_test.py", "-s"])
#     # pytest.main(["validity_test.py", "-s", "--alluredir", "../reports/tmp"])
#     # os.system("allure serve ../reports/tmp")
#     # pytest.main(["validity_test.py", "-s", "--alluredir", "../../reports/tmp"])
#     # os.system("allure serve allure ../../reports/tmp")
