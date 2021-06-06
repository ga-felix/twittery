from db.sql import sql
from crawler import crawler

def main():
    db = sql.Sql("twitter", "root", "zxc12989")
    crawler.foo()

if __name__ == "__main__":
    main()