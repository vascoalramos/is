const express = require("express");
const router = express.Router();

const patient = require("../../controllers/patient");

router.get("/", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { title: "Express", data: data });
    });
});

module.exports = router;
