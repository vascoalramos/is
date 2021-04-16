const express = require("express");
const router = express.Router();

const patient = require("../../controllers/patient");

router.get("", (req, res) => {
    patient.list().then((data) => {
        res.status(200).jsonp(data);
    });
});

router.post("", (req, res) => {
    patient
        .insert(req.body)
        .then(() => {
            res.status(200).jsonp({ message: "Success" });
        })
        .catch((error) => {
            res.status(500).jsonp(error);
        });
});

module.exports = router;
