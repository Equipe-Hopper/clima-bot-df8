# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

from webdriver_manager.chrome import ChromeDriverManager



class Bot(WebBot):

    def pesquisar_cidade(self, cidade: str) -> None:
        while len(self.find_elements('//*[@id="search"]', By.XPATH)) < 1:
            self.wait(1000)
            print('carregando...')
            
        self.find_element('//*[@id="search"]', By.XPATH).send_keys(cidade)
        self.wait(2000)#Aguarda determinados segundos
        self.page_down()
        self.wait(1000)#Aguarda determinados segundos
        self.enter()
        self.wait(2000)#Aguarda determinados segundos
        self.find_element('//*[@id="previsao"]/div[3]/a[1]/button', By.XPATH).click() #Btn proximos dias

    
    def selecionar_aba(self):
        """Seleciona a segunda aba do navegador"""
        abas_abertas = self.get_tabs()
        nova_aba = abas_abertas[1]
        self.activate_tab(nova_aba)



    def extrair_dados_clima(self):
        self.selecionar_aba()

        while len(self.find_elements('//*[@id="containerFullScreen"]/div/div/section[1]/div/font/b', By.XPATH)) < 1:
            print('carregando...')
            self.wait(1000)

        coleta = {
            'dia1': {},
            'dia2': {},
            'dia3': {},
            'dia4': {},
            'dia5': {},
        }

        dia1 = self.find_element('//*[@id="containerFullScreen"]/div/div/section[1]/div/font/b', By.XPATH).text
        dia2 = self.find_element('//*[@id="containerFullScreen"]/div/div/section[4]/div/font/b', By.XPATH).text
        dia3 = self.find_element('//*[@id="containerFullScreen"]/div/div/div[1]/section[1]/div/font/b', By.XPATH).text
        dia4 = self.find_element('//*[@id="containerFullScreen"]/div/div/div[2]/section[1]/div/font/b', By.XPATH).text
        dia5 = self.find_element('//*[@id="containerFullScreen"]/div/div/div[3]/section[1]/div/font/b', By.XPATH).text

        dia1 = dia1.split('-')
        dia2 = dia2.split('-')
        dia3 = dia3.split('-')
        dia4 = dia4.split('-')
        dia5 = dia5.split('-')

        coleta['dia1']['data'] = dia1[1]
        coleta['dia2']['data'] = dia2[1]
        coleta['dia3']['data'] = dia3[2]
        coleta['dia4']['data'] = dia4[2]
        coleta['dia5']['data'] = dia5[2]        
        

        print(coleta)

        temp_min = self.find_element('//*[@id="containerFullScreen"]/div/div/section[2]/div[1]/font[1]',By.XPATH).text
        temp_max = self.find_element('//*[@id="containerFullScreen"]/div/div/section[2]/div[2]/font[1]',By.XPATH).text
                                    


        
 






            

    


    def configuracoes_bot(self) -> None:
        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = ChromeDriverManager().install()

    
    def abrir_site(self, url: str = "https://www.botcity.dev") -> None:
        try:
            # Opens the BotCity website.
            self.browse(url)
            self.maximize_window()
        except Exception as ex:
            print(f'Erro ao tentar abrir o site: {ex}')
            self.save_screenshot('Erro ao abrir o site.png')
            raise ex



    def action(self, execution = None):
        # Runner passes the server url, the id of the task being executed,
        # the access token and the parameters that this task receives (when applicable).
        maestro = BotMaestroSDK.from_sys_args()
        ## Fetch the BotExecution with details from the task, including parameters
        execution = maestro.get_execution()

        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")

        # Implement here your logic...

        try:
            self.configuracoes_bot()
            self.abrir_site(r'https://portal.inmet.gov.br/')

            self.pesquisar_cidade('Manaus')
            
            self.extrair_dados_clima()
           

        except Exception as ex:
            print('Erro: ', ex)
            self.save_screenshot('Erro.png')
        
        finally:
    
            # Wait 3 seconds before closing
            self.wait(6000)

            # Finish and clean up the Web Browser
            # You MUST invoke the stop_browser to avoid
            # leaving instances of the webdriver open
            self.stop_browser()

            # Uncomment to mark this task as finished on BotMaestro
            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task Finished OK."
            )


    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()