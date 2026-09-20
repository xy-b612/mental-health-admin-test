# mental-health-admin 接口自动化测试总结报告

> **版本**：V1.0 | **日期**：2026-09-20 | **测试人**：小杨 | **技术栈**：Python + pytest + requests

---

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 自动化框架 | pytest + requests（Python） |
| 覆盖接口 | 16 个 REST CRUD 接口（5 个特殊接口手工覆盖） |
| 测试用例总数 | 39 条 |
| 通过用例数 | 33 条 |
| 失败用例数 | 6 条（**全部为缺陷证据**） |
| 通过率 | 84.6% |
| 发现缺陷 | 6 个（均为接口层缺陷） |
| 报告工具 | pytest-html |

**自动化范围说明**：SSE 流式（依赖 AI）、AI 情绪分析（依赖 AI）、数据统计（依赖数据）、分类树（简单查询）、文件上传（需文件准备）5 个接口不适合断言自动化，已通过手工功能测试覆盖。

---

## 2. 接口覆盖清单

| 模块 | 接口数 | 用例数 | 通过 | 失败 |
|------|--------|--------|------|------|
| 用户（login/add/logout） | 3 | 10 | 7 | 3 |
| 心理咨询（session） | 4 | 9 | 8 | 1 |
| 情绪日记（emotion-diary） | 3 | 7 | 5 | 2 |
| 知识文章（knowledge/article） | 6 | 13 | 13 | 0 |
| **合计** | **16** | **39** | **33** | **6** |

---

## 3. 缺陷清单（接口自动化发现）

| ID | 缺陷标题 | 严重等级 | 发现用例 |
|----|---------|---------|---------|
| BUG-001 | 注册邮箱格式未校验，非法邮箱可注册成功 | C-一般 | test_register_wrong_email |
| BUG-004 | 情绪日记核心字段（moodScore/dominantEmotion）后端无必填校验 | C-一般 | test_diary_create_empty_moodScore / empty_dominantEmotion |
| BUG-006 | 登出接口无 token 鉴权，未登录可调用成功 | C-一般 | test_logout_without_token |
| BUG-007 | 注册缺 email 字段也可注册成功（后端不校验 email 必填） | C-一般 | test_register_empty_email |
| BUG-008 | 查询不存在的会话消息返回"成功+null"，非友好错误提示 | D-轻微 | test_session_chat_emptyID |
| BUG-009 | 创建会话返回的 sessionId（带 session_ 前缀）与删除/查询接口期望的 id（纯数字）格式不一致 | D-轻微 | 探测发现 |

> **补充发现（手工 + 探测）**：普通用户（userType=1）可通过接口直接创建文章，绕过后台管理员权限限制（前端路由守卫之外的后端鉴权缺失）。

---

## 4. 踩坑经验总结（本项目的核心学习成果）

| # | 坑 | 正确做法 |
|---|-----|---------|
| 1 | `!= 200`（数字）vs `!= "200"`（字符串） | 字符串和数字永远不等，用 `CODE_SUCCESS` 常量 |
| 2 | HTTP 状态码 vs 业务 code 混淆 | 状态码看拦截（403），业务结果看 body 的 `code` |
| 3 | 盲目 `resp.json()` | 只有 200 才解析，403/404/500 直接看状态码 |
| 4 | 接口路径单复数（`session` vs `sessions`） | 路径每个字母都是接口的一部分，逐个核对文档 |
| 5 | id 格式不一致（`session_37766` vs `37766`） | 创建返回的 id 与删除期望的 id 格式要验证 |
| 6 | 返回结构差异（字典 `{records}` vs 列表 `[...]`） | 探测后确认 data 是字典还是数组 |

---

## 5. 关键结论

1. **接口自动化成功复现并扩展了功能测试的缺陷**：BUG-001（邮箱格式）、BUG-004（字段校验）在接口层得到确认，且发现后端连评分字段都不校验。
2. **接口自动化发现了手工测试测不到的缺陷**：BUG-006（登出无鉴权）、BUG-007（缺 email）、BUG-009（id 前缀不一致）——这些是页面自动带 token 或前端绕开，手工测不出来的。
3. **鉴权并非普遍缺失**：情绪日记分页、知识文章读接口无 token 均返回 403（有鉴权），仅登出接口漏了（BUG-006）。

---

## 6. 产出物清单

| 序号 | 产出物 | 路径 |
|------|--------|------|
| 1 | 自动化脚本 | `api_automation/`（config.py / conftest.py / test_user.py / test_register.py / test_diary.py / test_article.py / test_session.py） |
| 2 | HTML 测试报告 | `api_automation/report.html` |
| 3 | 接口测试用例 | `doc/mental-health-admin接口测试用例.md` |
| 4 | 本总结报告 | 本文档 |

---

## 7. 后续计划

1. **缺陷回归**：后端修复后，重新跑 `pytest`，6 条 FAIL 转 PASS 即验证修复。
2. **参数化优化**：用 `@pytest.mark.parametrize` 把重复用例做数据驱动。
3. **CI 集成**：接入 Jenkins/GitHub Actions，实现提测自动跑。
