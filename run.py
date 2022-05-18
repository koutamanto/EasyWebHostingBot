import subprocess
import threading

t1 = threading.Thread(target=subprocess.run, args=("py -3.8 scripts/discord_bot.py",))
t2 = threading.Thread(target=subprocess.run, args=("py -3.8 main.py",))

t1.start()
t2.start()

t1.join()
t2.join()

print(threading.current_thread().name)