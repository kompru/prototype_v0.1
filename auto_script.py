from input_settings import InputSettings
from datetime import datetime
import sched, time
import subprocess

current_script = "rappi_search.py"

def get_title():
    print("")
    print("".center(50, '='))
    print(f' running script every {InputSettings.AUTO_SCRIPT_SCHEDULER_TIME / 60} minutes '.center(50, '='))
    print(f' {current_script} '.center(50, '='))

    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
    time_format_str = f' Starting at: {formatted_time} '
    print(time_format_str.center(50, '='))
    print(" (CTRL + C) TO EXIT".center(50, '='))
    print("".center(50, '='))

def get_client():
    clients = InputSettings.CLIENTS
    clientIndex = None
    len_clients = len(clients)

    if len_clients == 0 or len_clients == 1:
        clientIndex = 0
    else:
        while clientIndex is None:
            print("ESCOLHA O CLIENTE (Entre com um número)")

            counter = 1
            for cl in clients:
                _client = cl["__NAME__"]
                print(f"[{counter}] - {_client}")
                counter += 1

            try:
                index = int(input())

                if index > 0 and index <= len_clients:
                    clientIndex = index - 1
                else:
                    print(f'-- Entre com o número entre 1 a {counter - 1} --')
            except ValueError:
                print('-- Entre com o número do cliente --')
    return str(clientIndex)

def rappi_searcher(_scheduler, clientIndex):
    get_title()

    subprocess.run(["python", current_script, clientIndex])

    _scheduler.enter(InputSettings.AUTO_SCRIPT_SCHEDULER_TIME, 1, rappi_searcher, (_scheduler, clientIndex))

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(0, 1, rappi_searcher, (scheduler, get_client()))
scheduler.run()