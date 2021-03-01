from hl7apy.core import Message
from hl7.client import MLLPClient
import hl7
import nanoid
import re

from config import IP as SERVER_IP


def generate_hl7_orm_o01_message(sender, receiver, data, cancel):
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
    m.ORM_O01_PATIENT.pid.pid_3 = str(data["patient_id"])
    m.ORM_O01_PATIENT.pid.pid_5 = data["patient_name"]
    m.ORM_O01_PATIENT.pid.pid_11 = data["patient_address"]
    m.ORM_O01_PATIENT.pid.pid_13 = data["patient_phone_number"]

    # pv1
    m.ORM_O01_PATIENT.ORM_O01_PATIENT_VISIT.pv1.pv1_2 = "I"
    m.ORM_O01_PATIENT.ORM_O01_PATIENT_VISIT.pv1.pv1_19 = str(data["episode_number"])

    # orc
    m.ORM_O01_ORDER.orc.orc_1 = "CA" if cancel else "NW"
    m.ORM_O01_ORDER.ORC.orc_2 = str(data["number"])
    m.ORM_O01_ORDER.ORC.orc_3 = str(data["number"])
    m.ORM_O01_ORDER.ORC.orc_9 = m.msh.msh_7

    # obr
    # m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.add_segment("OBR")
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_2 = (
        "1"
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_2 = str(
        data["number"]
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.obr_3 = str(
        data["number"]
    )
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.OBR_4 = (
        "M10405^TORAX, UMA INCIDENCIA"
    )
    time = str(data["date"])[:10] + str(data["hour"])
    time = re.sub("[\/\-:]", "", time)
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.OBR_7 = (
        time
    )

    m.validate()
    # return m.to_mllp().replace("\r", "\n")  # TODO: fix this
    return m.to_mllp()


def generate_hl7_message(type, sender, receiver, data, cancel=False):
    if type == "ORM_O01":
        return generate_hl7_orm_o01_message(sender, receiver, data, cancel)
    else:
        raise ValueError("Message Type not suported")


def send_message(port, message):
    with MLLPClient(SERVER_IP, port) as client:
        client.send_message(hl7.parse(message))
