from hl7apy.core import Message
import hl7
import nanoid


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
    return m.to_mllp().replace("\r", "\n")  # TODO: fix this


def generate_hl7_message(type, sender, receiver, data):
    if type == "ORM_O01":
        return generate_hl7_orm_o01_message(sender, receiver, data)
    else:
        raise ValueError("Message Type not suported")