from database.sql import sql
from extractor import extractor
from settings import settings

def main():
    settings.init()
    extractor.foo()

if __name__ == "__main__":
    main()