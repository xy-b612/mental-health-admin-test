import requests
from config import BASE_URL, TEST_USERNAME, TEST_PASSWORD, CODE_SUCCESS


def test_session_start(token):
    """IF_SESSION_001 正常创建会话"""
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        headers={"token": token},
        json={"initialMessage": "你好"},  # 必填
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
    assert "sessionId" in data["data"], "sessionId 为空"


def test_session_start_emptyToken():
    """IF_SESSION_002 未登录创建会话"""
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        json={"initialMessage": "你好"},  # 必填
        timeout=10,
    )
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


def test_session_page(token):
    """IF_SESSION_003 获取正常分页消息列表"""
    resp = requests.get(
        BASE_URL + "/psychological-chat/sessions",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取分页消息列表失败：{data}"
    assert "records" in data["data"], "返回缺少records字段"


def test_session_smallPage(token):
    """IF_SESSION_004 正常分页消息列表（0）"""
    resp = requests.get(
        BASE_URL + "/psychological-chat/sessions",
        headers={"token": token},
        params={"pageNum": 0, "pageSize": 10},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取分页消息列表失败：{data}"
    assert "records" in data["data"], "返回缺少records字段"


def test_session_emptyToken():
    """IF_SESSION_005 未登录获取分页消息列表"""
    resp = requests.get(
        BASE_URL + "/psychological-chat/sessions",
        timeout=10,
    )
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


def test_session_delete(token):
    """IF_SESSION_006 删除存在的会话"""
    # 先创建一个会话
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        headers={"token": token},
        json={"initialMessage": "你好"},  # 必填
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
    assert "sessionId" in data["data"], "sessionId 为空"
    # 删除会话
    resp = requests.delete(
        BASE_URL
        + f"/psychological-chat/sessions/{data['data']['sessionId'].replace('session_', '')}",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"删除失败：{data}"


def test_session_delete_emptyID(token):
    """IF_SESSION_007 删除不存在的会话"""
    resp = requests.delete(
        BASE_URL + "/psychological-chat/sessions/123456",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"删除成功：{data}"


def test_session_chat(token):
    """IF_SESSION_008 正常获取会话消息"""
    # 先创建一个会话
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        headers={"token": token},
        json={"initialMessage": "你好"},  # 必填
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
    assert "sessionId" in data["data"], "sessionId 为空"
    # 获取会话消息
    resp = requests.get(
        BASE_URL
        + f"/psychological-chat/sessions/{data['data']['sessionId'].replace('session_', '')}/messages",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取会话消息失败：{data}"
    assert data["data"], "消息列表为空"


def test_session_chat_emptyID(token):
    """IF_SESSION_009 获取不存在的会话消息"""
    resp = requests.get(
        BASE_URL + "/psychological-chat/sessions/123456/messages",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"获取会话消息成功：{data}"
