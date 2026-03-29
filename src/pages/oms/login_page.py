"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class OMSLoginPage(BasePage):
    def open_login(self, base_url: str, login_path: str) -> None:
        """中文说明：在 OMSLoginPage 中打开与 open_login 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}{login_path}")

    def login(self, username: str, password: str) -> None:
        """中文说明：在 OMSLoginPage 中执行登录与 login 相关的操作。"""
        self.fill(
            "oms_username",
            username,
            [
                LocatorCandidate("username-id", "#username"),
                LocatorCandidate("username-name", "input[name='username']"),
            ],
            "OMS 登录用户名输入框",
        )
        self.fill(
            "oms_password",
            password,
            [
                LocatorCandidate("password-id", "#password"),
                LocatorCandidate("password-name", "input[type='password']"),
            ],
            "OMS 登录密码输入框",
        )
        self.click(
            "oms_login",
            [
                LocatorCandidate("login-button", "button[type='submit']"),
                LocatorCandidate("login-text", "text=登录"),
            ],
            "OMS 登录按钮",
        )