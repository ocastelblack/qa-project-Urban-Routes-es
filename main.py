import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # NUEVOS LOCALIZADORES
    comfort_tariff = (By.XPATH, "//div[text()='Comfort']")
    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    phone_code_input = (By.XPATH, "//input[@id='code']")
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")

    add_card_button = (By.XPATH, "//div[text()='Agregar tarjeta']")
    add_card_option = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//input[@id='code' and @placeholder='12']")
    add_button = (By.XPATH, "//div[contains(@class,'section active')]//button[text()='Agregar']")
    close_payment_modal = (By.CSS_SELECTOR, "button.close-button.section-close")

    message_input = (By.ID, "comment")

    blanket_checkbox = (By.XPATH, "//div[text()='Manta y pañuelos']/following::span[@class='slider round'][1]")
    icecream_button = (By.CLASS_NAME, "counter-plus")

    order_taxi_button = (By.XPATH, "//button[text()='Pedir taxi']")
    request_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    payment_method_button = (By.CLASS_NAME, "pp-button")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def request_taxi(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.request_taxi_button)
        ).click()

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff)
        ).click()


    def set_phone(self, phone):
        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.phone_next_button).click()


    def confirm_phone_code(self):

        # esperar campo del código
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_code_input)
        )

        code = retrieve_phone_code(self.driver)

        self.driver.find_element(*self.phone_code_input).send_keys(code)

        self.driver.find_element(*self.confirm_code_button).click()

    def open_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        ).click()


    def add_card(self, number, code):

        # click "Agregar tarjeta" en el primer modal
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_option)
        ).click()

        # esperar que aparezca el modal con el formulario
        number_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_number_input)
        )
        number_field.send_keys(number)

        # escribir CVV
        code_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.card_code_input)
        )
        code_field.send_keys(code)

        # quitar foco para habilitar botón
        code_field.send_keys(Keys.TAB)

        add_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.add_button)
        )

        self.driver.execute_script("arguments[0].click();", add_btn)

        # cerrar modal sin esperar
        self.driver.execute_script(
            "document.querySelector('button.close-button.section-close').click()"
        )

    def write_message(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)


    def add_blanket(self):
        self.driver.find_element(*self.blanket_checkbox).click()


    def add_icecream(self):
        self.driver.find_element(*self.icecream_button).click()
        self.driver.find_element(*self.icecream_button).click()


    def order_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

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

        routes_page.write_message(data.message_for_driver)

        routes_page.add_blanket()

        routes_page.add_icecream()

        routes_page.order_taxi()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
