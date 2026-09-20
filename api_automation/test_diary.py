import requests
from config import BASE_URL, CODE_SUCCESS


def test_diary_create(token):
    """正常提交日记"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",  # 必填！不传报错
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


def test_diary_create_empty_moodScore(token):
    """提交日记失败：moodScore为空（不传字段）"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",  # 必填！不传报错
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


def test_diary_create_empty_dominantEmotion(token):
    """提交日记失败：dominantEmotion为空（不传字段）"""
    resp = requests.post(
        BASE_URL + "/emotion-diary",
        headers={"token": token},
        json={
            "diaryDate": "2026-09-20",  # 必填！不传报错
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
    assert data["code"] != CODE_SUCCESS, (
        f"dominantEmotion为空，但是日记提交成功：{data}"
    )


def test_diary_page(token):
    """获取日记分页列表"""
    resp = requests.get(
        BASE_URL + "/emotion-diary/admin/page",
        headers={"token": token},
        params={
            "pageNum": 1,
            "pageSize": 10,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取日记分页列表失败：{data}"


def test_diary_page_emptyToken():
    """无Token获取日记分页列表"""
    resp = requests.get(
        BASE_URL + "/emotion-diary/admin/page",
        headers={},
        params={
            "pageNum": 1,
            "pageSize": 10,
        },
        timeout=10,
    )
    # 注意：确认你的接口无token返回的http码，如果不是403，修改此处
    assert resp.status_code == 403, f"无 token 应返回 403，实际：{resp.status_code}"


def test_diary_delete_id(token):
    """删除存在id的日记"""
    # 先创建一个日记
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

    diary_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    resp = requests.delete(
        BASE_URL + f"/emotion-diary/admin/{diary_id}",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    del_data = resp.json()
    assert del_data["code"] == CODE_SUCCESS, (
        f"在存在id的情况下，日记删除失败：{del_data}"
    )


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
