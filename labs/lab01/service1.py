from mysql.connector import connect
from hl7apy.core import Message
import hl7
import nanoid

from config import services

username = services[0]["username"]
password = services[0]["password"]
db_name = services[0]["db_name"]


def generate_hl7_orm_o01_message(sender, receiver, data, cancel=False):
    m = Message("ORM_O01")

    # msh
    m.msh.msh_3 = sender
    m.msh.msh_4 = sender
    m.msh.msh_5 = receiver
    m.msh.msh_6 = receiver
    m.msh.msh_9 = "ORM^O01"
    m.msh.msh_10 = nanoid.generate()
    m.msh.msh_11 = "P"

    # pid
    m.add_group("ORM_O01_PATIENT")
    m.ORM_O01_PATIENT.pid.pid_3 = str(data["patient"]["number"])
    m.ORM_O01_PATIENT.pid.pid_5 = data["patient"]["name"]
    m.ORM_O01_PATIENT.pid.pid_11 = data["patient"]["address"]
    m.ORM_O01_PATIENT.pid.pid_13 = data["patient"]["phone_number"]

    # pv1
    m.ORM_O01_PATIENT.ORM_O01_PATIENT_VISIT.pv1.pv1_2 = "I"
    m.ORM_O01_PATIENT.ORM_O01_PATIENT_VISIT.pv1.pv1_19 = str(data["episode_number"])

    # orc
    m.ORM_O01_ORDER.orc.orc_1 = "CA" if cancel else "NW"
    m.ORM_O01_ORDER.ORC.orc_2 = "4727374"
    m.ORM_O01_ORDER.ORC.orc_3 = "4727374"
    m.ORM_O01_ORDER.ORC.orc_9 = m.msh.msh_7

    # obr
    # m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.add_segment("OBR")
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_2 = (
        "1"
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_2 = (
        "4727374"
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_3 = (
        "4727374"
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.OBR_4 = (
        "M10405^TORAX, UMA INCIDENCIA"
    )

    m.validate()
    return m.to_mllp().replace("\r", "\n")


def generate_hl7_message(type, sender, receiver, data):
    if type == "ORM_O01":
        return generate_hl7_orm_o01_message(sender, receiver, data)
    else:
        raise ValueError("Message Type not suported")


def register_request(conn, r):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO work_list (date, hour, patient_id, patient_name, patient_address, patient_phone_number, episode_number, info)
            VALUES ('{r["date"]}', '{r["hour"]}', {r["patient"]["number"]}, '{r["patient"]["name"]}', '{r["patient"]["address"]}', '{r["patient"]["phone_number"]}', {r["episode_number"]}, '{r["clinical_info"]}')"""
        )
        conn.commit()

        # hl7 message
        m = generate_hl7_message("ORM_O01", "Service1", "Serivce2", r)
        # TODO: send message

        return cursor.lastrowid


def cancel_request(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"UPDATE work_list SET status='canceled' WHERE number={req_id}")
        conn.commit()

        # TODO: create cancel message


def check_request_status(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT status FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        if results:
            return results[0][0]
        else:
            return None


def get_request_report(conn, req_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT report FROM work_list WHERE number={req_id}")
        results = cursor.fetchall()
        conn.commit()
        if results:
            return results[0][0]
        else:
            return None


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
                print(f"New request inserted successfully. Number: {req_id}\n")
            except Exception as e:
                print("Operation failded! Try again!\nError:" + str(e) + "\n")

        elif op == "c":
            try:
                req_id = int(input("Medical exam request nº: "))

                if check_request_exists(conn, req_id):
                    if not check_request_is_canceled(conn, req_id):
                        cancel_request(conn, req_id)
                        print(f"Medical exam request canceled successfully!\n")
                    else:
                        print(f"The request nº{req_id} was already canceled!\n")
                else:
                    print(f"The request nº{req_id} does not exist!\n")
            except:
                print("Invalid input!")

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
    main()