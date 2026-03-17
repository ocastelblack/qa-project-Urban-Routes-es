import data
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages import UrbanRoutesPage


@pytest.mark.order(1)
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver.maximize_window()

    @pytest.mark.order(1)
    def test_set_route(self):

        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)

        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    @pytest.mark.order(2)
    def test_select_comfort_fare(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.request_taxi()
        routes_page.select_comfort()

        comfort = self.driver.find_element(By.XPATH, "//div[text()='Comfort']")
        assert comfort.is_displayed()

    @pytest.mark.order(3)
    def test_fill_phone(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_phone(data.phone_number)
        routes_page.confirm_phone_code()

        phone_button = self.driver.find_element(By.CLASS_NAME, "np-button")
        assert data.phone_number in phone_button.text

    @pytest.mark.order(4)
    def test_add_card(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.open_payment_method()
        routes_page.add_card(data.card_number, data.card_code)
        routes_page.close_payment()

        payment_button = self.driver.find_element(By.CLASS_NAME, "pp-button")
        assert payment_button.is_displayed()

    @pytest.mark.order(5)
    def test_comment_for_driver(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.write_message(data.message_for_driver)

        message = self.driver.find_element(By.ID, "comment")
        assert message.get_attribute("value") == data.message_for_driver

    @pytest.mark.order(6)
    def test_extra_requirements(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.add_blanket()
        routes_page.add_icecream()

        blanket_input = self.driver.find_element(
            By.XPATH,
            "//div[text()='Manta y pañuelos']/following::input[@type='checkbox'][1]"
        )

        assert blanket_input.is_selected()

        icecream_counter = self.driver.find_element(
            By.XPATH,
            "//div[text()='Helado']/..//div[@class='counter-value']"
        )

        assert icecream_counter.text == "2"

    @pytest.mark.order(7)
    def test_order_taxi(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.order_taxi()

        routes_page.wait_for_driver()

        assert routes_page.is_driver_modal_displayed()

    @classmethod
    def teardown_class(cls):
        import time
        time.sleep(5)
        cls.driver.quit()