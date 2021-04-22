const express = require("express");
const router = express.Router();

const request = require("../../controllers/request");

router.get("/", function (req, res) {
    request.list().then((data) => {
        console.log(data);
        res.render("index", { view: "listExams", data: data });
    });
});

router.get("/addRequest", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view: "addRequest", data: data });
    });
});

router.get("/filter", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view: "filter", data: data });
    });
});

router.get("/addPacient", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view: "addPacient", data: data });
    });
});

module.exports = router;
