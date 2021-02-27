from mysql.connector import connect, Error
from config import username, password, db_name

conn = None


def menu():
    print("Available options:")
    print("(i) register new request")
    print("(c) cancel request")
    print("(s) check request status")
    print("(r) see request report")
    print("(e) exit")
    return input("Option? ")


def main():
    try:
        conn = connect(
            host="localhost",
            user=username,
            password=password,
            database=db_name,
        )
    except:
        print("Connection to db not sucessfull")
        exit(1)

    print("Welcome to Medical Requests Register\n")

    while True:
        op = menu()
        if op == "e":
            print("\nEXIT\n")
            break

        elif op == "i":
            print("Operation not yet implemented\n")

        elif op == "c":
            print("Operation not yet implemented\n")

        elif op == "s":
            print("Operation not yet implemented\n")

        elif op == "r":
            print("Operation not yet implemented\n")

        else:
            print("Invalid option!\n")

    conn.close()


if __name__ == "__main__":
    main()