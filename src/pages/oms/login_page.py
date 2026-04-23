"""OMS 登录页面对象，封装用户名/密码填写和登录提交操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class OMSLoginPage(BasePage):
    """OMS 登录页，包含打开登录页和提交登录凭据两个核心操作。"""

    def open_login(self, base_url: str, login_path: str) -> None:
        """导航到 OMS 登录页并等待页面就绪。"""
        self.open(f"{base_url.rstrip('/')}{login_path}")

    def login(self, username: str, password: str) -> None:
        """填写用户名、密码并点击登录按钮。"""
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