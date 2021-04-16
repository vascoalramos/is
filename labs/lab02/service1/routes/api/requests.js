const express = require("express");
const router = express.Router();

const request = require("../../controllers/request");

router.get("", (req, res) => {
    request.list().then((data) => {
        res.status(200).jsonp(data);
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

router.put("/:id", (req, res) => {
    let reqId = req.params.id;

    let status = req.body.status;

    if (status) {
        if (status === "canceled") {
            return res.status(200).jsonp({ message: "Canceled" });
        } else if (status === "completed") {
            return res.status(200).jsonp({ message: "Completed" });
        } else {
            return res.status(400).jsonp({ message: "'status' not valid!'" });
        }
    }

    let report = req.body.report;

    if (report) {
        // check if status is 'completed'
        return res.status(200).jsonp({ message: "Report submeted" });
    }

    return res.status(400).jsonp({ message: "Invalid payload!" });
});

module.exports = router;
