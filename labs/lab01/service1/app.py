import sys, inspect

from mysql.connector import connect
from os import path, makedirs

currentdir = path.dirname(path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = path.dirname(currentdir)
sys.path.insert(0, parentdir)

from common.config import services, PORT2 as SERVER_PORT
from common.hl7_messages import generate_hl7_message, send_message

username = services[0]["username"]
password = services[0]["password"]
db_name = services[0]["db_name"]


def store_message(id, message):
    completeName = "logs/" + id
    with open(completeName, "w") as file:
        file.write(message)


def register_request(conn, r):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM patient WHERE number={r['patient_number']}")
        results = cursor.fetchall()
        conn.commit()

        patient_id = None

        if results == []:
            cursor.execute(
                f"""INSERT INTO patient (number, name, address, phone_number)
                VALUES ({r["patient_number"]}, '{r["patient_name"]}', '{r["patient_address"]}', '{r["patient_phone_number"]}')"""
            )
            conn.commit()

            patient_id = cursor.lastrowid

            # hl7 message
            id, m = generate_hl7_message("ADT_A08", "Service1", "Service2", r)
            store_message(id, m)
            send_message(SERVER_PORT, m)

        else:
            results = results[0]
            patient_id = results["id"]

            if (
                results["address"] != r["patient_address"]
                or results["phone_number"] != r["patient_phone_number"]
                or results["name"] != r["patient_name"]
            ):
                r["patient_name"] = (
                    r["patient_name"] if r["patient_name"] != "" else results["name"]
                )
                r["patient_phone_number"] = (
                    r["patient_phone_number"]
                    if r["patient_phone_number"] != ""
                    else results["phone_number"]
                )
                r["patient_address"] = (
                    r["patient_address"]
                    if r["patient_address"] != ""
                    else results["address"]
                )
                cursor.execute(
                    f"""UPDATE patient
                    SET name = '{r["patient_name"]}', address = '{r["patient_address"]}', phone_number = '{r["patient_phone_number"]}'
                    WHERE number={r['patient_number']};"""
                )

                # hl7 message
                id, m = generate_hl7_message("ADT_A08", "Service1", "Service2", r)
                store_message(id, m)
                send_message(SERVER_PORT, m)

        cursor.execute(
            f"""INSERT INTO request (date, hour, patient_id, episode_number, info)
            VALUES ('{r["date"]}', '{r["hour"]}', {patient_id}, {r["episode_number"]}, 'M10405^TORAX, UMA INCIDENCIA')"""
        )
        conn.commit()

        # hl7 message
        r["number"] = cursor.lastrowid
        id, m = generate_hl7_message("ORM_O01", "Service1", "Service2", r)
        store_message(id, m)
        send_message(SERVER_PORT, m)
        return cursor.lastrowid


def cancel_request(conn, req_id):
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"UPDATE request SET status='canceled' WHERE number={req_id}")
        cursor.execute(
            f"SELECT * FROM request JOIN patient ON patient_id = id WHERE request.number={req_id}"
        )
        results = cursor.fetchall()
        conn.commit()

        results[0]["number"] = req_id
        results[0]["patient_number"] = results[0]["number"]
        results[0]["patient_name"] = results[0]["name"]
        results[0]["patient_address"] = results[0]["address"]
        results[0]["patient_phone_number"] = results[0]["phone_number"]
        del results[0]["id"]
        del results[0]["name"]
        del results[0]["address"]
        del results[0]["phone_number"]

        # hl7 message
        id, m = generate_hl7_message("ORM_O01", "Service1", "Service2", results[0], 1)
        store_message(id, m)
        send_message(SERVER_PORT, m)


def check_request_status(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM request WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        if results:
            return results[0][0]
        else:
            return None


def get_request_report(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT report FROM request WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        if results:
            return results[0][0]
        else:
            return None


def check_request_exists(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM request WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        return results != []


def check_request_is_canceled(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM request WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        return results[0][0].lower() == "canceled"


def menu():
    print("Available options:")
    print("(i) insert new request")
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
            request = {}
            try:
                request["patient_number"] = int(input("Patient number: "))
                request["patient_name"] = input("Patient name: ")
                request["patient_address"] = input("Patient address: ")
                request["patient_phone_number"] = input("Patient phone number: ")
                request["date"] = input("Exam date: ")
                request["hour"] = input("Exam hour: ")
                request["episode_number"] = int(input("Episode number: "))
                request["info"] = input("Aditional clinical info: ")
            except:
                print("Invalid input!")

            try:
                req_id = register_request(conn, request)
                print(f"New request inserted successfully. Number: {req_id}\n")
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
                        if not check_request_is_canceled(conn, req_id):
                            cancel_request(conn, req_id)
                            print(f"Medical exam request canceled successfully!\n")
                        else:
                            print(f"The request nº{req_id} was already canceled!\n")
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
                    report = get_request_report(conn, req_id)
                    if report:
                        print(f"The report for the request nº{req_id} is:\n{report}\n")
                    else:
                        print(f"The request nº{req_id} does not have a report yet!\n")
                else:
                    print(f"The request nº{req_id} does not exist!\n")
            except:
                print("Invalid input!")

        else:
            print("Invalid option!\n")

    conn.close()


if __name__ == "__main__":
    if not path.exists("logs"):
        makedirs("logs")
    main()