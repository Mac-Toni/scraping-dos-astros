import schedule
import time

def tarefa():
    print("Executando tarefa...")

schedule.every(5).seconds.do(tarefa)

while True:
    schedule.run_pending()
    time.sleep(1)