
from threading import Thread

def run_proccess(command):
    thread = Thread(target=command)
    thread.start()