from mysql.connector import connect

from config import services, PORT1 as SERVER_PORT
from hl7_messages import generate_hl7_message, send_message

username = services[1]["username"]
password = services[1]["password"]
db_name = services[1]["db_name"]


def store_message(id, message):
    completeName = 'service2/' + id      
    with open(completeName, "w") as file:
        file.write(message)


def finish_request(conn, req_id):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"UPDATE work_list SET status='completed' WHERE number={req_id}")
        cursor.execute(f"SELECT * FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()

        # hl7 message
        id, m = generate_hl7_message("ORM_O01", "Service2", "Service1", results[0], 2)
        send_message(SERVER_PORT, m)


def cancel_request(conn, req_id):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"UPDATE work_list SET status='canceled' WHERE number={req_id}")
        cursor.execute(f"SELECT * FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()

        # hl7 message
        id, m = generate_hl7_message("ORM_O01", "Service2", "Service1", results[0], True)
        store_message(id,m)
        send_message(SERVER_PORT, m)

    


def check_request_status(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        if results:
            return results[0][0]
        else:
            return None


def publish_report(conn, req_id, lines):
    report = "\n".join(lines)
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"UPDATE work_list SET report='{report}' WHERE number={req_id}")
        cursor.execute(f"SELECT * FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()

        results[0]["report"] = results[0]["report"].split("\n")

        # hl7 message
        m = generate_hl7_message("ORU_R01", "Service2", "Service1", results[0], True)
        store_message(id,m)
        send_message(SERVER_PORT, m)




def check_request_exists(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        return results != []


def check_request_is_canceled(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        return results[0][0].lower() == "canceled"


def check_request_is_completed(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        return results[0][0].lower() == "completed"


def menu():
    print("Available options:")
    print("(f) finish request")
    print("(c) cancel request")
    print("(s) check request status")
    print("(r) publish report")
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

        elif op == "f":
            try:
                req_id = int(input("Medical exam request nº: "))
            except:
                print("Invalid input!")
            else:
                try:
                    if check_request_exists(conn, req_id):
                        if check_request_is_canceled(conn, req_id):
                            print(f"The request nº{req_id} was already canceled!\n")
                        elif check_request_is_completed(conn, req_id):
                            print(f"The request nº{req_id} was already completed!\n")
                        else:
                            finish_request(conn, req_id)
                            print(f"Medical exam request completed successfully!\n")

                    else:
                        print(f"The request nº{req_id} does not exist!\n")
                except Exception as e:
                    print("Operation failded! Try again!\nError:" + str(e) + "\n")

        elif op == "c":
            try:
                req_id = int(input("Medical exam request nº: "))
            except:
                print("Invalid input!")
            else:
                try:
                    if check_request_exists(conn, req_id):
                        if check_request_is_canceled(conn, req_id):
                            print(f"The request nº{req_id} was already canceled!\n")
                        elif check_request_is_completed(conn, req_id):
                            print(f"The request nº{req_id} was already completed!\n")
                        else:
                            cancel_request(conn, req_id)
                            print(f"Medical exam request canceled successfully!\n")
                    else:
                        print(f"The request nº{req_id} does not exist!\n")
                except Exception as e:
                    print("Operation failded! Try again!\nError:" + str(e) + "\n")

        elif op == "s":
            try:
                req_id = int(input("Medical exam request nº: "))

                if check_request_exists(conn, req_id):
                    status = check_request_status(conn, req_id)
                    print(
                        f"The status for the request nº{req_id} is:  {status.upper()}\n"
                    )
                else:
                    print(f"The request with nº{req_id} does not exist!\n")
            except:
                print("Invalid input!")

        elif op == "r":
            try:
                req_id = int(input("Medical exam request nº: "))
                if check_request_exists(conn, req_id):
                    if check_request_is_canceled(conn, req_id):
                        print(f"The request nº{req_id} was already canceled!\n")
                    else:
                        print("Enter report. Ctrl-D to save it.")
                        lines = []
                        while True:
                            try:
                                line = input()
                            except EOFError:
                                break
                            lines.append(line)
                        publish_report(conn, req_id, lines)
                        print(f"Medical exam request report published successfully!\n")
                else:
                    print(f"The request nº{req_id} does not exist!\n")
            except Exception as e:
                print("Operation failded! Try again!\nError:" + str(e) + "\n")

        else:
            print("Invalid option!\n")

    conn.close()


if __name__ == "__main__":
    main()