import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver.maximize_window()

    def test_set_route(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_fare(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        comfort = self.driver.find_element(By.XPATH, "//div[text()='Comfort']")

        assert comfort.is_displayed()

    def test_fill_phone(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        routes_page.set_phone(data.phone_number)

        routes_page.confirm_phone_code()

        phone_button = self.driver.find_element(By.CLASS_NAME, "np-button")

        assert data.phone_number in phone_button.text

    def test_add_card(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        routes_page.set_phone(data.phone_number)

        routes_page.confirm_phone_code()

        routes_page.open_payment_method()

        routes_page.add_card(data.card_number, data.card_code)

        routes_page.close_payment()

        payment_button = self.driver.find_element(By.CLASS_NAME, "pp-button")

        assert payment_button.is_displayed()

    def test_comment_for_driver(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        routes_page.write_message(data.message_for_driver)

        message = self.driver.find_element(By.ID, "comment")

        assert message.get_attribute("value") == data.message_for_driver

    def test_extra_requirements(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        routes_page.add_blanket()

        blanket_input = self.driver.find_element(
            By.XPATH,
            "//div[text()='Manta y pañuelos']/following::input[@type='checkbox'][1]"
        )

        assert blanket_input.is_selected()

    def test_order_taxi(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        routes_page.request_taxi()

        routes_page.select_comfort()

        routes_page.set_phone(data.phone_number)

        routes_page.confirm_phone_code()

        routes_page.open_payment_method()

        routes_page.add_card(data.card_number, data.card_code)

        routes_page.close_payment()

        routes_page.write_message(data.message_for_driver)

        routes_page.add_blanket()

        routes_page.add_icecream()

        routes_page.order_taxi()

        # esperar que termine la búsqueda del conductor
        driver_info = (By.CLASS_NAME, "order-header-content")

        WebDriverWait(self.driver, 60).until_not(
            EC.text_to_be_present_in_element(driver_info, "Buscar automóvil")
        )

        modal = self.driver.find_element(*driver_info)

        assert modal.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()