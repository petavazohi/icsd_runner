import json
import os
import shutil
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://icsd.fiz-karlsruhe.de/index.xhtml')


def clear_query():
    time.sleep(2)
    driver.find_element(By.NAME, "content_form:btnClearQuery").click()


def run_query():
    time.sleep(2)
    button = driver.find_element(By.XPATH,
                                 '//*[@id="content_form:btnRunQuery"]')
    button.click()


def login(user, password):
    time.sleep(2)
    id_box = driver.find_element(By.NAME, 'content_form:loginId')
    pass_box = driver.find_element(By.NAME, 'content_form:password')
    # Send login information
    id_box.send_keys(user)
    pass_box.send_keys(password)
    # Click login
    driver.find_element(By.NAME, 'content_form:loginButtonPersonal').click()
    driver.find_element(
        By.XPATH,
        '//*[@id="content_form:uiSelectContent"]/tbody/tr[2]/td/div').click()


def logout():
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//*[@id="header_form:logoutLink"]/span').click()


def enter_icsd(_id):
    time.sleep(2)
    icsd_code_form = driver.find_element(
        By.ID,
        "content_form:uiCodeCollection:input:componentInputPanel")
    icsd_code_form.click()
    action = webdriver.ActionChains(driver)
    action.key_down(
        Keys.CONTROL
        ).send_keys_to_element(
            icsd_code_form, "a"
            ).key_up(Keys.CONTROL).send_keys_to_element(
                icsd_code_form, Keys.DELETE
                ).send_keys_to_element(icsd_code_form, _id).perform()


def check_uncheck_theory():
    # check in theoroitical
    time.sleep(2)
    driver.find_element(
        By.XPATH,
        '//*[@id="content_form:uiSelectContent"]/tbody/tr[3]/td/div/div[2]'
        ).click()


def select_all():
    time.sleep(2)
    driver.find_element(
        By.XPATH,
        '//*[@id="display_form:listViewTable:uiSelectAllRows"]/div[2]/span'
        ).click()


def export_data(name, mode):
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        '//*[@id="display_form:btnExportData"]/span[2]').click()
    time.sleep(1)
    export_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "display_form:expName")))
    webdriver.ActionChains(driver).key_down(
        Keys.SHIFT
        ).send_keys_to_element(
            export_name, Keys.END
            ).send_keys_to_element(
                export_name, Keys.DELETE
                ).key_up(
                    Keys.SHIFT
                    ).send_keys_to_element(
                        export_name, f"{name}_{mode}"
                        ).perform()
    select = Select(driver.find_element(
        By.XPATH,
        '//*[@id="display_form:expCelltype:input_input"]'))
    select.select_by_visible_text(mode)
    export_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="display_form:j_idt284"]')))
    export_button.click()
    driver.find_element(
        By.XPATH,
        '//*[@id="display_form:expData"]/div[1]/a/span').click()


def back_to_query():
    driver.find_element(
        By.XPATH,
        '//*[@id="display_form:btnBackToQuery"]/span[2]').click()


with open("icsd_mp_id.json", 'r') as rf:
    data = json.load(rf)

errors = {}

# if you want to only download from this list
# my_list = ["mp-486",
#            "mp-8430",
#            "mp-8446",
#            "mp-11715",
#            "mp-1243",
#            "mp-2352",
#            "mp-3810",
#            "mp-504535",
#            "mp-568624"]

my_list = list(data.keys())
icsd_download_path = "G:/My Drive/_projects/PBEvsPBEsol/icsd/icsd_downloads"
chrome_download_path = 'C:/Users/Pedram/Downloads'
driver.find_element(
    By.XPATH, 
    '//*[@id="cookie-notice"]/div/table/tbody/tr[2]/td[2]/a[2]').click()
with open('.login', 'r') as rf:
    username = rf.readline()
    password = rf.readline()
login(username, password)
for i, mp_id in enumerate(data):
    if mp_id not in my_list:
        continue
    if mp_id not in errors:
        errors[mp_id] = []
    # if i > 3:
    #     continue
    path = Path(icsd_download_path)
    path = Path.joinpath(path, mp_id)
    if len(data[mp_id]) == 0:
        continue
    elif not os.path.exists(path.as_posix()):
        os.mkdir(path.as_posix())
    elif any(["standardized" in x for x in os.listdir(path.as_posix())]):
        continue
    found_one = False
    for icsd_id in data[mp_id]:
        if found_one:
            continue
        try:
            # check only in experimental
            clear_query()
            enter_icsd(icsd_id)
            run_query()
            name = f"{mp_id}"
            print(name)
            select_all()
            # export_data(name, "experimental")
            export_data(name, "standardized")
            back_to_query()
            found_one = True

        except:
            errors[mp_id].append(icsd_id)
            continue
            # # clear_query()
            # check_uncheck_theory()
            # try:
            #     enter_icsd(icsd_id)
            #     run_query()
            #     name = f"{mp_id}-theoritical"
            #     print(name)
            #     select_all()
            #     export_data(name, "experimental")
            #     export_data(name, "standardized")
            #     back_to_query()
            # except:
            #     # uncheck the theoritical
            #     # check_uncheck_theory()
            #     errors[mp_id].append(icsd_id)
            #     continue
        for fname in ['standardized']:
            src_path = Path(chrome_download_path)
            src_path = Path.joinpath(
                src_path, f"{name}_{fname}_CollCode{icsd_id}.zip")
            dst_path = Path.joinpath(path, f"{name}_{fname}_{icsd_id}")
            if os.path.exists(src_path.as_posix()):
                shutil.unpack_archive(src_path, dst_path)
            else:
                errors[mp_id].append(icsd_id)
logout()
with open('errors.json', 'w') as wf:
    json.dump(errors, wf, indent=True)
