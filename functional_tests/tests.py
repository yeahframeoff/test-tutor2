from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys

from unittest import skip


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @skip
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Fry potatoes" into a textbox
        inputbox.send_keys('Fry potatoes')

        # When she hits Enter, the page updates, and now the page
        # lists "#1: Fry potatoes" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('#1: Fry potatoes')

        # There is still a textbox inviting her to add another item.
        # She enters "Bake some bread"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Bake some bread')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('#1: Fry potatoes')
        self.check_for_row_in_list_table('#2: Bake some bread')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visits home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Fry potatoes', page_text)
        self.assertNotIn('Bake some bread', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kill 300 spartans')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URl.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Fry potatoes', page_text)
        self.assertNotIn('Bake some bread', page_text)
        self.assertIn('Kill 300 spartans', page_text)

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=6
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=6
        )

