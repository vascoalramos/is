const express = require("express");
const router = express.Router();

const request = require("../../controllers/request");

router.get("", (req, res) => {
    request
        .list()
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

router.post("", (req, res) => {
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
        if (status === "canceled" || status === "completed") {
            if (currentStatus === "canceled") {
                return res.status(400).jsonp({ message: "Request is already canceled!" });
            } else if (currentStatus === "completed") {
                return res.status(400).jsonp({ message: "Request is already completed!" });
            }

            try {
                await request.updateStatus(reqId, status);
                return res.status(200).jsonp({ message: status.charAt(0).toUpperCase() + status.slice(1) });
            } catch (error) {
                console.log(error);
                return res.status(500).jsonp(error);
            }
        } else {
            return res.status(400).jsonp({ message: "'status' not valid!'" });
        }
    }

    let report = req.body.report;

    if (report) {
        if (currentStatus === "canceled") {
            return res.status(400).jsonp({ message: "Request is already canceled!" });
        } else if (currentStatus !== "completed") {
            return res.status(400).jsonp({ message: "Request was not yet completed!" });
        }

        try {
            await request.writeReport(reqId, report);
            return res.status(200).jsonp({ message: "Report submited" });
        } catch (error) {
            console.log(error);
            return res.status(500).jsonp(error);
        }
    }

    return res.status(400).jsonp({ message: "Invalid payload!" });
});

module.exports = router;
