from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class ReactSelect(object):
    select_menu_locator = "Select-menu"

    def __init__(self, web_element):
        if 'Select' not in web_element.get_attribute('class'):
            raise Exception('This element is Not a ReactSelect')

        self.driver = web_element.parent
        self.select_menu = web_element
        self.wait = WebDriverWait(self.driver, 5)

        self.is_multiple = 'Select--multi' in web_element.get_attribute('class')

    @property
    def menu(self):
        self.open_menu()
        return self.select_menu.find_element_by_class_name(self.select_menu_locator)

    @property
    def selected_options_on_line(self):
        return self.select_menu.find_elements_by_class_name('Select-value')

    @property
    def options(self):
        options_locator = "//div[@role='option']"
        # wait for react menu to load
        WebDriverWait(self.driver, 10).until(lambda _: len(self.menu.find_elements_by_xpath(options_locator)) > 0)

        return self.menu.find_elements_by_xpath(options_locator)

    @property
    def all_selected_options(self):
        """Returns a list of all selected options belonging to this select tag"""
        ret = []
        for opt in self.options:
            if opt.is_selected():
                ret.append(opt)
        return ret

    @property
    def first_selected_option(self):
        """The first selected option in this select tag (or the currently selected option in a
        normal select)"""
        for opt in self.options:
            if opt.is_selected():
                return opt
        raise NoSuchElementException("No options are selected")

    # todo : cut index from id
    def select_by_index(self, index):
        match = str(index)
        for opt in self.options:
            if self._get_option_index(opt) == match:
                self._setSelected(opt)
                self._close_menu()
                return

        raise NoSuchElementException("Could not locate element with index %d" % index)

    def deselect_all(self):

        if not self.is_multiple and len(self.select_menu.find_elements_by_class_name('Select-clear')) == 0:
            raise Exception("There is no deselect all button")

        self.select_menu.find_element_by_class_name('Select-clear').click()

    # todo:implement selection by partial text
    def select_by_visible_text(self, text):
        wanted_elements_indexes = [self._get_option_index(i) for i in self.options if
                                   i.text.strip() == text.strip()]

        if len(wanted_elements_indexes) == 0:
            raise NoSuchElementException("Could not locate element with text {0}".format(text))

        for element_index in wanted_elements_indexes:
            self.select_by_index(element_index)

            if not self.is_multiple:
                return

    def deselect_by_index(self, index):
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect options of a multi-select")

        index = int(index)
        if len(self.selected_options_on_line) < index:
            raise NoSuchElementException("Could not locate element with index %d %index")

        self._unsetSelected(self.selected_options_on_line[index])

    def deselect_by_visible_text(self, text):
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect options of a multi-select")

        selected = False

        for opt in self.selected_options_on_line:
            if opt.find_element_by_class_name('Select-value-label').text.strip() == text.strip():
                self._unsetSelected(opt)
                selected = True

        if selected is False:
            raise NoSuchElementException("Could not locate element with text {0}".format(text))

    def open_menu(self):
        if self._is_menu_open():
            return

        self._click_select_arrow_button()

        self.wait.until(lambda _: self.driver.find_element_by_class_name(self.select_menu_locator))

    def _get_option_index(self, option):
        return option.get_attribute("id").split('option-')[1]

    def _setSelected(self, option):
        if not option.is_selected():
            option.click()

    def _is_menu_open(self):
        return 'is-open' in self.select_menu.get_attribute('class')

    def _close_menu(self):
        if self._is_menu_open():
            self._click_select_arrow_button()

    def _unsetSelected(self, selected_option):
        selected_option.find_element_by_class_name('Select-value-icon').click()

    def _click_select_arrow_button(self):
        ActionChains(self.driver).move_to_element(
            self.select_menu.find_element_by_class_name('Select-arrow')).click().perform()
