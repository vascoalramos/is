const express = require("express");
const router = express.Router();

const patient = require("../../controllers/patient");

router.get("/", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view : "addPacient", data: data });
    });
});

router.get("/addRequest", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view : "addRequest", data: data });
    });
});

router.get("/filter", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view : "filter", data: data });
    });
});

router.get("/list", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view : "listExams", data: data });
    });
});


module.exports = router;
