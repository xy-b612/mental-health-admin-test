# AI心理助手（mental-health-admin）测试项目

> 针对 mental-health-admin（Vue 3 心理健康平台）的完整测试产出物，包含**手工功能测试** + **接口自动化测试**（pytest + requests）。

## 📁 目录结构

```
├── doc/                     # 测试文档
│   ├── mental-health-admin需求规格说明书.md
│   ├── mental-health-admin测试计划.md
│   ├── AI心理助手测试点.xmind
│   ├── mental-health-admin测试用例-登录权限模块.md
│   ├── mental-health-admin测试用例-AI心理咨询模块.md
│   ├── mental-health-admin测试用例-情绪日记模块.md
│   ├── mental-health-admin测试用例-知识文章管理模块.md
│   ├── mental-health-admin测试总结报告.md
│   ├── mental-health-admin接口测试用例.md
│   ├── mental-health-admin接口自动化总结报告.md
│   ├── 功能测试用例.xlsx
│   └── 接口测试用例.xlsx
├── api_automation/          # 接口自动化脚本
│   ├── config.py            # 配置（接口地址 + 测试账号）
│   ├── conftest.py          # 登录拿 token 的 fixture
│   ├── test_user.py         # 用户接口（登录/登出）
│   ├── test_register.py     # 注册接口
│   ├── test_diary.py        # 情绪日记接口
│   ├── test_article.py      # 知识文章接口
│   └── test_session.py      # 心理咨询接口
└── image/                   # 测试截图
```

## 🧪 功能测试（手工）

| 模块 | 用例数 | 通过 | 缺陷 |
|------|--------|------|------|
| 登录认证与权限隔离 | 11 | 10 | 1 |
| AI 心理咨询（SSE 流式） | 16 | 13 | 3 |
| 情绪日记 | 9 | 8 | 1 |
| 知识文章管理 | 15 | 13 | 2 |

## 🤖 接口自动化（pytest + requests）

### 环境准备

```bash
pip install requests pytest pytest-html
```

### 配置测试账号

修改 `api_automation/config.py`（需先手动注册一个前台测试账号）：

```python
TEST_USERNAME = "你的测试账号"
TEST_PASSWORD = "你的测试密码"
```

### 运行

```bash
cd api_automation
pytest -v                                # 运行所有用例
pytest --html=report.html --self-contained-html   # 生成 HTML 报告
```

### 覆盖范围

- **16 个 REST CRUD 接口，39 条用例**
- 覆盖维度：正常 / 异常参数 / 边界 / 鉴权（无 token）/ 不存在资源
- 未纳入自动化（已手工覆盖）：SSE 流式、AI 情绪分析、数据统计、分类树、文件上传

## 🐛 缺陷清单（摘要）

| ID | 缺陷 | 等级 |
|----|------|------|
| BUG-001 | 注册邮箱格式未校验 | C |
| BUG-002 | 断网/超时暴露底层错误，无友好提示 | C |
| BUG-004 | 情绪日记核心字段无必填校验 | C |
| BUG-005 | 知识文章必填校验前端未生效 | C |
| BUG-006 | 登出接口无 token 鉴权 | C |
| BUG-007~009 | 缺 email、查不存在会话、sessionId 格式不一致 | C/D |

> 详细缺陷分析见 `doc/` 下的总结报告。

## 🛠 技术栈

- Python 3.10 + pytest + requests
- pytest-html（测试报告）
- 被测系统：Vue 3 心理健康平台（后端为课程方部署的外部服务）
