# -*- coding: utf-8 -*-
"""pytest 公共 fixture：登录拿 token，所有用例复用"""
import pytest
import requests
from config import BASE_URL, TEST_USERNAME, TEST_PASSWORD, CODE_SUCCESS

# `@pytest.fixture` 是 pytest 的装饰器，代表下面这个`token()`是**夹具（前置脚本）**，等价 Postman 的 Pre‑request Script。
@pytest.fixture(scope="session")
def token():
    """登录一次，拿到 token，整个测试会话复用（不用每个用例都登录一次）"""
    url = BASE_URL + "/user/login"
    body = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
    resp = requests.post(url, json=body, timeout=10)
    data = resp.json()
    # 断言登录成功，失败时抛出带提示的错误
    assert data["code"] == CODE_SUCCESS, f"登录失败，请检查 config.py 账号密码：{data}"
    return data["data"]["token"]
