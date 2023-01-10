'''
author: Zhuangting
createTime: 2022-11-18
'''

import datetime
import time

import requests
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from common.log import MyLog
from common.merchandise.Validity.readyaml import readyaml
from common.ui.elements_api import ElementsApi
from common.ui.elements_location import ElementsLocation
from datetime import timedelta, date

# def readyaml1():
#     return readyaml('config.yaml')
from services.merchandise.Validity.mysql import mysql


class Api(ElementsApi):
    #     add by gg
    def readyaml(self):
        return readyaml('config.yaml')

    def __init__(self, my_driver):
        ElementsApi.__init__(self, my_driver)
        self.time_now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.time_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
        # 180天前 大米
        self.productionDate = (date.today() - relativedelta(months=6) + relativedelta(days=1)).strftime("%Y-%m-%d")
        # 牛奶 保质期180天
        self.milkProductionDate = (date.today() - relativedelta(months=6) - relativedelta(days=3)).strftime("%Y-%m-%d")
        # 720天前 冰淇淋花
        self.iceProductionDate = (date.today() - relativedelta(months=24)).strftime("%Y-%m-%d")
        print(self.productionDate)
        self.conf_data = self.readyaml()
        self.host = self.conf_data['MySQL']['test']['host']
        self.port = self.conf_data['MySQL']['test']['port']
        self.user = self.conf_data['MySQL']['test']['user']
        self.password = self.conf_data['MySQL']['test']['password']
        self.database = self.conf_data['MySQL']['test']['database']
        self.vegetables_code = self.conf_data['ValidityData']['test']['vegetableCode']
        self.cold_code = self.conf_data['ValidityData']['test']['coldStorageCode']
        self.my_store_code = self.conf_data['STORE']['test']['storeCode']
        self.dryCode = self.conf_data['ValidityData']['test']['dryCode']
        self.expiredDryCode = self.conf_data['ValidityData']['test']['expiredDryCode']
        self.expiredDryCode2 = self.conf_data['ValidityData']['test']['expiredDryCode2']
        self.newRetailingCode = self.conf_data['ValidityData']['test']['newRetailingCode']

    def Validity_Sign_in(self):
        # MyLog.info(f"登录库存中心")
        self.input_text(ElementsLocation.Validity.yonghuming_text, 'RCwr')
        self.input_text(ElementsLocation.Validity.mima_text, '1')
        self.input_text(ElementsLocation.Validity.yanzhengma_code, "1234")
        self.click_by_xpath(ElementsLocation.Validity.dianji_click)

    def Validity_Choose_kfc(self):
        # MyLog.info(f"选择品牌餐厅进入库存中心")
        self.click_by_xpath(ElementsLocation.Validity.kfc_choose_click)
        self.click_by_xpath(ElementsLocation.Validity.kfc_click)

    def Validity_Choose_store(self):
        MyLog.info(f"点击效期一栏输入餐厅编码")
        # self.click_by_xpath(ElementsLocation.Validity.zhankaicaidan_click)
        self.click_by_xpath(ElementsLocation.Validity.validity_click)
        self.click_by_xpath(ElementsLocation.Validity.validity_login_click)
        self.click_by_xpath(ElementsLocation.Validity.store_bianma_input)
        self.input_text(ElementsLocation.Validity.store_bianma_input, 'SHA039')
        self.click_by_xpath(ElementsLocation.Validity.store_search_click)
        self.click_by_xpath(ElementsLocation.Validity.store_choose_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.store_ok_click)

    #     add by gg

    def Validity_Inq_ExpiredVegetable(self):
        # MyLog.info(f"已过期未报废，冷藏菜库查询")
        time.sleep(1)
        # self.open_url(self.conf_data['URL']['test']['vegetableUrl'])
        self.click_by_xpath(ElementsLocation.Validity.vegetables_ok_click)
        print(self.vegetables_code)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.vegetables_code)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        print(self.time_now)
        time.sleep(1)
        assert self.time_now > my_list[4]

    def Validity_Inq_expiringVegetable(self):
        # MyLog.info(f"本月即将到期，冷藏菜库查询")
        time.sleep(1)
        # self.open_url(self.conf_data['URL']['test']['vegetableUrl'])
        self.click_by_xpath(ElementsLocation.Validity.expiring_ok_click)
        self.click_by_xpath(ElementsLocation.Validity.vegetables_ok_click)
        time.sleep(1)
        print(self.vegetables_code)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.vegetables_code)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        print(self.time_now)
        time.sleep(1)
        assert my_list[3] < self.time_now

    def Validity_Inq_SelfDefiningVegetable(self):
        MyLog.info(f"自定义查看tab，冷藏菜库查询")
        time.sleep(1)
        # self.open_url(self.conf_data['URL']['test']['vegetableUrl'])
        self.click_by_xpath(ElementsLocation.Validity.self_defining_click)
        self.click_by_xpath(ElementsLocation.Validity.vegetables_ok_click)
        print(self.time_date)
        time.sleep(1)
        self.input_text(ElementsLocation.Validity.end_date_input, self.time_date)
        self.click_by_xpath(ElementsLocation.Validity.selfDefining_click)
        self.click_by_xpath(ElementsLocation.Validity.selfDefining_click)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        last_today = self.time_date + " 59:59:59"
        print(last_today)
        time.sleep(1)
        assert last_today > my_list[4]

    def Validity_InqByItemCode(self):
        MyLog.info(f"搜索")
        time.sleep(1)
        print(self.cold_code)
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.cold_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.cold_code)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
                           database=self.database, charset='utf8')
        data = Validitydb.query_sql_one(
            f'SELECT cqe12.store_code,cqe12.item_code FROM `cic_quality_expire_12` cqe12 where cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.cold_code}"')
        print(data)
        assert data[1] == my_list[2]

    def Validity_ModifyByItemCode(self):
        MyLog.info(f"修改")
        time.sleep(1)
        print(self.cold_code)
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.cold_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.cold_code)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        # 修改到期日期
        self.click_by_xpath(ElementsLocation.Validity.expire_date_click)
        self.click_by_xpath(ElementsLocation.Validity.expire_date_input)
        # date = int(my_list[6].split('-')[2]) - 1
        # print(date)
        # expire_date_choose = (
        #     By.XPATH, "//td[contains(@class,'available current')]//span[contains(text(),'" + str(date) + "')]")  # 当日日期
        self.click_by_xpath(ElementsLocation.Validity.expire_date_choose)
        self.click_by_xpath(ElementsLocation.Validity.expire_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.cold_code)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        my_list1 = self.get_table_listone()
        print(my_list1)
        Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
                           database=self.database, charset='utf8')
        data = Validitydb.query_sql_one(
            f'SELECT cqe12.store_code,cqe12.item_code,cqe12.expired_time FROM `cic_quality_expire_12` cqe12 where '
            f'cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.cold_code}" AND cqe12.batch_time ="{my_list1[5]}"')
        print(data)
        # 转换成2022-12-02形式
        expired_time = data[2].strftime("%Y-%m-%d")
        print(expired_time)
        assert expired_time == my_list1[6]

    def Validity_delete(self):
        MyLog.info(f"删除")
        time.sleep(1)
        print(self.cold_code)
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.cold_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.cold_code)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        self.click_by_xpath(ElementsLocation.Validity.delete_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_ok_click)
        Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
                           database=self.database, charset='utf8')
        data = Validitydb.query_sql_one(
            f'SELECT cqe12.store_code,cqe12.item_code,cqe12.expired_time FROM `cic_quality_expire_12` cqe12 where '
            f'cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.cold_code}" AND '
            f'cqe12.expired_time="{my_list[6]}" ')
        print(data)
        assert data is None

    # 执行前准备数据
    def Validity_CreateData(self):
        MyLog.info(f"点击异常处理输入餐厅编码")
        self.click_by_xpath(ElementsLocation.Validity.zhankaicaidan_click)
        self.click_by_xpath(ElementsLocation.Validity.validity_click)
        self.click_by_xpath(ElementsLocation.Validity.ExceptionDeal_click)
        self.click_by_xpath(ElementsLocation.Validity.store_bianma_input)
        self.input_text(ElementsLocation.Validity.store_bianma_input, self.my_store_code)
        self.click_by_xpath(ElementsLocation.Validity.store_search_click)
        self.click_by_xpath(ElementsLocation.Validity.store_choose_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.store_ok_click)
        # 添加品项  已过期未报废-冷冻库 86110010 冷冻薯条 保质期365 选择生产日期2021-12-4
        self.click_by_xpath(ElementsLocation.Validity.addItem_click)
        self.input_text(ElementsLocation.Validity.ItemCode_input, self.cold_code)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeInq_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeAdd_click)
        self.input_text(ElementsLocation.Validity.shengChanDate_input, "2021-12-4")
        self.click_by_xpath(ElementsLocation.Validity.chooseDate_ok_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.add_ok_click)
        # 今日即将到期-干货库 86110623 大米  如今日2022-12-30 保质期180天  生产日期2022-7-1
        self.click_by_xpath(ElementsLocation.Validity.addItem_click)
        self.input_text(ElementsLocation.Validity.ItemCode_input, self.dryCode)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeInq_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeAdd_click)
        self.input_text(ElementsLocation.Validity.shengChanDate_input, self.productionDate)
        self.click_by_xpath(ElementsLocation.Validity.chooseDate_ok_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.add_ok_click)
        # 已过期未报废-干货库 86110383 纯牛奶-1升*12盒/箱 2022-2-28
        self.click_by_xpath(ElementsLocation.Validity.addItem_click)
        self.input_text(ElementsLocation.Validity.ItemCode_input, self.expiredDryCode)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeInq_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeAdd_click)
        self.input_text(ElementsLocation.Validity.shengChanDate_input, self.milkProductionDate)
        self.click_by_xpath(ElementsLocation.Validity.chooseDate_ok_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.add_ok_click)
        # 已过期未报废-干货库 86132846 冰激凌花筒60g白牛纸托_小黄人香蕉-250个*8条/箱 保质期365 选择生产日期2020-1-1
        self.click_by_xpath(ElementsLocation.Validity.addItem_click)
        self.input_text(ElementsLocation.Validity.ItemCode_input, self.expiredDryCode2)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeInq_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.ItemCodeAdd_click)
        self.input_text(ElementsLocation.Validity.shengChanDate_input, self.iceProductionDate)
        self.click_by_xpath(ElementsLocation.Validity.chooseDate_ok_click)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.add_ok_click)
        # 关闭异常处理
        # self.click_by_xpath(ElementsLocation.Validity.closeExceptionDeal_ok_click)
        self.click_by_xpath(ElementsLocation.Validity.userId_ok_click)
        self.click_by_xpath(ElementsLocation.Validity.loginOut_ok_click)

    def Validity_Inq_TodayExpiringDry(self):
        MyLog.info(f"今日即将到期，干货库")
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.todayTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.dry_code_input, self.dryCode)
        self.click_by_xpath(ElementsLocation.Validity.dry_inq_click)
        # 只展示第一行
        my_list = self.get_table_listone()
        print(my_list)
        print(self.time_date)
        time.sleep(1)
        assert self.time_date == my_list[6]

    def Validity_Inq_expiredDryProduction(self):
        # MyLog.info(f"干货库调拨流水")
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.expiredDryCode)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
        #                    database=self.database, charset='utf8')
        # data = Validitydb.query_sql_one(
        #     f'SELECT cqe12.store_code,cqe12.item_code,cqe12.expired_time FROM `cic_quality_expire_12` cqe12 where cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.expiredDryCode}" AND cqe12.batch_time="2022-02-28"')
        # print(data)
        my_list = self.get_table_listone()
        print(my_list)
        assert my_list[6] < self.time_date

    def Validity_Inq_expiredDry(self):
        # MyLog.info(f"干货库进货流水")
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.expiredDryCode2)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
        #                    database=self.database, charset='utf8')
        # data = Validitydb.query_sql_one(
        #     f'SELECT cqe12.store_code,cqe12.item_code,cqe12.expired_time FROM `cic_quality_expire_12` cqe12 where '
        #     f'cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.expiredDryCode2}" AND '
        #     f'cqe12.batch_time="2020-1-1"')
        # print(data)
        # # 转换成2022-12-02形式
        # expired_time = data[2].strftime("%Y-%m-%d")
        my_list = self.get_table_listone()
        print(my_list)
        assert my_list[6] < self.time_date

    def Validity_dealDataAfterTest(self):
        MyLog.info(f"测试后处理数据")
        time.sleep(1)
        # 已过期未报废-冷冻库 86110010 冷冻薯条 保质期365 选择生产日期2021-12-5
        # self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        # self.click_by_xpath(ElementsLocation.Validity.cold_click)
        # self.input_text(ElementsLocation.Validity.vegetables_code_input, self.cold_code)
        # time.sleep(1)
        # self.click_by_xpath(ElementsLocation.Validity.inq_click)
        # self.click_by_xpath(ElementsLocation.Validity.delete_click)
        # self.click_by_xpath(ElementsLocation.Validity.delete_ok_click)
        # 今日即将到期-干货库 86110623 大米
        self.click_by_xpath(ElementsLocation.Validity.todayTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.dryCode)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_ok_click)
        # 已过期未报废-干货库 86110383 纯牛奶-1升*12盒/箱 保质期180
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.expiredDryCode)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_ok_click)
        # 已过期未报废-干货库 86132846 冰激凌花筒60g白牛纸托_小黄人香蕉-250个*8条/箱
        self.click_by_xpath(ElementsLocation.Validity.expiredTab_click)
        self.click_by_xpath(ElementsLocation.Validity.dry_ok_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.expiredDryCode2)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_click)
        self.click_by_xpath(ElementsLocation.Validity.delete_ok_click)

    def Validity_Inq_newRetailingProduct(self):
        MyLog.info(f"新零售临期品")
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.newRetailingTab_click)
        self.click_by_xpath(ElementsLocation.Validity.cold_click)
        self.input_text(ElementsLocation.Validity.vegetables_code_input, self.newRetailingCode)
        time.sleep(1)
        self.click_by_xpath(ElementsLocation.Validity.inq_click)
        Validitydb = mysql(host=self.host, port=self.port, user=self.user, password=self.password,
                           database=self.database, charset='utf8')
        data = Validitydb.query_sql_one(
            f'SELECT cqe12.store_code,cqe12.item_code,cqe12.expired_time,cqe12.offline_sail_time FROM '
            f'`cic_quality_expire_12` cqe12 where '
            f'cqe12.store_code ="{self.my_store_code}" AND cqe12.item_code ="{self.newRetailingCode}" AND '
            f'cqe12.batch_time="2022-1-14"')
        print(data)
        print(data[3])  # 报废时间-配置的仅线下售卖的时间
        # 转换成2022-12-02形式
        expired_time = data[2].strftime("%Y-%m-%d")
        assert expired_time < self.time_date
