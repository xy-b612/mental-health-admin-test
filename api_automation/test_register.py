import allure
import requests
import time

from config import BASE_URL, CODE_SUCCESS


@allure.feature("用户接口")
@allure.story("注册")
@allure.title("IF_USER_005 正常注册")
@allure.severity(allure.severity_level.NORMAL)
def test_register_success():
    """05 正常注册"""
    unique = str(int(time.time() * 1000))
    resp = requests.post(
        BASE_URL + "/user/add",
        json={
            "username": "test_" + unique,
            "email": unique + "@test.com",
            "password": "123456",
            "confirmPassword": "123456",
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"注册失败：{data}"


@allure.feature("用户接口")
@allure.story("注册")
@allure.title("IF_USER_006 缺 email 注册")
@allure.severity(allure.severity_level.NORMAL)
def test_register_empty_email():
    """06 注册失败：邮箱为空"""
    unique = str(int(time.time() * 1000))
    resp = requests.post(
        BASE_URL + "/user/add",
        json={
            "username": "test_" + unique,
            "password": "123456",
            "confirmPassword": "123456"
        },
        timeout=10
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"注册成功：{data}"


@allure.feature("用户接口")
@allure.story("注册")
@allure.title("IF_USER_007 非法邮箱格式注册（BUG-001）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：邮箱格式未校验，非法邮箱可注册成功，本用例持续红，用于缺陷回归")
def test_register_wrong_email():
    """07 注册失败：邮箱格式错误"""
    unique = str(int(time.time() * 1000))
    resp = requests.post(
        BASE_URL + "/user/add",
        json={
            "username": "test_" + unique,
            "email": unique,
            "password": "123456",
            "confirmPassword": "123456"
        },
        timeout=10
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"注册成功：{data}"


@allure.feature("用户接口")
@allure.story("注册")
@allure.title("IF_USER_008 重复邮箱注册")
@allure.severity(allure.severity_level.NORMAL)
def test_register_repeated_email():
    """08 注册失败：邮箱已存在"""
    unique = str(int(time.time() * 1000))
    register_body = {
        "username": "test_" + unique,
        "email": unique + "@test.com",
        "password": "123456",
        "confirmPassword": "123456"
    }

    with allure.step("1. 首次注册（预期成功）"):
        first_resp = requests.post(BASE_URL + "/user/add", json=register_body, timeout=10)
        first_data = first_resp.json()
        assert first_data["code"] == CODE_SUCCESS, f"首次注册失败：{first_data}"

    with allure.step("2. 相同邮箱再次注册（预期失败）"):
        resp = requests.post(BASE_URL + "/user/add", json=register_body, timeout=10)
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        data = resp.json()
        assert data["code"] != CODE_SUCCESS, f"邮箱重复，但是居然注册成功了！{data}"
