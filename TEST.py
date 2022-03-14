import selenium
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
path_to_binary = Path(
    "C:/Users/Pedram/Documents/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(path_to_binary.as_posix())
driver.get('https://mix.wvu.edu')
id_box = driver.find_element_by_name('username')
pass_box = driver.find_element_by_name('password')
# Send login information
id_box.send_keys('')
pass_box.send_keys('')
# Click login
login_button = driver.find_element_by_name('submit')
login_button.click()
push = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="auth_methods"]/fieldset[1]/div[1]/button')))
push.click()
# <button tabindex="2" type="submit" class="positive auth-button"><!-- -->Send Me a Push </button>
# Send Me a Push 
# run_query = driver.find_element_by_name('content_form:btnRunQuery')
# clear_query = driver.find_element_by_name('content_form:btnClearQuery')
# clear_query.click()

# icsd_code_form = driver.find_element_by_id("content_form:uiCodeCollection:input:componentInputPanel")
# icsd_code_form.send_keys("616165")
# run_query.click()
