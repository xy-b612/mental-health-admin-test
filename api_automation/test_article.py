import requests
from config import BASE_URL, CODE_SUCCESS, TEST_USERNAME, TEST_PASSWORD


def test_article_page(token):
    """创建IF_ARTICLE_001 获取文章分页列表"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/page",
        headers={"token": token},
        params={
            "pageNum": 1,
            "pageSize": 10,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取文章分页列表失败：{data}"


def test_article_page_samllPage(token):
    """创建IF_ARTICLE_002 获取文章分页列表-小页码"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/page",
        headers={"token": token},
        params={
            "pageNum": 0,
            "pageSize": 10,
        },
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取文章分页列表失败：{data}"


def test_article_detail(token):
    """创建IF_ARTICLE_003 获取存在id的文章详情"""
    # 先创建一个文章
    create_resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
    data = create_resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    article_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    resp = requests.get(
        BASE_URL + f"/knowledge/article/{article_id}",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取文章详情失败：{data}"


def test_article_detail_emptyId(token):
    """创建IF_ARTICLE_004 不存在id的文章详情"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200          # 后端统一 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS     # 业务失败


def test_article_create(token):
    """创建IF_ARTICLE_005 正常新增文章"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    assert data["data"]["id"], "返回文章id为空"


def test_article_create_emptyTitle(token):
    """创建IF_ARTICLE_006 标题为空"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "categoryId": 1,  # 必填，1~4 有效
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"标题为空，但是文章提交成功：{data}"


def test_article_create_emptyContent(token):
    """创建IF_ARTICLE_007 内容为空"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"内容为空，但是文章提交成功：{data}"


def test_article_change(token):
    """创建IF_ARTICLE_008 更新存在id的文章详情"""
    # 先创建一个文章
    create_resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
    data = create_resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    article_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    # 更新文章
    update_resp = requests.put(
        BASE_URL + f"/knowledge/article/{article_id}",
        headers={"token": token},
        json={
            "title": "更新后的测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "content": "更新后的测试内容",  # 必填
            "summary": "更新后的测试摘要",  # 可选
        },
        timeout=10,
    )
    assert update_resp.status_code == 200, f"HTTP状态异常：{update_resp.status_code}"
    data = update_resp.json()
    assert data["code"] == CODE_SUCCESS, f"更新文章失败：{data}"


def test_article_change_emptyId(token):
    """创建IF_ARTICLE_009 更新 不存在id的文章详情"""
    resp = requests.put(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        json={
            "title": "更新后的测试文章",
            "categoryId": 1,  # 必填，1~4 有效
            "content": "更新后的测试内容",  # 必填
            "summary": "更新后的测试摘要",  # 可选
        },
        timeout=10,
    )
    assert resp.status_code == 200          # 后端统一 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS     # 业务失败


def test_article_up(token):
    """创建IF_ARTICLE_010 上架文章"""
    # 先创建一个文章
    create_resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 修复：使用已经解析好的data，不重复调用json()
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
    data = create_resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    article_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    # 上架文章
    up_resp = requests.put(
        BASE_URL + f"/knowledge/article/{article_id}/status",
        headers={"token": token},
        json={
            "status": 1,  # 1：上架，2：下架
        },
        timeout=10,
    )
    assert up_resp.status_code == 200, f"HTTP状态异常：{up_resp.status_code}"
    data = up_resp.json()
    assert data["code"] == CODE_SUCCESS, f"上架文章失败：{data}"


def test_article_down(token):
    """创建IF_ARTICLE_011 下架文章"""
    # 先创建一个文章
    create_resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 修复：使用已经解析好的data，不重复调用json()
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
    data = create_resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    article_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    # 下架文章
    down_resp = requests.put(
        BASE_URL + f"/knowledge/article/{article_id}/status",
        headers={"token": token},
        json={
            "status": 2,  # 1：上架，2：下架
        },
        timeout=10,
    )
    assert down_resp.status_code == 200, f"HTTP状态异常：{down_resp.status_code}"
    data = down_resp.json()
    assert data["code"] == CODE_SUCCESS, f"下架文章失败：{data}"


def test_article_delete(token):
    """创建IF_ARTICLE_012 删除存在id文章"""
    # 先创建一个文章
    create_resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,  # 修复：使用已经解析好的data，不重复调用json()
            "content": "测试内容",  # 必填
            "summary": "测试摘要",  # 可选
        },
        timeout=10,
    )
    assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
    data = create_resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    article_id = data["data"]["id"]  # 修复：使用已经解析好的data，不重复调用json()

    # 删除文章
    resp = requests.delete(
        BASE_URL + f"/knowledge/article/{article_id}",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"删除文章失败：{data}"


def test_article_delete_emptyId(token):
    """创建IF_ARTICLE_013 删除不存在id文章"""
    resp = requests.delete(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200          # 后端统一 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS     # 业务失败
