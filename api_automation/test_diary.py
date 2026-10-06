import allure
import requests
from config import BASE_URL, CODE_SUCCESS


@allure.feature("情绪日记")
@allure.story("新增日记")
@allure.title("IF_DIARY_001 正常提交日记")
@allure.severity(allure.severity_level.NORMAL)
def test_diary_create(token):
    """正常提交日记"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",
            "moodScore": 5,
            "dominantEmotion": "开心",
            "emotionTriggers": "工作压力",
            "diaryContent": "今天有点累",
            "sleepQuality": 4,
            "stressLevel": 2,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"提交日记失败：{data}"


@allure.feature("情绪日记")
@allure.story("新增日记")
@allure.title("IF_DIARY_002 缺 moodScore 提交（BUG-004）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：后端未校验 moodScore 必填，缺字段仍可提交成功，本用例持续红，用于缺陷回归")
def test_diary_create_empty_moodScore(token):
    """提交日记失败：moodScore为空（不传字段）"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",
            "dominantEmotion": "开心",
            "emotionTriggers": "工作压力",
            "diaryContent": "今天有点累",
            "sleepQuality": 4,
            "stressLevel": 2,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"moodScore为空，但是日记提交成功：{data}"


@allure.feature("情绪日记")
@allure.story("新增日记")
@allure.title("IF_DIARY_003 缺 dominantEmotion 提交（BUG-004）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：后端未校验 dominantEmotion 必填，缺字段仍可提交成功，本用例持续红，用于缺陷回归")
def test_diary_create_empty_dominantEmotion(token):
    """提交日记失败：dominantEmotion为空（不传字段）"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",
            "moodScore": 5,
            "emotionTriggers": "工作压力",
            "diaryContent": "今天有点累",
            "sleepQuality": 4,
            "stressLevel": 2,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"dominantEmotion为空，但是日记提交成功：{data}"


@allure.feature("情绪日记")
@allure.story("后台分页")
@allure.title("IF_DIARY_004 日记分页查询")
@allure.severity(allure.severity_level.NORMAL)
def test_diary_page(token):
    """获取日记分页列表"""
    resp = requests.get(
        BASE_URL + "/emotion-diary/admin/page",
        headers={"token": token},
        params={"pageNum": 1, "pageSize": 10},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取日记分页列表失败：{data}"


@allure.feature("情绪日记")
@allure.story("后台分页")
@allure.title("IF_DIARY_005 无 Token 分页-应被拦截")
@allure.severity(allure.severity_level.CRITICAL)
def test_diary_page_emptyToken():
    """无Token获取日记分页列表"""
    resp = requests.get(
        BASE_URL + "/emotion-diary/admin/page",
        headers={},
        params={"pageNum": 1, "pageSize": 10},
        timeout=10,
    )
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


@allure.feature("情绪日记")
@allure.story("后台删除")
@allure.title("IF_DIARY_006 删除存在的日记")
@allure.severity(allure.severity_level.NORMAL)
def test_diary_delete_id(token):
    """删除存在id的日记"""
    with allure.step("1. 先创建一条日记，获取 id"):
        create_resp = requests.post(
            BASE_URL + "/emotion-diary",
            headers={"token": token},
            json={
                "diaryDate": "2026-09-20",
                "moodScore": 5,
                "dominantEmotion": "开心",
                "emotionTriggers": "工作压力",
                "diaryContent": "今天有点累",
                "sleepQuality": 4,
                "stressLevel": 2,
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"提交日记失败：{data}"
        diary_id = data["data"]["id"]

    with allure.step("2. 删除该日记，断言删除成功"):
        resp = requests.delete(
            BASE_URL + f"/emotion-diary/admin/{diary_id}",
            headers={"token": token},
            timeout=10,
        )
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        del_data = resp.json()
        assert del_data["code"] == CODE_SUCCESS, f"在存在id的情况下，日记删除失败：{del_data}"


@allure.feature("情绪日记")
@allure.story("后台删除")
@allure.title("IF_DIARY_007 删除不存在的日记")
@allure.severity(allure.severity_level.NORMAL)
def test_diary_delete_id_emptyId(token):
    """删除不存在id的日记"""
    not_exist_id = "10000000000000000000000000000000"
    resp = requests.delete(
        BASE_URL + f"/emotion-diary/admin/{not_exist_id}",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"在不存在id的情况下，日记删除成功：{data}"
