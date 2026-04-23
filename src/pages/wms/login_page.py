"""WMS 登录页面对象，封装用户名/密码填写和登录提交操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSLoginPage(BasePage):
    """WMS 登录页，包含打开登录页和提交登录凭据两个核心操作。"""

    def open_login(self, base_url: str, login_path: str) -> None:
        """导航到 WMS 登录页并等待用户名输入框可见。"""
        self.open(f"{base_url.rstrip('/')}{login_path}")
        self.page.locator("#username").wait_for(state="visible", timeout=30000)

    def login(self, username: str, password: str) -> None:
        """填写用户名、密码并点击登录按钮。"""
        self.fill("wms_username", username, [LocatorCandidate("username-id", "#username"), LocatorCandidate("username-name", "input[name='username']")], "WMS 登录用户名输入框")
        self.fill("wms_password", password, [LocatorCandidate("password-id", "#password"), LocatorCandidate("password-name", "input[type='password']")], "WMS 登录密码输入框")
        self.click("wms_login", [LocatorCandidate("login-button", "button[type='submit']"), LocatorCandidate("login-text", "text=登录")], "WMS 登录按钮")
