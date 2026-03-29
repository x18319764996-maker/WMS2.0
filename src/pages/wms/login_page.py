"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSLoginPage(BasePage):
    def open_login(self, base_url: str, login_path: str) -> None:
        """中文说明：在 WMSLoginPage 中打开与 open_login 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}{login_path}")
        self.page.locator("#username").wait_for(state="visible", timeout=30000)

    def login(self, username: str, password: str) -> None:
        """中文说明：在 WMSLoginPage 中执行登录与 login 相关的操作。"""
        self.fill("wms_username", username, [LocatorCandidate("username-id", "#username"), LocatorCandidate("username-name", "input[name='username']")], "WMS 登录用户名输入框")
        self.fill("wms_password", password, [LocatorCandidate("password-id", "#password"), LocatorCandidate("password-name", "input[type='password']")], "WMS 登录密码输入框")
        self.click("wms_login", [LocatorCandidate("login-button", "button[type='submit']"), LocatorCandidate("login-text", "text=登录")], "WMS 登录按钮")
