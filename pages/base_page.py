# Здесь будут общие методы для всех страниц
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()

    def wait_for_url_contains(self, text: str):
        self.page.wait_for_url(f"**/*{text}*")

    def is_text_visible(self, text: str, timeout: int = 5000) -> bool:
        try:
            expect(self.page.get_by_text(text, exact=True).first).to_be_visible(
                timeout=timeout
            )
            return True
        except Exception:
            return False
