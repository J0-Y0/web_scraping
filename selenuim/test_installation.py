from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://yosefemyayu.pythonanywhere.com/")
print("Title of the page:", driver.title)

# other actions

element = driver.find_element("name", "description")
element_content = element.get_attribute("content")
print("element_content:", element_content)

# Quit the driver
# driver.quit()
