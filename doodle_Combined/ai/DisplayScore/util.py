import sqlite3 

def show_menu():

    print("1. reset data in database(set as not_added")
    print("2. clear data in database(set as not_added")
    print("enter no:", end='')


def main():
    conn = sqlite3.connect('score.sqlite')
    c = conn.cursor()
    show_menu()
    n = eval(input())
    if(n == 1) :
        c.execute("update info set is_added = 0;")
    else :
        c.execute("delete from info")
    conn.commit()
    print("done.")


if __name__ == '__main__':
    main()