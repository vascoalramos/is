from mysql.connector import connect
from hl7apy.core import Message

from config import username, password, db_name


def register_request(conn, r):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO requests (date, hour, patient_id, patient_name, patient_address, patient_phone_number, episode_number, info)
            VALUES ('{r["date"]}', '{r["hour"]}', {r["patient"]["number"]}, '{r["patient"]["name"]}', '{r["patient"]["address"]}', '{r["patient"]["phone_number"]}', {r["episode_number"]}, '{r["clinical_info"]}')"""
        )
        # TODO: insert to work list

        conn.commit()
        return cursor.lastrowid


def cancel_request(conn):
    print("Operation not yet implemented\n")


def check_request_status(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM requests WHERE number={req_id}")
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None


def get_request_report(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT report FROM requests WHERE number={req_id}")
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None


def check_request_exists(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM requests WHERE number={req_id}")
        return cursor.fetchall() != []


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
            request = {"patient": {}}
            try:
                request["patient"]["number"] = int(input("Patient number: "))
                request["patient"]["name"] = input("Patient name: ")
                request["patient"]["address"] = input("Patient address: ")
                request["patient"]["phone_number"] = input("Patient phone number: ")
                request["date"] = input("Exam date: ")
                request["hour"] = input("Exam hour: ")
                request["episode_number"] = int(input("Episode number: "))
                request["clinical_info"] = input("Aditional clinical info: ")
            except:
                print("Invalid input!")

            try:
                req_id = register_request(conn, request)
                print(f"New request inserted successfully. ID: {req_id}\n")
            except Exception as e:
                print("Operation failded! Try again!\nError:" + str(e) + "\n")

        elif op == "c":
            cancel_request(conn)

        elif op == "s":
            try:
                req_id = int(input("Medical exam request ID: "))

                if check_request_exists(conn, req_id):
                    status = check_request_status(conn, req_id)
                    print(
                        f"The status for the request with ID '{req_id}' is:  {status.upper()}\n"
                    )
                else:
                    print(f"The request with ID '{req_id}' does not exist!\n")
            except:
                print("Invalid input!")

        elif op == "r":
            try:
                req_id = int(input("Medical exam request ID: "))

                if check_request_exists(conn, req_id):
                    report = get_request_report(conn, req_id)
                    if report:
                        print(
                            f"The report for the request with ID '{req_id}' is:\n{report}\n"
                        )
                    else:
                        print(
                            f"The request with ID '{req_id}' does not have a report yet!\n"
                        )
                else:
                    print(f"The request with ID '{req_id}' does not exist!\n")
            except:
                print("Invalid input!")

        else:
            print("Invalid option!\n")

    conn.close()


if __name__ == "__main__":
    main()