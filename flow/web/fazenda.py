from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from .. import cfg
import logging

class Fazenda(webdriver.Chrome):
    def __init__(self, driver_path=ChromeDriverManager().install(), teardown=False):
        self._driver_path = Service(driver_path)
        logging.debug("Baixado o WebDriver com êxito.")
        self._teardown = teardown
        self._prefs = {
            "download.default_directory": cfg["PATHS"]["PastaDownload"]
        }
        self._options = webdriver.ChromeOptions()
        self._options.add_experimental_option('prefs', self._prefs)
        self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self._options.add_experimental_option("useAutomationExtension", False)
        self._options.add_argument("--disable-blink-features=AutomationControlled")
        self._options.add_extension(r'.\extension_1_0_0_0.crx')
        super().__init__(service=self._driver_path, options=self._options)
        self.implicitly_wait(30)
        self.maximize_window()
        logging.debug("Instanciado o navegador com o WebDriver.")
        
    def __exit__(self, *args, **kwargs):
        if self._teardown:
            self.quit()
            logging.debug("Finalizado o WebDriver do navegador.")
        logging.debug("Mantido WebDriver com o navegador aberto.")
            
    def page_access(self):
        site = cfg['LOCAL']['PortalFazenda']
        self.get(site)
        logging.debug(f'Acessado o portal "{site}"')
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def nfe_submit(self, access_key: str):
        self.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtChaveAcessoResumo").send_keys(access_key)
        logging.debug(f"Inserido a chave de acesso {access_key} no campo.")
        input()
        self.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btnConsultarHCaptcha").click()
        logging.debug('Pressionado botão "Continuar"')
        ...
    
    def download_nfe(self):
        self.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btnDownload").click()
        # REMOVER SE O CERTIFICADO ESTIVER OK
        Alert(self).accept()