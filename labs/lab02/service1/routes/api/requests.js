const express = require("express");
const router = express.Router();

const patient = require("../../controllers/patient");

router.get("", (req, res) => {
    patient.list().then((data) => {
        res.status(200).jsonp(data);
    });
});

module.exports = router;
