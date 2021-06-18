from database.sql import sql
from extractor import extractor
from settings import settings
import threading

def main():
    settings.init()
    thread1 = threading.Thread(target = extractor.foo, args = ())
    thread2 = threading.Thread(target = extractor.foo, args = ())
    thread3 = threading.Thread(target = extractor.foo, args = ())
    #thread4 = threading.Thread(target = extractor.foo, args = ())
    thread1.start()
    thread2.start()
    thread3.start()
    #thread4.start()
    
if __name__ == "__main__":
    main()