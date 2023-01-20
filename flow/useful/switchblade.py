import json
from queue import Queue
from .. import cfg

class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def json_ext(self) -> dict:
        with open(self.file_path, "r+") as file:
            content = file.read()
        if content:
            content = json.loads(content)
        return content
    
class QueueCreator:
    def __init__(self, elements: dict) -> Queue:
        self.elements = elements
        
    def prepare(self):
        queue = Queue()
        cnpj = self.elements.get('cnpj_contribuinte')
        chaves_acesso = self.elements.get('chaves')
        for codigo in chaves_acesso:
            queue.put((cnpj, codigo.get("chave_acesso")))
        for _ in range(int(cfg['OPCOES']['QtdeAbas'])):
            queue.put("False")
        return queue
        