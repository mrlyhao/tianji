from threading import Thread
import time

def sayhi():
    time.sleep(10)
    a=b
    print('ceshi')
while True:
    try:
        t=Thread(target=sayhi)
        t.start()
        print('主线程')
        time.sleep(5)
    except:
        time.sleep(2)
        continue
