import logging 
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import dotenv
from pathlib import Path
from shutil import rmtree

from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import *

from datetime import datetime
import time
from numpy import random
import json
import csv
import os
import glob


class ChomeDriver(QObject):
    done = pyqtSignal()
    
    def __init__(self,parent=None, headless=False):
        super().__init__(parent=parent)
        self.headless=headless
        self.timeout = 10
        self.FIRST = True
        self.LATCHED = None
        self.HEADERS_SAVED = False
        self.running = False
        
    def highlight(self, element, effect_time, color, border):
        """Highlights (blinks) a Selenium Webdriver element"""
        def apply_style(s):
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
        original_style = element.get_attribute('style')
        apply_style("border: {0}px solid {1};".format(border, color))
        time.sleep(effect_time)
        apply_style(original_style)
    
    def download_wait(self, directory, timeout, nfiles=None):
        """
        Wait for downloads to finish with a specified timeout.

        Args
        ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        nfiles : int, defaults to None
            If provided, also wait for the expected number of files.

        """
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            self.delay(1)
            dl_wait = False
            files = os.listdir(directory)
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1
        return seconds
    
    def stop_interupt(self):
        # self.quit()
        self.running = False
        print("Stopping soon")
    
    def quit(self):
        self.driver.quit()
        self.FIRST = True
        self.LATCHED = None
        self.running = False
 
    def execute(self, form_data, combinations, **kwargs):
        
        # if self.FIRST:
        #     return None
        
        download_path = os.getenv('DOWNLOAD_PATH')
        
        if download_path is None:
            dotenv_file = dotenv.find_dotenv()
            if len(dotenv_file) == 0:
                with open('.env', 'w') as env: pass
                dotenv_file = dotenv.find_dotenv()
                
            os.environ["DOWNLOAD_PATH"] = 'run'
            dotenv.set_key(dotenv_file, "DOWNLOAD_PATH", os.environ["DOWNLOAD_PATH"])
        
        
        download_path = os.path.join(os.getenv('DOWNLOAD_PATH'))
        self.running = True
        print("Download path = ", os.path.abspath(download_path))
                   
        if self.FIRST:
            try:
                for path in Path(download_path).glob("**"+os.sep+"*"):
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        rmtree(path)
            except Exception as e:
                return 
            
            # self.navigate_to_strategy(False)
        
        defaults = self.capture_defaults()
        defaults.append(' ')
        defaults.append(' ')
        summary_data = [list((' ', *tuple(self.parameters), 'Net Profit', 'Ticker')), defaults]
        
            
        if all(v is None for v in combinations[0]):
            self.quit()
            self.done.emit()
            return
        
        
        # making sure tickers are active
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "symbolName-FeemEKQq")))
        tickers = self.driver.find_elements_by_class_name('symbolName-FeemEKQq')
        activeTicker = kwargs.get('activeTicker')
        isdeep = kwargs.get('isdeep')
        deep = self.driver.find_elements_by_class_name('input-Wv0rGnT8')[-1]
        state = deep.is_selected()
        if isdeep^state:
            self.click(deep)
                
                
        idx = 0
        for ti in range(len(tickers)): 
            if not activeTicker:
                # self.click(ticker)
                tickers[ti].click()
                self.delay(4)

            tickername = self.driver.find_elements_by_class_name('text-_iN2IH5A')[-1].text
            # making sure deep is selected if wanted
            
            
            # populating values    
            for j, combination in enumerate(combinations):
                if not self.running:
                    break
                
                i= 0
                index  = 0
                offset = 0
                self.click_settings_button()
                self.click_input_tab()
                print(f"Working on combination no. {j}")
                content = self.driver.find_element_by_class_name('content-mTbR5jYu')
                rows = content.find_elements_by_css_selector('.cell-mTbR5jYu')
                
                ok_button = self.driver.find_elements_by_css_selector('[data-name="submit-button"]')[0]
                # Filling data
                while i < len(rows):
                    is_checkbox = 'fill' in rows[i].get_attribute('class')
                    skip = rows[i].get_attribute('class').lower().find('checkabletitle') > -1
                    if skip:
                        i = i+1
                        offset = offset + 1
                        continue
                    
  
                    if combination[index] is not None:
                        if form_data[index]['is_input']:
                            input_element = rows[i+1].find_elements_by_css_selector('.container-Mtq7m9Yl')[0]
                            input = input_element.find_elements_by_css_selector('.input-oiYdY6I4')[0]
                            # self.driver.execute_script("arguments[0].value = '';", input)
                            
                            isfloat = defaults[index+1].find('.') > 0
                            if not isfloat:
                                val = str(int(combination[index]))
                            else:
                                val = str(combination[index])
                                
                            self.fill_element(input, val)
                            # self.driver.execute_script("arguments[0].value = arguments[1];", input, str(combination[index]))
                            
                        elif form_data[index]['is_dropbox']:
                            input_element = rows[i+1].find_elements_by_css_selector('.container-Mtq7m9Yl')[0]
                            self.click(input_element)
                            options = self.driver.find_element_by_class_name('menuBox-biWYdsXC').find_elements_by_css_selector('[role="option"]')
                            target_option = [o for o in options if o.text == combination[index]][0]
                            self.click(target_option)

                        elif form_data[index]['is_checkbox']:
                            input_element = rows[i].find_elements_by_css_selector('[type="checkbox"]')[0]
                            state = input_element.is_selected()
                            if state ^ combination[index]:
                                self.click(input_element)
                        
                    index += 1
                    i = i+1 if is_checkbox else i+2
            
                self.click(ok_button)
                self.delay(1)

                if isdeep:
                    generate = self.driver.find_elements_by_class_name('content-OvB35Th_')[-1]
                    generate.click()
                
                
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="List of Trades"]')))
                # capturing
                self.driver.find_element(By.XPATH, '//button[text()="List of Trades"]').click()
                try:
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ka-table ")))
                except TimeoutException as e:
                    idx += 1
                    print("Cannot read output out of this combination")
                    continue
                
                download_btn = self.driver.find_elements_by_css_selector('.no-content-msfP1I4t')[-1]
                
                # print(download_btn)
                self.click(download_btn)
                # download_btn.click()
                # Wait for download
                secs = self.download_wait(os.getenv('DOWNLOAD_PATH'), 200, idx+1)
                print(secs)
                
                # rename it
                files = glob.glob(os.path.join(os.getenv('DOWNLOAD_PATH') , '*'))
                max_file = max(files, key=os.path.getmtime)
                
                filename = max_file.split(os.sep)[-1].split(".")[0]
                new_path = max_file.replace(filename, f'A{str(idx+1).zfill(5)}')
                os.rename(max_file, new_path)
                
                
                
                print(f"Downloaded {max_file} -> {new_path}")
                
                idx += 1
                
                self.driver.find_element(By.XPATH, '//button[text()="Overview"]').click()
                net_profit = self.driver.find_elements_by_xpath("//*[contains(@class, 'Value-b1pZpka9')]")[0].text.replace('−', '-')
                
                data_values = list((new_path,*tuple(str(c) if c is not None else ' ' for c in combination )))
                data_values.append(net_profit)
                data_values.append(tickername)
                summary_data.append(data_values)


                dmin = os.getenv('DELAY_MIN')
                dmax = os.getenv('DELAY_MAX')
                
                if dmin is None or dmax is None:
                    dotenv_file = dotenv.find_dotenv()
                    os.environ["DELAY_MIN"] = '3500'
                    os.environ["DELAY_MAX"] = '15000'
                    dotenv.set_key(dotenv_file, "DELAY_MIN", os.environ["DELAY_MIN"])
                    dotenv.set_key(dotenv_file, "DELAY_MAX", os.environ["DELAY_MAX"])
                    dmin = os.getenv('DELAY_MIN')
                    dmax = os.getenv('DELAY_MAX')
                    
                time.sleep(random.uniform(int(dmin), int(dmax))/1000)

            if activeTicker:
                break
            
            # just updating again
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "symbolName-FeemEKQq")))
            tickers = self.driver.find_elements_by_class_name('symbolName-FeemEKQq')

        tstamp = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
        summary_data[1][-1] = summary_data[2][-1]
        
        download_path = os.getenv('DOWNLOAD_PATH')
        
        for i in summary_data:
            self.append_to_csv(i, os.path.join(download_path, f'{os.getenv("CSV_PATH")}_{tstamp}.csv'))
        
        if self.running:
            self.done.emit()
        
        # self.quit()
        
    def prepare_driver(self):
        # helper to edit 'Preferences' file inside Chrome profile directory.
        # https://stackoverflow.com/questions/61616747/selenium-chrome-load-profile-and-change-download-folder-python
        
        options = webdriver.ChromeOptions()
        download_path = os.path.join(os.getcwd(), 'run\\')
        profile_path = os.path.dirname(os.getenv('CHROME_PROFILE'))
        profile_name = os.path.basename(os.getenv('CHROME_PROFILE'))
        options.headless = self.headless
        options.add_argument(f"user-data-dir={profile_path}")
        options.add_argument(f"--profile-directory={profile_name}")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        
        try:
            def set_download_directory(profile_path, profile_name, download_path):
                    prefs_path = os.path.join(profile_path, profile_name, 'Preferences')
                    with open(prefs_path, 'r') as f:
                        prefs_dict = json.loads(f.read())
                    prefs_dict['download']['default_directory'] = download_path
                    prefs_dict['savefile']['directory_upgrade'] = True
                    prefs_dict['download']['directory_upgrade'] = True
                    with open(prefs_path, 'w') as f:
                        json.dump(prefs_dict, f)
                        
            print('Changing download directory')
            # set_download_directory(profile_path, profile_name, download_path) # Edit the Preferences first before loading the profile.
            print('Changing download directory Done')
            
        except Exception as e:
            import traceback
            print(str(e))
            traceback.print_exc()

        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.join(os.getcwd(), 'run\\'),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })
            
            
            
        print('Opening sChrome')

        # start chrome
        print('Opening driver')
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 60)
        return self.driver
    
    def delay(self,delay):
        time.sleep(delay)
    
    def fill_element(self,element,data):
        for i in range(4):
            element.send_keys(Keys.BACKSPACE)
            
        for char in data:
            element.send_keys(char)
            self.delay(0.1)

    def scroll(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def click(self, element):
        self.driver.execute_script("arguments[0].click();",element)

    def click_strategy_tester(self):
        """check if strategy tester tab is the active tab. If it's not, click to open tab."""
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title-uqXh1Q3i")))

            strategy_tester_tab = self.driver.find_elements(By.CLASS_NAME, "title-uqXh1Q3i")
            for index, web_element in enumerate(strategy_tester_tab):
                if web_element.text == "Strategy Tester":
                    active_tab = strategy_tester_tab[index].get_attribute("data-active")
                    if active_tab == "false":
                        strategy_tester_tab[index].click()
                        break
        except Exception:
            print("Could Not Click Strategy Tester Tab. Please Check web element's class name in commands.py file.")

    def click_settings_button(self):
        """click settings button."""
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "light-button-msfP1I4t")))

            settings_button = self.driver.find_element(By.CLASS_NAME, "light-button-msfP1I4t")
            settings_button.click()

        except Exception:
            print("Could not click settings button. Please check web_element's in commands.py file.")
    
    def click_input_tab(self):
        """click the input tab."""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "tab-Rf5MOAG5"))
            )
            
            input_tab = self.driver.find_element(By.CLASS_NAME, "tab-Rf5MOAG5")
            if input_tab.get_attribute("data-value") == "inputs":
                # input_tab.click()
                self.click(input_tab)
                return True
            return False
        except IndexError:
            print("Could not input tab button. Please check web_element's in commands.py file.")
            return False
    
    def capture_defaults(self):
        self.click_strategy_tester()
        self.click_settings_button()
        self.click_input_tab()
        content = self.driver.find_element_by_class_name('content-mTbR5jYu')
        rows = content.find_elements_by_css_selector('.cell-mTbR5jYu')
        self.values = [' ']
        
        i = 0
        while i < len(rows):
            label = rows[i].text
            self.scroll(rows[i])
            is_checkbox = 'fill' in rows[i].get_attribute('class')
            skip = rows[i].get_attribute('class').lower().find('checkabletitle') > -1
            if skip:
                i = i+1
                continue
            
            # self.highlight(rows[i], 2, "red", 1)
            if not is_checkbox:    
                input_element = rows[i+1].find_elements_by_css_selector('.container-Mtq7m9Yl')[0]
                
                is_input = len(input_element.find_elements_by_css_selector('.input-oiYdY6I4')) > 0
                is_dropbox = len(input_element.find_elements_by_class_name('button-allnSfnt')) > 0
                
                if is_input:
                    value = input_element.find_elements_by_css_selector('.input-oiYdY6I4')[0].get_attribute("value")
                    self.values.append(value)
                elif is_dropbox:
                    value = input_element.find_elements_by_class_name('button-children-nCHoYtuE')[0].text
                    self.values.append(value)
                    
                
            else:
                input_element = rows[i].find_elements_by_css_selector('[type="checkbox"]')[0]
                value = str(input_element.is_selected())
                self.values.append(value)
            
                
            i = i+1 if is_checkbox else i+2

        return self.values
    
    def navigate_to_strategy(self, capture=True):
        if not self.FIRST:
            return None
        try:
            self.prepare_driver()
            print('Navigating to strategy link')
            self.driver.get(os.getenv('STRATEGY')) 
            
            time.sleep(2)
            if not capture:
                return
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-name="base"]')))
            tickers_bar = self.driver.find_element_by_xpath('//*[@data-name="base"]')
            is_active = tickers_bar.get_attribute('class').lower().find('isactive') > -1
            if not is_active:
                tickers_bar.click()
            
            # extract strategy parameters
            self.click_strategy_tester()
            self.click_settings_button()
            self.click_input_tab()
            
            
            
            time.sleep(2)
            print('Capturing parameters')
            content = self.driver.find_element_by_class_name('content-mTbR5jYu')
            rows = content.find_elements_by_css_selector('.cell-mTbR5jYu')
            fields = []
            self.parameters = []
            i = 0
            while i < len(rows):
                label = rows[i].text
                skip = rows[i].get_attribute('class').lower().find('checkabletitle') > -1
                if skip:
                    i = i+1
                    continue
                
                is_checkbox = 'fill' in rows[i].get_attribute('class')
                options = []
                
                if not is_checkbox:    
                    input_element = rows[i+1].find_elements_by_css_selector('.container-Mtq7m9Yl')[0]
                    is_input = len(input_element.find_elements_by_css_selector('.input-oiYdY6I4')) > 0
                    is_dropbox = len(input_element.find_elements_by_class_name('button-allnSfnt')) > 0
                    # is_checkbox = len(input_element.find_elements_by_class_name('checkbox-dV7I8XN5')) > 0
                    
                    # input_element = input_element.find_elements_by_css_selector('.container-Mtq7m9Yl')[0].find_element_by_class_name('inner-slot-yJbunXPO').find_elements_by_css_selector('*')[0]
                    if is_dropbox:
                        element = input_element.find_elements_by_class_name('button-allnSfnt')[0]
                        self.click(element)
                        options = [o.text for o in self.driver.find_element_by_class_name('menuBox-biWYdsXC').find_elements_by_css_selector('[role="option"]')]
                        self.click(element)
                else:
                    is_input = False
                    is_dropbox = False
                
                self.parameters.append(label)
                field = {'label': label, 
                            'is_input':is_input, 
                            'is_dropbox':is_dropbox, 
                            'is_checkbox':is_checkbox, 
                            'value':options}
                fields.append(field)
                print(field)
                i = i+1 if is_checkbox else i+2


            self.click(self.driver.find_element_by_class_name('close-HS2PTQRJ'))
            
            
            
            print('Saving Captured parameters')
            with open('strategy_params.json', 'w') as fout:
                json.dump(fields , fout)
            
            return fields

        except Exception as e:
            print(str(e))
            return None
        
    def append_to_csv(self, data_list, filename):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_list)