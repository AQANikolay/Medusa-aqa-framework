from pages.base_page import BasePage


# Здесь страница управления товарами в админке
class ProductsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.products_menu_link = (
            page.get_by_role("navigation").get_by_role("link", name="Products").first
        )
        self.create_button = page.get_by_role("link", name="Create")
        self.search_input = page.get_by_placeholder("Search").first
        self.next_page_button = page.get_by_role("button", name="Next").first
        self.previous_button = page.get_by_role("button", name="Previous").first
        self.no_results_message = page.get_by_text("No results").first

    def open_products_list(self):  # здесь переход в раздел товаров через боковое меню
        self.products_menu_link.click()
        self.wait_for_url_contains("products")
        self.page.wait_for_timeout(1000)

    def search_for_product(
        self, product_name: str
    ):  # здесь ввод названия товара в строку поиска
        self.search_input.fill(product_name)
        self.page.wait_for_timeout(1500)

    def click_create_button(self):
        self.create_button.click()

    def open_product_details(self, product_name: str):
        self.page.get_by_text(product_name).first.click()

    def is_product_visible(self, product_name: str, timeout: int = 5000) -> bool:
        row = self.page.get_by_text(product_name).first
        try:
            row.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def go_to_next_page(self):
        self.next_page_button.click()
        self.page.wait_for_timeout(1000)

    def go_to_previous_page(self):
        self.previous_button.click()
        self.page.wait_for_timeout(1000)
