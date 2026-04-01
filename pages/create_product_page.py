from pages.base_page import BasePage
import re


class CreateProductPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.title_input = page.locator("input[name='title']").first

        self.continue_button = page.locator('button:has-text("Continue")').last
        self.publish_button = page.locator('button:has-text("Publish")').last

        self.success_toast = page.get_by_text("Product created")

    def fill_basic_info(self, title: str):
        self.page.wait_for_timeout(1500)
        self.title_input.wait_for(state="visible", timeout=10000)
        self.title_input.click(force=True, timeout=5000)
        self.title_input.fill(title, force=True)

    def is_creation_successful(self) -> bool:
        try:
            success_toast = self.page.get_by_text(
                re.compile(r"was successfully created", re.IGNORECASE)
            )
            return True
        except Exception:
            return False

    def create_simple_product(self, title: str):
        self.title_input.click(force=True)
        self.fill_basic_info(title)
        self.page.wait_for_timeout(500)
        print("[UI-DEBUG] Смотри в браузер!")
        # self.page.pause()

        self.continue_button.click(force=True)
        self.page.wait_for_timeout(1000)

        self.continue_button.click(force=True)
        self.page.wait_for_timeout(1000)

        self.publish_button.click(force=True)

    def cancel_creation(self):
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(1000)
