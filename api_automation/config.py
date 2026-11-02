# -*- coding: utf-8 -*-
"""接口自动化配置

账号来源优先级：
1. 环境变量（CI 中由 GitHub Secrets 注入）
2. config_local.py（本地开发用，已 gitignore，不入库）
3. 占位符（默认，未配置时登录会失败并给出提示）
"""
import os

# 后端接口地址（带 /api 前缀，前端通过 Vite 代理转发到这里）
BASE_URL = os.getenv("BASE_URL", "http://159.75.169.224:1235/api")

# 测试账号：CI 用 Secrets，本地用 config_local.py
try:
    # 本地开发：config_local.py 不入库
    from config_local import TEST_USERNAME, TEST_PASSWORD  # type: ignore
except ImportError:
    TEST_USERNAME = os.getenv("TEST_USERNAME", "你的测试账号")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "你的测试密码")

# 成功业务码（注意：是字符串，不是数字）
CODE_SUCCESS = "200"
