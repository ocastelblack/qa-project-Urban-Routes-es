from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from helpers import retrieve_phone_code


class UrbanRoutesPage:

    from_field = (By.ID, "from")
    to_field = (By.ID, "to")

    comfort_tariff = (By.XPATH, "//div[text()='Comfort']")

    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    phone_code_input = (By.ID, "code")
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")

    payment_method_button = (By.CLASS_NAME, "pp-button")

    add_card_option = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    add_button = (By.XPATH, "//div[contains(@class,'section active')]//button[text()='Agregar']")
    close_payment_modal = (By.CSS_SELECTOR, "button.close-button.section-close")

    message_input = (By.ID, "comment")

    blanket_checkbox = (
        By.XPATH,
        "//div[text()='Manta y pañuelos']/following::span[contains(@class,'slider')]"
    )

    icecream_button = (
        By.XPATH,
        "//div[text()='Helado']/..//div[@class='counter-plus']"
    )

    order_taxi_button = (By.XPATH, "//button[text()='Pedir taxi']")
    request_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def request_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        ).click()

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property("value")

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_tariff)
        ).click()

    def set_phone(self, phone):
        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.phone_next_button).click()

    def confirm_phone_code(self):

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.phone_code_input)
        )

        code = retrieve_phone_code(self.driver)

        self.driver.find_element(*self.phone_code_input).send_keys(code)

        self.driver.find_element(*self.confirm_code_button).click()

    def open_payment_method(self):

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_button)
        ).click()

    def add_card(self, number, code):

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_option)
        ).click()

        number_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_number_input)
        )
        number_field.send_keys(number)

        code_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_code_input)
        )
        code_field.send_keys(code)

        code_field.send_keys(Keys.TAB)

        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_button)
        )

        add_btn.click()

    def close_payment(self):

        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'modal')]//button[contains(@class,'close-button')]")
            )
        )

        close_btn.click()

    def write_message(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def add_blanket(self):
        self.driver.find_element(*self.blanket_checkbox).click()

    def add_icecream(self):
        self.driver.find_element(*self.icecream_button).click()
        self.driver.find_element(*self.icecream_button).click()

    def order_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()