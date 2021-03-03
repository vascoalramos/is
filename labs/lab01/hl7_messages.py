from hl7apy.core import Message, Segment
from hl7.client import MLLPClient
import hl7
import nanoid
import re

from config import IP as SERVER_IP


def generate_hl7_orm_o01_message(sender, receiver, data, op):
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
    if op == 1:
        m.ORM_O01_ORDER.orc.orc_1 = "CA"
    elif op == 2:
        m.ORM_O01_ORDER.orc.orc_1 = "SC"
        m.ORM_O01_ORDER.orc.orc_5 = "CM"
    else:
        m.ORM_O01_ORDER.orc.orc_1 = "NW"
    m.ORM_O01_ORDER.ORC.orc_2 = str(data["number"])
    m.ORM_O01_ORDER.ORC.orc_3 = str(data["number"])
    m.ORM_O01_ORDER.ORC.orc_9 = m.msh.msh_7

    # obr
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
    time = re.sub("[\/\-:]", "", str(data["date"])[:10] + str(data["hour"]))
    m.ORM_O01_ORDER.ORM_O01_ORDER_DETAIL.ORM_O01_OBRRQDRQ1RXOODSODT_SUPPGRP.OBR.OBR_7 = (
        time
    )

    m.validate()
    return m.to_mllp()


def generate_hl7_oru_r01_message(sender, receiver, data, op):
    m = Message("ORU_R01")

    # msh
    m.MSH.msh_3 = sender
    m.MSH.msh_4 = sender
    m.MSH.msh_5 = receiver
    m.MSH.msh_6 = receiver
    m.MSH.msh_9 = "ORU^R01"
    m.MSH.msh_10 = nanoid.generate()
    m.MSH.msh_11 = "P"

    # pid
    m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_3 = str(data["patient_id"])
    m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_5 = data["patient_name"]
    m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_11 = data["patient_address"]
    m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_13 = data["patient_phone_number"]

    # orc
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORC.orc_1 = "RE"
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORC.orc_2 = str(data["number"])
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORC.orc_3 = str(data["number"])
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORC.orc_9 = m.msh.msh_7

    # obr
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.obr_2 = "1"
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.obr_2 = str(data["number"])
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.obr_3 = str(data["number"])
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.OBR_4 = (
        "M10405^TORAX, UMA INCIDENCIA"
    )
    time = re.sub("[\/\-:]", "", str(data["date"])[:10] + str(data["hour"]))
    m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.OBR_7 = time

    # obx
    for idx, line in enumerate(data["report"]):
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.add_segment(
            "OBX"
        )
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.children[
            idx
        ].obx_1 = str(idx + 1)
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.children[
            idx
        ].obx_2 = "TX"
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.children[
            idx
        ].obx_5 = line
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.children[
            idx
        ].obx_11 = "F"
    m.validate()

    # TODO: maybe improve this in the future
    message = m.to_mllp()[:-2]
    for (
        obx
    ) in (
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.ORU_R01_OBSERVATION.children
    ):
        message += obx.to_er7() + "\r"
    return message


def generate_hl7_message(type, sender, receiver, data, op=0):
    if type == "ORM_O01":
        return generate_hl7_orm_o01_message(sender, receiver, data, op)
    elif type == "ORU_R01":
        return generate_hl7_oru_r01_message(sender, receiver, data, op)
    else:
        raise ValueError("Message Type not suported")


def send_message(port, message):
    with MLLPClient(SERVER_IP, port) as client:
        client.send_message(hl7.parse(message))
