from flow.web.fazenda import Fazenda
from flow.useful.switchblade import FileReader, QueueCreator
from threading import Thread
from flow import cfg
from queue import Queue

def main(queue: Queue):
    obj = Fazenda()
    obj.page_access()
    while not queue.empty():
        cnpj, chave_acesso = queue.get()
        obj.nfe_submit(chave_acesso)
        queue.task_done()

def worker(queue: Queue):
    for _ in range(int(cfg['OPCOES']['QtdeAbas'])):
        t_worker = Thread(target=main, args=(queue,), daemon=True)
        t_worker.start()
        
try:
    content_file = FileReader(cfg['PATHS']['PastaNomeArquivoJsonInput']).json_ext()
    queue = QueueCreator(content_file).prepare()
    main(queue)
    worker(queue)
except BaseException as error:
    print(error)
    ...