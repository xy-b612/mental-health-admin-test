import allure
import requests
from config import BASE_URL, CODE_SUCCESS


@allure.feature("心理咨询")
@allure.story("会话管理")
@allure.title("IF_SESSION_001 正常创建会话")
@allure.severity(allure.severity_level.NORMAL)
def test_session_start(token):
    """IF_SESSION_001 正常创建会话"""
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        headers={"token": token},
        json={"initialMessage": "你好"},
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
    assert "sessionId" in data["data"], "sessionId 为空"


@allure.feature("心理咨询")
@allure.story("会话管理")
@allure.title("IF_SESSION_002 无 Token 创建会话-应被拦截")
@allure.severity(allure.severity_level.CRITICAL)
def test_session_start_emptyToken():
    """IF_SESSION_002 未登录创建会话"""
    resp = requests.post(
        BASE_URL + "/psychological-chat/session/start",
        json={"initialMessage": "你好"},
        timeout=10,
    )
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


@allure.feature("心理咨询")
@allure.story("会话列表")
@allure.title("IF_SESSION_003 会话列表查询")
@allure.severity(allure.severity_level.NORMAL)
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


@allure.feature("心理咨询")
@allure.story("会话列表")
@allure.title("IF_SESSION_004 会话列表分页边界（pageNum=0）")
@allure.severity(allure.severity_level.MINOR)
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


@allure.feature("心理咨询")
@allure.story("会话列表")
@allure.title("IF_SESSION_005 无 Token 查询会话列表-应被拦截")
@allure.severity(allure.severity_level.CRITICAL)
def test_session_emptyToken():
    """IF_SESSION_005 未登录获取分页消息列表"""
    resp = requests.get(
        BASE_URL + "/psychological-chat/sessions",
        timeout=10,
    )
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


@allure.feature("心理咨询")
@allure.story("会话管理")
@allure.title("IF_SESSION_006 删除存在的会话")
@allure.severity(allure.severity_level.NORMAL)
def test_session_delete(token):
    """IF_SESSION_006 删除存在的会话"""
    with allure.step("1. 创建会话，获取 sessionId 并去除 session_ 前缀"):
        resp = requests.post(
            BASE_URL + "/psychological-chat/session/start",
            headers={"token": token},
            json={"initialMessage": "你好"},
            timeout=10,
        )
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
        assert "sessionId" in data["data"], "sessionId 为空"
        # 创建返回的 sessionId 带 session_ 前缀，删除接口需纯数字 id
        session_id = data["data"]["sessionId"].replace("session_", "")

    with allure.step("2. 删除该会话，断言删除成功"):
        resp = requests.delete(
            BASE_URL + f"/psychological-chat/sessions/{session_id}",
            headers={"token": token},
            timeout=10,
        )
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"删除失败：{data}"


@allure.feature("心理咨询")
@allure.story("会话管理")
@allure.title("IF_SESSION_007 删除不存在的会话")
@allure.severity(allure.severity_level.NORMAL)
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


@allure.feature("心理咨询")
@allure.story("会话消息")
@allure.title("IF_SESSION_008 获取会话消息")
@allure.severity(allure.severity_level.NORMAL)
def test_session_chat(token):
    """IF_SESSION_008 正常获取会话消息"""
    with allure.step("1. 创建会话，获取 sessionId 并去除 session_ 前缀"):
        resp = requests.post(
            BASE_URL + "/psychological-chat/session/start",
            headers={"token": token},
            json={"initialMessage": "你好"},
            timeout=10,
        )
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"创建失败：{data}"
        assert "sessionId" in data["data"], "sessionId 为空"
        session_id = data["data"]["sessionId"].replace("session_", "")

    with allure.step("2. 查询该会话消息，断言返回消息列表"):
        resp = requests.get(
            BASE_URL + f"/psychological-chat/sessions/{session_id}/messages",
            headers={"token": token},
            timeout=10,
        )
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"获取会话消息失败：{data}"
        assert data["data"], "消息列表为空"


@allure.feature("心理咨询")
@allure.story("会话消息")
@allure.title("IF_SESSION_009 获取不存在的会话消息（BUG-008）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：查询不存在的会话消息，后端返回 code=200 + data=null，未做友好提示，本用例持续红，用于缺陷回归")
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
