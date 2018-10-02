from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

user = "qacandidate@splashthat.com"
pwd = "testingislife"


class SplashFramework:

    def __init__(self):
        self.browser = None
        self.driver_init()
        self.start_page = "https://www.splashthat.com"

    def driver_init(self):
        print("Init Driver.")
        try:
            self.browser = webdriver.Chrome()
        except WebDriverException as exc:
            raise print("Cant find chrome driver.")

        """Set some timeouts, adjust if necessary"""
        self.browser.implicitly_wait(15)
        self.browser.set_page_load_timeout(5)
        return self.browser

    def driver_quit(self):
        self.browser.quit()
        print("Driver Quit.")

    def login_test(self, user, pwd, fail = False):

        """This has been verified on Edge and Firefox as well"""
        browser = self.browser
        browser.get(self.start_page)

        """If failure flag is up add some string to username so login fails"""
        if fail:
            user += "123!"

        cur_page = "splashthat.com"

        if browser.current_url.find(cur_page) == -1:
            print("Error :: Couldn't get to {}.".format(cur_page))
            return False

        elem_login = WebDriverWait(browser, 5).\
            until(EC.visibility_of_element_located((By.XPATH,'//a[text()="Log In"]'))).click()

        print("Info :: We are at login page.")
        elem_email = WebDriverWait(browser, 3).\
            until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name*='email'"))).send_keys(user)
        elem_pwd = browser.find_element_by_css_selector("input[name*='password'").send_keys(pwd)
        elem_submit = browser.find_element_by_css_selector("input[type='submit'").click()

        if fail:
            """Check for login failure popup message"""
            elem_error = WebDriverWait(browser, 3).\
                until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#flashMessage")))

            """Go back to Login page"""
            elem_email = WebDriverWait(browser, 3). \
                until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name*='email'"))).send_keys(user)

            print("Info :: Error message popped successfully and we are back to login page.")
            return True

        elem_events = WebDriverWait(browser, 3).\
            until(EC.visibility_of_element_located((By.XPATH, '//span[text() = "Events"]')))
        print("Info :: We are logged in.")

        print("Info :: Logging out...")
        elem_user = browser.find_element_by_css_selector('div.user-image').click()
        elem_logout = browser.find_element_by_xpath("//a[@href='/users/logout']").click()

        cur_page = "splashthat.com/login"
        if browser.current_url.find(cur_page) != -1:
            print("Info :: Successfully logged out")

        print("Info :: Test complete...")
        return True


class TestCases:

    st = SplashFramework()

    def test_login(self, user, pwd):
        return self.st.login_test(user, pwd)

    def test_failed_login(self, user, pwd):
        return self.st.login_test(user, pwd, True)


"""Main body"""
if __name__ == "__main__":
    tc = TestCases()
    if tc.test_login(user, pwd):
        print("Info :: Login Test Complete")
    else:
        print("Error :: Login Test Failed.")

    if tc.test_failed_login(user, pwd):
        print("Info :: Failed login Test Complete")
    else:
        print("Error :: Login Failure Test Failed.")

    tc.st.driver_quit()
