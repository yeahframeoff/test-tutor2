from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage.
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('#1: Fry potatoes', [row.text for row in rows])

        # There is still a textbox inviting her to add another item.
        # She enters "Bake some bread"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Bake some bread')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('#1: Fry potatoes', [row.text for row in rows])
        self.assertIn('#2: Bake some bread', [row.text for row in rows])

        self.fail('Finish the test!')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.
