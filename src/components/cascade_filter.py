from __future__ import annotations

from components.base_component import BaseComponent


class CascadeFilterComponent(BaseComponent):
    def apply_filters(self, filters: list[tuple[str, str]]) -> None:
        for trigger_selector, option_text in filters:
            self.page.locator(trigger_selector).click()
            self.page.get_by_text(option_text, exact=True).click()