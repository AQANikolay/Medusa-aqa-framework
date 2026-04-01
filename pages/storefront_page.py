from pages.base_page import BasePage
from config import Config
from playwright.sync_api import expect


class StorefrontPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.search_icon = page.get_by_role("button", name="Search")
        self.search_input = page.get_by_placeholder("Search products...")
        self.cart_icon = page.get_by_test_id("nav-cart-link").first
        self.add_to_cart_button = page.get_by_test_id("add-product-button")
        self.checkout_button = page.get_by_test_id("checkout-button")
        self.menu_button = page.get_by_role("button", name="Menu").first
        self.store_link = page.locator('a:has-text("Store")').first
        self.country_selector = page.locator('button:has-text("Shipping to:")').first
        self.current_country = page.get_by_text("Denmark").first

    def open_storefront(self):
        self.open(Config.STOREFRONT_URL)
        expect(self.current_country)

    def change_country_to_germany(self):
        print("\n[UI-DEBUG] Открываем Бургер-меню...")
        self.menu_button.click(force=True)
        self.page.wait_for_timeout(1500)

        expect(self.current_country).to_be_visible(timeout=5000)

        print("[UI-DEBUG] Наводим мышку на текущую страну (Denmark)...")
        self.current_country.hover()
        self.page.wait_for_timeout(1000)

        print("[UI-DEBUG] Кликаем на Germany...")
        self.page.get_by_text("Germany", exact=True).first.click(force=True)

        print("[UI-DEBUG] Ждем перезагрузки витрины (смена региона)...")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def search_product(self, product_name: str):
        if self.search_icon.is_visible():
            self.search_icon.click()
        self.search_input.fill(product_name)
        self.search_input.press("Enter")
        self.page.wait_for_timeout(1000)

    def open_product_card(self, product_name: str):
        product_card = self.page.get_by_role("link", name=product_name).first
        product_card.click()
        expect(self.add_to_cart_button).to_be_visible(timeout=Config.UI_TIMEOUT)

    def add_current_product_to_cart(self):
        self.add_to_cart_button.click(force=True)
        self.page.wait_for_timeout(1000)

    def go_to_checkout(self):
        self.cart_icon.click(force=True)
        self.checkout_button.click(force=True)
        self.wait_for_url_contains("checkout")

    def go_to_store_catalog(self):
        self.menu_button.click(force=True)
        self.page.wait_for_timeout(1000)
        self.store_link.click(force=True)
        self.wait_for_url_contains("store")
        self.page.wait_for_load_state("networkidle")

    def open_product_card_from_catalog(self, product_name: str):
        product_card = self.page.get_by_text(product_name).first
        product_card.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        product_card.click(force=True)
        expect(self.add_to_cart_button).to_be_visible(timeout=10000)
