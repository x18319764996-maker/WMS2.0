from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSLoginPage(BasePage):
    def open_login(self, base_url: str, login_path: str) -> None:
        self.open(f"{base_url.rstrip('/')}{login_path}")

    def login(self, username: str, password: str) -> None:
        self.fill("wms_username", username, [LocatorCandidate("username-id", "#username"), LocatorCandidate("username-name", "input[name='username']")], "WMS 登录用户名输入框")
        self.fill("wms_password", password, [LocatorCandidate("password-id", "#password"), LocatorCandidate("password-name", "input[type='password']")], "WMS 登录密码输入框")
        self.click("wms_login", [LocatorCandidate("login-button", "button[type='submit']"), LocatorCandidate("login-text", "text=登录")], "WMS 登录按钮")