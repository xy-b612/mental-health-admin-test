import requests
import time

from config import BASE_URL, CODE_SUCCESS


def test_register_success():
    """05 正常注册"""
    # 生成唯一账号
    unique = str(int(time.time() * 1000))
    # 发送请求
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
    # 断言
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"注册失败：{data}"

def test_register_empty_email():
    """06 注册失败：邮箱为空"""
    unique = str(int(time.time() * 1000))
    resp = requests.post(
        BASE_URL + "/user/add",
        json={
            "username": "test_" + unique,
            "password":"123456",
            "confirmPassword":"123456"
        },
        timeout=10
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"]!=CODE_SUCCESS, f"注册成功：{data}"

def test_register_wrong_email():
    """07 注册失败：邮箱格式错误"""
    unique = str(int(time.time() * 1000))
    resp = requests.post(
        BASE_URL + "/user/add",
        json={
            "username": "test_" + unique,
            "email": unique,
            "password":"123456",
            "confirmPassword":"123456"
        },
        timeout=10
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"]!=CODE_SUCCESS, f"注册成功：{data}"

def test_register_repeated_email():
    """08 注册失败：邮箱已存在"""
    unique = str(int(time.time() * 1000))
    # 构造注册请求体，存到变量，后面可以复用
    register_body = {
        "username": "test_" + unique,
        "email": unique + "@test.com",
        "password":"123456",
        "confirmPassword":"123456"
    }
    # 第一次注册
    first_resp = requests.post(
        BASE_URL + "/user/add",
        json=register_body,
        timeout=10
    )
    first_data = first_resp.json()
    # 断言第一次注册必须成功，否则没必要跑第二步
    assert first_data["code"] == CODE_SUCCESS, f"首次注册失败：{first_data}"

    # 第二次，发送完全相同的body，重复邮箱注册
    resp = requests.post(
        BASE_URL + "/user/add",
        json=register_body,
        timeout=10
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    # 重复邮箱，预期业务code不等于200
    assert data["code"] != CODE_SUCCESS, f"邮箱重复，但是居然注册成功了！{data}"