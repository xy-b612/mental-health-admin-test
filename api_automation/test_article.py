import allure
import requests
from config import BASE_URL, CODE_SUCCESS


@allure.feature("知识文章")
@allure.story("文章分页")
@allure.title("IF_ARTICLE_001 文章分页查询")
@allure.severity(allure.severity_level.NORMAL)
def test_article_page(token):
    """IF_ARTICLE_001 获取文章分页列表"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/page",
        headers={"token": token},
        params={"pageNum": 1, "pageSize": 10},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取文章分页列表失败：{data}"


@allure.feature("知识文章")
@allure.story("文章分页")
@allure.title("IF_ARTICLE_002 文章分页边界（pageNum=0）")
@allure.severity(allure.severity_level.MINOR)
def test_article_page_samllPage(token):
    """IF_ARTICLE_002 获取文章分页列表-小页码"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/page",
        headers={"token": token},
        params={"pageNum": 0, "pageSize": 10},
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"获取文章分页列表失败：{data}"


@allure.feature("知识文章")
@allure.story("文章详情")
@allure.title("IF_ARTICLE_003 查询存在的文章详情")
@allure.severity(allure.severity_level.NORMAL)
def test_article_detail(token):
    """IF_ARTICLE_003 获取存在id的文章详情"""
    with allure.step("1. 创建文章，获取 article_id"):
        create_resp = requests.post(
            BASE_URL + "/knowledge/article",
            headers={"token": token},
            json={
                "title": "测试文章",
                "categoryId": 1,
                "content": "测试内容",
                "summary": "测试摘要",
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
        article_id = data["data"]["id"]

    with allure.step("2. 查询该文章详情，断言成功"):
        resp = requests.get(
            BASE_URL + f"/knowledge/article/{article_id}",
            headers={"token": token},
            timeout=10,
        )
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"获取文章详情失败：{data}"


@allure.feature("知识文章")
@allure.story("文章详情")
@allure.title("IF_ARTICLE_004 查询不存在的文章详情")
@allure.severity(allure.severity_level.NORMAL)
def test_article_detail_emptyId(token):
    """IF_ARTICLE_004 不存在id的文章详情"""
    resp = requests.get(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200          # 后端统一 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS     # 业务失败


@allure.feature("知识文章")
@allure.story("新增文章")
@allure.title("IF_ARTICLE_005 正常新增文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_create(token):
    """IF_ARTICLE_005 正常新增文章"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,
            "content": "测试内容",
            "summary": "测试摘要",
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
    assert data["data"]["id"], "返回文章id为空"


@allure.feature("知识文章")
@allure.story("新增文章")
@allure.title("IF_ARTICLE_006 标题为空新增（BUG-005）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：前端必填校验未生效，空标题可创建文章；后端有校验兜底，本用例断言后端行为")
def test_article_create_emptyTitle(token):
    """IF_ARTICLE_006 标题为空"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "categoryId": 1,
            "content": "测试内容",
            "summary": "测试摘要",
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"标题为空，但是文章提交成功：{data}"


@allure.feature("知识文章")
@allure.story("新增文章")
@allure.title("IF_ARTICLE_007 内容为空新增（BUG-005）")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("已知缺陷：前端必填校验未生效，空内容可创建文章；后端有校验兜底，本用例断言后端行为")
def test_article_create_emptyContent(token):
    """IF_ARTICLE_007 内容为空"""
    resp = requests.post(
        BASE_URL + "/knowledge/article",
        headers={"token": token},
        json={
            "title": "测试文章",
            "categoryId": 1,
            "summary": "测试摘要",
        },
        timeout=10,
    )
    data = resp.json()
    assert data["code"] != CODE_SUCCESS, f"内容为空，但是文章提交成功：{data}"


@allure.feature("知识文章")
@allure.story("修改文章")
@allure.title("IF_ARTICLE_008 修改存在的文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_change(token):
    """IF_ARTICLE_008 更新存在id的文章"""
    with allure.step("1. 创建文章，获取 article_id"):
        create_resp = requests.post(
            BASE_URL + "/knowledge/article",
            headers={"token": token},
            json={
                "title": "测试文章",
                "categoryId": 1,
                "content": "测试内容",
                "summary": "测试摘要",
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
        article_id = data["data"]["id"]

    with allure.step("2. 修改文章，断言修改成功"):
        update_resp = requests.put(
            BASE_URL + f"/knowledge/article/{article_id}",
            headers={"token": token},
            json={
                "title": "更新后的测试文章",
                "categoryId": 1,
                "content": "更新后的测试内容",
                "summary": "更新后的测试摘要",
            },
            timeout=10,
        )
        assert update_resp.status_code == 200, f"HTTP状态异常：{update_resp.status_code}"
        data = update_resp.json()
        assert data["code"] == CODE_SUCCESS, f"更新文章失败：{data}"


@allure.feature("知识文章")
@allure.story("修改文章")
@allure.title("IF_ARTICLE_009 修改不存在的文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_change_emptyId(token):
    """IF_ARTICLE_009 更新不存在id的文章"""
    resp = requests.put(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        json={
            "title": "更新后的测试文章",
            "categoryId": 1,
            "content": "更新后的测试内容",
            "summary": "更新后的测试摘要",
        },
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS


@allure.feature("知识文章")
@allure.story("上下架")
@allure.title("IF_ARTICLE_010 上架文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_up(token):
    """IF_ARTICLE_010 上架文章"""
    with allure.step("1. 创建文章，获取 article_id"):
        create_resp = requests.post(
            BASE_URL + "/knowledge/article",
            headers={"token": token},
            json={
                "title": "测试文章",
                "categoryId": 1,
                "content": "测试内容",
                "summary": "测试摘要",
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
        article_id = data["data"]["id"]

    with allure.step("2. 上架文章（status=1），断言成功"):
        up_resp = requests.put(
            BASE_URL + f"/knowledge/article/{article_id}/status",
            headers={"token": token},
            json={"status": 1},
            timeout=10,
        )
        assert up_resp.status_code == 200, f"HTTP状态异常：{up_resp.status_code}"
        data = up_resp.json()
        assert data["code"] == CODE_SUCCESS, f"上架文章失败：{data}"


@allure.feature("知识文章")
@allure.story("上下架")
@allure.title("IF_ARTICLE_011 下架文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_down(token):
    """IF_ARTICLE_011 下架文章"""
    with allure.step("1. 创建文章，获取 article_id"):
        create_resp = requests.post(
            BASE_URL + "/knowledge/article",
            headers={"token": token},
            json={
                "title": "测试文章",
                "categoryId": 1,
                "content": "测试内容",
                "summary": "测试摘要",
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
        article_id = data["data"]["id"]

    with allure.step("2. 下架文章（status=2），断言成功"):
        down_resp = requests.put(
            BASE_URL + f"/knowledge/article/{article_id}/status",
            headers={"token": token},
            json={"status": 2},
            timeout=10,
        )
        assert down_resp.status_code == 200, f"HTTP状态异常：{down_resp.status_code}"
        data = down_resp.json()
        assert data["code"] == CODE_SUCCESS, f"下架文章失败：{data}"


@allure.feature("知识文章")
@allure.story("删除文章")
@allure.title("IF_ARTICLE_012 删除存在的文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_delete(token):
    """IF_ARTICLE_012 删除存在id文章"""
    with allure.step("1. 创建文章，获取 article_id"):
        create_resp = requests.post(
            BASE_URL + "/knowledge/article",
            headers={"token": token},
            json={
                "title": "测试文章",
                "categoryId": 1,
                "content": "测试内容",
                "summary": "测试摘要",
            },
            timeout=10,
        )
        assert create_resp.status_code == 200, f"HTTP状态异常：{create_resp.status_code}"
        data = create_resp.json()
        assert data["code"] == CODE_SUCCESS, f"新增文章失败：{data}"
        article_id = data["data"]["id"]

    with allure.step("2. 删除文章，断言删除成功"):
        resp = requests.delete(
            BASE_URL + f"/knowledge/article/{article_id}",
            headers={"token": token},
            timeout=10,
        )
        assert resp.status_code == 200, f"HTTP状态异常：{resp.status_code}"
        data = resp.json()
        assert data["code"] == CODE_SUCCESS, f"删除文章失败：{data}"


@allure.feature("知识文章")
@allure.story("删除文章")
@allure.title("IF_ARTICLE_013 删除不存在的文章")
@allure.severity(allure.severity_level.NORMAL)
def test_article_delete_emptyId(token):
    """IF_ARTICLE_013 删除不存在id文章"""
    resp = requests.delete(
        BASE_URL + "/knowledge/article/10000000000000000000000000000000",
        headers={"token": token},
        timeout=10,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] != CODE_SUCCESS
