import pytest
from common import global_var
from common.log import MyLog
from pluggy import HookspecMarker
from selenium import webdriver

from common.ui_mobile.init_assistant_machine import AssistantMachine
from services.merchandise.Validity.api import Api

global_var.init()

hookspec = HookspecMarker("pytest")


@hookspec(firstresult=True)
def pytest_runtest_protocol(item, nextitem):
    global_var.set_value("method_name", item.name)


@pytest.fixture(autouse=True)
def print_method_name():
    my_method_name = global_var.get_value("method_name")
    MyLog.info(f"马上执行 {my_method_name}")


@pytest.fixture(scope='session', autouse=True)
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {"": ""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    chrome_options.add_experimental_option("prefs", prefs)
    my_driver = webdriver.Chrome(options=chrome_options)
    my_driver.get("http://10.218.223.214:8081/IH_WEB/#/login")
    my_driver.maximize_window()
    print('测试是否走到这一步')
    yield my_driver
    print("用例測試結束")
    # my_driver.close()


def scan_QR_code():
    my_assistant_init = AssistantMachine()
    my_assistant_init.scan_qi_wei_QRcode(2)


@pytest.fixture(scope="class", autouse=True)
def createData(init_driver):
    # 准备数据
    print("准备数据")
    my_web_driver = init_driver
    my_web_driver.get("http://10.218.223.214:8081/IH_WEB/#/login")
    # my_web_driver.minimize_window()
    Validity = Api(my_web_driver)
    Validity.Validity_Sign_in()  # 登录
    Validity.Validity_Choose_kfc()  # 选择品牌
    Validity.Validity_Sign_in()  # 登录
    Validity.Validity_Choose_kfc()  # 选择品牌
    Validity.Validity_CreateData()


@pytest.fixture(scope="class", autouse=True)
def dealDataAfterTest_class(init_driver):
    yield
    print("删除创建的数据")
    # 删除创建的数据
    my_web_driver = init_driver
    # my_web_driver.get("http://10.218.223.214:8081/IH_WEB/#/login")
    Validity = Api(my_web_driver)
    # Validity.Validity_Sign_in()  # 登录
    # Validity.Validity_Choose_kfc()  # 选择品牌
    # Validity.Validity_Sign_in()  # 登录
    # Validity.Validity_Choose_kfc()  # 选择品牌
    # Validity.Validity_Choose_store()
    Validity.Validity_dealDataAfterTest()
    my_web_driver.quit()
