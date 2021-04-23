const express = require("express");
const router = express.Router();

const request = require("../../controllers/request");
const patient = require("../../controllers/patient");

router.get("", (req, res) => {
    let date = req.query.date;

    let action;

    if (date) {
        if (date === "today") {
            action = request.filterByDate(new Date().toISOString().slice(0, 10));
        } else if (/^\d{4}-\d{2}-\d{2}$/.test(date)) {
            action = request.filterByDate(date);
        } else {
            return res.status(400).jsonp({ message: "Date is not valid. Use format: yyyy-mm-dd" });
        }
    } else {
        action = request.list();
    }

    action
        .then((data) => {
            res.status(200).jsonp(data);
        })
        .catch((error) => {
            console.log(error);
            res.status(500).jsonp(error);
        });
});

router.get("/:id", (req, res) => {
    let reqId = req.params.id;

    request
        .get(reqId)
        .then((data) => {
            res.status(200).jsonp(data);
        })
        .catch((error) => {
            console.log(error);
            res.status(500).jsonp(error);
        });
});

router.post("", async (req, res) => {
    req.body.patient_id = (await patient.getPatientByNumber(req.body.patient_id))[0].patient_id;
    request
        .insert(req.body)
        .then(() => {
            res.status(200).jsonp({ message: "Success" });
        })
        .catch((error) => {
            console.log(error);
            res.status(500).jsonp(error);
        });
});

router.put("/:id", async (req, res) => {
    let reqId = req.params.id;

    let currentStatus;

    try {
        currentStatus = (await request.getStatus(reqId))[0].status;
    } catch {
        return res.status(404).jsonp({ message: "Request doesn't exist!" });
    }

    let status = req.body.status;

    if (status) {
        if (status === "canceled") {
            if (currentStatus === "canceled") {
                return res.status(400).jsonp({ message: "Request is already canceled!" });
            } else if (currentStatus === "completed") {
                return res.status(400).jsonp({ message: "Request is already completed!" });
            }

            try {
                await request.updateStatus(reqId, status);
                return res.status(200).jsonp({ message: "Canceled" });
            } catch (error) {
                console.log(error);
                return res.status(500).jsonp(error);
            }
        } else {
            return res.status(400).jsonp({ message: "'status' not valid!'" });
        }
    }

    return res.status(400).jsonp({ message: "Invalid payload!" });
});

module.exports = router;
