# -*- coding: utf-8 -*-
"""用户接口测试：登录 / 登出（对应 IF_USER_001~004、009~010）
"""
import allure
import requests
from config import BASE_URL, TEST_USERNAME, TEST_PASSWORD, CODE_SUCCESS


# ---------- 登录 ----------

@allure.feature("用户接口")
@allure.story("登录")
@allure.title("IF_USER_001 正常登录-返回 Token")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success():
    """IF_USER_001 正常登录：code="200"，token 非空"""
    with allure.step("1. 使用正确账号密码请求 /user/login"):
        resp = requests.post(BASE_URL + "/user/login", json={
            "username": TEST_USERNAME, "password": TEST_PASSWORD
        }, timeout=10)
    with allure.step("2. 断言 HTTP 状态码与业务码"):
        data = resp.json()
        assert resp.status_code == 200, f"HTTP 状态码异常：{resp.status_code}"
        assert data["code"] == CODE_SUCCESS, f"业务码异常：{data}"
    with allure.step("3. 断言返回 Token 非空"):
        assert data["data"]["token"], "token 为空"


@allure.feature("用户接口")
@allure.story("登录")
@allure.title("IF_USER_002 错误密码-登录失败")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_wrong_password():
    """IF_USER_002 错误密码：登录失败（code != "200"）"""
    resp = requests.post(BASE_URL + "/user/login", json={
        "username": TEST_USERNAME, "password": "wrong_password_123"
    }, timeout=10)
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"错误密码居然登录成功：{data}"


@allure.feature("用户接口")
@allure.story("登录")
@allure.title("IF_USER_003 空参数-登录失败")
@allure.severity(allure.severity_level.NORMAL)
def test_login_empty_params():
    """IF_USER_003 空参数：登录失败，不返回 500"""
    resp = requests.post(BASE_URL + "/user/login", json={
        "username": "", "password": ""
    }, timeout=10)
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"空参数居然登录成功：{data}"


@allure.feature("用户接口")
@allure.story("登录")
@allure.title("IF_USER_004 不存在用户-登录失败")
@allure.severity(allure.severity_level.NORMAL)
def test_login_not_exist_user():
    """IF_USER_004 不存在用户：登录失败，不返回 500"""
    resp = requests.post(BASE_URL + "/user/login", json={
        "username": "not_exist_user_999", "password": "123456"
    }, timeout=10)
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"不存在用户居然登录成功：{data}"


# ---------- 登出 ----------

@allure.feature("用户接口")
@allure.story("登出")
@allure.title("IF_USER_009 正常登出")
@allure.severity(allure.severity_level.NORMAL)
def test_logout_with_token(token):
    """IF_USER_009 正常登出：带 token，code="200" """
    resp = requests.post(BASE_URL + "/user/logout", headers={"token": token}, timeout=10)
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"登出失败：{data}"


@allure.feature("用户接口")
@allure.story("登出")
@allure.title("IF_USER_010 无 Token 登出-应被拦截")
@allure.severity(allure.severity_level.CRITICAL)
def test_logout_without_token():
    """IF_USER_010 无 token 登出：被拦截（code != "200" 或 HTTP 401/403）"""
    resp = requests.post(BASE_URL + "/user/logout", timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        assert data["code"] != CODE_SUCCESS, f"无 token 居然登出成功：{data}"
    else:
        assert resp.status_code in (401, 403), f"无 token 返回异常状态码：{resp.status_code}"
