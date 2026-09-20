# AI心理健康助手（mental-health-admin）需求规格说明书

> **版本号**：V1.0  
> **日期**：2026-08-24  
> **来源项目**：https://github.com/xy-b612/mental-health-admin.git  
> **当前版本**：V1.0  
> **文档密级**：内部公开  

---

## 修订记录

| 版本 | 日期 | 修订人 | 修订内容 |
|------|------|--------|----------|
| V1.0 | 2026-08-24 | 小杨 | 初稿，覆盖全部现有功能模块 |

---

## 1. 引言

### 1.1 项目背景

AI心理健康助手是一款基于 Vue 3 + 人工智能的心理健康支持平台，面向有情绪管理、心理咨询、心理健康知识学习需求的普通用户，同时为管理人员提供数据分析与内容管理能力。系统通过 AI 实时流式对话、情绪分析、情绪日记追踪等功能，帮助用户缓解焦虑并追踪心理状态。

本项目为**纯前端工程**，后端接口由课程方统一部署（`http://159.75.169.224:1235`），前端通过 Vite 代理转发请求。测试范围为前端功能、前后端接口联调的黑盒测试。

### 1.2 目标用户

| 用户类型 | userType | 说明 |
|----------|----------|------|
| 普通用户 | 1 | 使用前台功能：AI 咨询、情绪日记、知识文章浏览 |
| 管理员 | 2 | 使用后台功能：数据分析、文章管理、咨询/情绪日志查看 |

### 1.3 产品定位

面向心理健康场景的业务产品，核心实现"AI 心理咨询 + 情绪追踪 + 心理健康知识"三大业务能力，配套后台数据可视化与管理端，与通用后台框架（如若依）形成差异化。

### 1.4 技术栈一览

| 层级 | 技术选型 |
|------|----------|
| 前端框架 | Vue 3.5（Composition API） |
| 路由 | Vue Router 4 |
| 状态管理 | Pinia 3 |
| UI 组件库 | Element Plus 2.13 |
| 构建工具 | Vite 8 |
| 网络请求 | Axios + `@microsoft/fetch-event-source`（SSE 流式） |
| 图表库 | ECharts 6 |
| 富文本 | WangEditor 5 |
| 样式 | SCSS，响应式适配 PC / 移动端 |

---

## 2. 系统架构概览

### 2.1 项目结构

```
mental-health-admin
├── public/                 # 静态资源
├── src/
│   ├── api/                # 接口定义（admin.js 后台 / frontend.js 前台）
│   ├── assets/             # 图片、图标资源
│   ├── components/         # 公共组件（布局、导航、富文本、Markdown渲染等）
│   ├── config/             # 全局配置（文件服务器地址）
│   ├── router/             # 路由配置（前台/后台/认证 三类路由 + 守卫）
│   ├── stores/             # Pinia 状态（admin）
│   ├── utils/request.js    # Axios 封装（拦截器、token 注入、统一错误处理）
│   └── views/              # 页面（前台 + 后台 + 认证）
├── .env.development        # 环境变量（VITE_API_URL=/api）
├── vite.config.js          # 代理配置（/api → 后端）
└── package.json
```

### 2.2 运行环境要求

| 依赖项 | 版本要求 |
|--------|----------|
| Node.js | ≥ 18（开发时） |
| npm | 随 Node 附带 |
| 后端服务 | 课程方部署，无需本地搭建 |

### 2.3 前后端数据流

```
前端页面 → axios/fetchEventSource → /api 前缀 → Vite 代理 → 后端(159.75.169.224:1235)
                                    ↑
                         请求头注入 headers['token'] = token（非标准 Authorization）
```

**响应结构约定**（重要，直接影响接口测试断言）：

```json
{ "code": "200", "msg": "操作成功", "data": { ... } }
```

| code 值 | 类型 | 含义 |
|---------|------|------|
| `"200"` | 字符串 | 成功（注意：是字符串，非数字） |
| `"-1"` | 字符串 | 登录过期 / 账号密码错误 |
| 其他 | 字符串 | 业务异常 |

**认证约定**：Token 存放于 `localStorage`，请求头字段名为 `token`（非 `Authorization`）。请求超时时间 5000ms。

---

## 3. 功能需求详述

---

### 3.1 用户认证与权限模块

**入口**：前台 `/auth/login`、`/auth/register`  
**用户类型**：userType 1 = 普通用户（前台），2 = 管理员（后台）

#### 3.1.1 登录功能

**功能描述**：用户输入"用户名或邮箱"与密码，系统校验通过后返回 Token，前端持久化后用于后续请求认证与自动登录。

**接口**：`POST /user/login`

**请求字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| username | string | 用户名或邮箱 |
| password | string | 登录密码 |

**业务规则**：
- BR-001：登录成功后将 `token`、`userInfo` 写入 localStorage，实现自动登录
- BR-002：登录失败返回 code `"-1"`，前端提示"账号或密码错误"
- BR-003：登录成功后根据 `userInfo.userType` 跳转：管理员进后台，普通用户进前台

#### 3.1.2 注册功能

**功能描述**：用户填写邮箱、手机号（可选）、密码、确认密码进行注册，默认注册为前台普通用户。

**接口**：`POST /user/add`

**请求字段**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名或邮箱 |
| email | string | 是 | 邮箱 |
| phone | string | 否 | 手机号 |
| password | string | 是 | 密码 |
| confirmPassword | string | 是 | 确认密码 |
| userType | number | 是 | 默认 1（前台用户） |

**业务规则**：
- BR-004：email、password、confirmPassword 为必填，前端做非空校验
- BR-005：密码与确认密码需一致
- BR-006：手机号为可选字段
- BR-007：注册默认 userType=1（前台用户）

#### 3.1.3 登出功能

**接口**：`POST /user/logout`  
**业务规则**：
- BR-008：登出后清除本地 Token 与用户信息，返回登录页

#### 3.1.4 路由权限隔离

**功能描述**：前端路由守卫根据登录态与用户类型控制页面访问。

**业务规则**（见 `router/index.js` 前置守卫）：
- BR-009：未登录访问 `/back`（后台）→ 重定向到 `/auth/login`；访问前台可正常浏览
- BR-010：userType=2（管理员）→ 仅能访问 `/back/**`，访问前台重定向到 `/back/dashboard`
- BR-011：userType=1（普通用户）→ 禁止访问 `/back` 和 `/auth`，访问则重定向到前台首页 `/`
- BR-012：Token 过期（接口返回 code `"-1"`）→ 前端清除登录信息，需重新登录

---

### 3.2 AI 心理咨询模块（核心）

**入口**：前台 `/consultation`  
**技术特点**：SSE 流式对话 + 情绪分析 + 会话管理 + 风险预警

#### 3.2.1 实时流式对话

**功能描述**：用户输入内容后，系统通过 SSE（Server-Sent Events）实时返回 AI 回复，前端以"打字机"效果逐字渲染。

**接口**：`POST /psychological-chat/stream`（SSE，`Accept: text/event-stream`）

**业务规则**：
- BR-013：流式响应要求响应 `Content-Type` 为 `text/event-stream`，否则判定接口异常
- BR-014：回复内容分片到达，前端逐段拼接渲染
- BR-015：请求超时时间 5000ms，超时需有友好提示

#### 3.2.2 情绪分析（情绪花园）

**功能描述**：基于对话内容实时分析用户情绪，以"情绪花园"可视化展示当前情绪状态。

**接口**：`GET /psychological-chat/session/{sessionId}/emotion`

**展示字段**：

| 字段 | 说明 |
|------|------|
| primaryEmotion | 主要情绪 |
| emotionScore | 情绪评分 |
| isNegative | 是否负面情绪（true 显示"需要关注"，false 显示"很不错"） |

**业务规则**：
- BR-016：根据情绪评分展示不同强度等级（情绪花园点亮）
- BR-017：`isNegative` 决定状态文案与配色

#### 3.2.3 会话管理

**功能描述**：支持新建、切换、删除历史会话。

**接口**：
- `POST /psychological-chat/session/start`（新建会话）
- `GET /psychological-chat/sessions`（会话列表）
- `DELETE /psychological-chat/sessions/{sessionId}`（删除会话）
- `GET /psychological-chat/sessions/{sessionId}/messages`（会话消息详情）

**业务规则**：
- BR-018：删除会话后列表实时刷新，被删会话不可再进入

#### 3.2.4 风险预警

**功能描述**：当检测到用户出现极端情绪时，自动展示心理援助提示。

**业务规则**：
- BR-019：极端情绪（如自伤、轻生倾向等）触发风险提示条
- BR-020：风险提示需显眼且不可轻易关闭

---

### 3.3 情绪日记模块

**入口**：前台 `/emotion-diary`  
**接口**：`POST /emotion-diary`（新增）、`GET /emotion-diary/admin/page`（后台分页）、`DELETE /emotion-diary/admin/{id}`（后台删除）

#### 3.3.1 情绪评分

**功能描述**：用户对当天整体情绪状态打分（1–10 分）。

**业务规则**：
- BR-021：评分为 1–10 分（组件 `el-rate max=10`）
- BR-022：评分对应 10 档文本：绝望崩溃(1)、消沉抑郁(2)、焦虑烦躁(3)、低落不悦(4)、平静淡然(5)、轻松惬意(6)、愉悦舒心(7)、欢欣满足(8)、兴奋欣喜(9)、极致幸福(10)

#### 3.3.2 主要情绪标签

**功能描述**：从 8 种情绪中选择一个主要情绪。

**业务规则**：
- BR-023：8 种情绪标签为：开心、平静、焦虑、悲伤、兴奋、疲惫、惊讶、困惑
- BR-024：单选，点击选中高亮

#### 3.3.3 其他记录项

| 字段 | 类型 | 说明 |
|------|------|------|
| emotionTriggers | text | 情绪触发因素（textarea，3 行） |
| diaryContent | text | 日记内容 |
| sleepQuality | number | 睡眠质量：1很差 / 2较差 / 3一般 / 4良好 / 5优秀 |
| stressLevel | number | 压力水平：1很低 / 2较低 / 3中等 / 4较高 / 5很高 |
| diaryDate | date | 记录日期，默认当天 |

**业务规则**：
- BR-025：diaryDate 默认填充当天日期
- BR-026：提交成功后重置表单

---

### 3.4 知识文章模块

#### 3.4.1 前台浏览（普通用户）

**入口**：前台 `/knowledge`、`/knowledge/article/:id`

**功能描述**：按分类展示文章列表，支持 Markdown 渲染，点击进入详情。

**接口**：
- `GET /knowledge/article/page`（文章分页列表，前台/后台共用）
- `GET /knowledge/article/{id}`（文章详情）
- `GET /knowledge/category/tree`（分类树）

**业务规则**：
- BR-027：文章支持分类筛选、分页、搜索
- BR-028：文章内容支持 Markdown 渲染（组件 MarkdownRenderer）

#### 3.4.2 后台管理（管理员）

**入口**：后台 `/back/knowledge`

**功能描述**：对知识文章进行增删改查，支持 WangEditor 富文本编辑与封面图上传。

**接口**：
- `POST /knowledge/article`（新增）
- `PUT /knowledge/article/{id}`（修改）
- `PUT /knowledge/article/{id}/status`（上/下架）
- `DELETE /knowledge/article/{id}`（删除）
- `POST /file/upload`（封面图上传）

**文章关键字段**：

| 字段 | 说明 |
|------|------|
| title | 文章标题 |
| category | 所属分类 |
| cover | 封面图 |
| content | 富文本正文 |
| status | 状态（上架/下架） |

**业务规则**：
- BR-029：文章正文使用 WangEditor 富文本编辑器
- BR-030：封面图上传接口 `file/upload`，请求为 multipart/form-data，携带 businessType=ARTICLE、businessId、businessField=cover
- BR-031：状态切换（上/下架）走独立接口 `PUT .../status`
- BR-032：删除文章需二次确认

---

### 3.5 后台仪表盘模块（数据分析）

**入口**：后台 `/back/dashboard`  
**接口**：`GET /data-analytics/overview`

**功能描述**：以 ECharts 图表展示平台核心数据指标。

**展示内容**：

| 图表 | 说明 |
|------|------|
| 用户活跃度 | 用户活跃趋势 |
| 情绪分布 | 各情绪类型占比 |
| 咨询趋势 | 咨询量变化趋势 |

**业务规则**：
- BR-033：图表数据来源于 `data-analytics/overview` 接口
- BR-034：图表渲染数值应与接口返回数据一致（测试重点）

---

### 3.6 咨询记录管理（管理员）

**入口**：后台 `/back/consultations`  
**接口**：`GET /psychological-chat/sessions`、`GET /psychological-chat/sessions/{sessionId}/messages`

**功能描述**：管理员查看所有用户的咨询会话记录，可查看单个会话的消息详情。

---

### 3.7 情绪日志管理（管理员）

**入口**：后台 `/back/emotional`  
**接口**：`GET /emotion-diary/admin/page`、`DELETE /emotion-diary/admin/{id}`

**功能描述**：管理员分页查看所有用户的情绪日记，可删除。

**业务规则**：
- BR-035：删除情绪日志需二次确认

---

## 4. 非功能需求

### 4.1 性能

- NFR-001：接口请求超时时间 5000ms，超时需有友好提示
- NFR-002：SSE 流式对话需保证打字机渲染流畅，无明显卡顿
- NFR-003：文章列表分页加载，单页数据量合理

### 4.2 兼容性

- NFR-004：响应式适配 PC 与移动端（SCSS 响应式布局）
- NFR-005：主流浏览器 Chrome、Edge 核心流程可正常使用

### 4.3 安全性

- NFR-006：密码加密存储（后端处理），前端不明文回显
- NFR-007：Token 持久化登录，未登录不可访问后台
- NFR-008：普通用户不可越权访问后台（路由守卫拦截）
- NFR-009：富文本内容与文章展示需防范 XSS 注入

### 4.4 易用性

- NFR-010：操作需有明确反馈（成功/失败提示）
- NFR-011：删除等危险操作需二次确认
- NFR-012：登录过期需引导用户重新登录

---

## 5. 接口总览

### 5.1 用户认证

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | /user/login | 否 | 登录 |
| POST | /user/add | 否 | 注册 |
| POST | /user/logout | 是 | 登出 |

### 5.2 AI 心理咨询

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | /psychological-chat/session/start | 是 | 新建会话 |
| GET | /psychological-chat/sessions | 是 | 会话列表（前台/后台共用） |
| DELETE | /psychological-chat/sessions/{sessionId} | 是 | 删除会话 |
| GET | /psychological-chat/sessions/{sessionId}/messages | 是 | 会话消息详情 |
| GET | /psychological-chat/session/{sessionId}/emotion | 是 | 情绪分析 |
| POST | /psychological-chat/stream | 是 | **SSE 流式对话** |

### 5.3 情绪日记

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | /emotion-diary | 是 | 新增情绪日记 |
| GET | /emotion-diary/admin/page | 是 | 后台分页查询 |
| DELETE | /emotion-diary/admin/{id} | 是 | 后台删除 |

### 5.4 知识文章

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | /knowledge/category/tree | 否 | 分类树 |
| GET | /knowledge/article/page | 否 | 文章分页列表 |
| GET | /knowledge/article/{id} | 否 | 文章详情 |
| POST | /knowledge/article | 是 | 新增文章 |
| PUT | /knowledge/article/{id} | 是 | 修改文章 |
| PUT | /knowledge/article/{id}/status | 是 | 上/下架 |
| DELETE | /knowledge/article/{id} | 是 | 删除文章 |

### 5.5 其他

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | /file/upload | 是 | 文件上传（封面图，multipart） |
| GET | /data-analytics/overview | 是 | 数据总览 |

---

## 6. 名词解释

| 术语 | 说明 |
|------|------|
| SSE | Server-Sent Events，服务端主动向客户端推送数据的单向流式通信技术 |
| userType | 用户类型标识：1=普通用户（前台），2=管理员（后台） |
| 情绪花园 | 情绪分析结果的可视化展示区域 |
| JWT Token | 用户登录后获取的身份凭证，请求时放入 `token` 请求头 |
| 富文本 | 支持格式化排版、图片等内容的多格式文本编辑器（WangEditor） |
| 路由守卫 | 前端在路由跳转前执行的登录态与权限校验逻辑 |

---

> **附录**：本文档基于 mental-health-admin V1.0 现有功能整理。本项目为纯前端工程，后端接口由课程方部署维护，测试以黑盒功能测试 + 接口测试为主。如需后续扩展功能，请在修订记录中追加。
