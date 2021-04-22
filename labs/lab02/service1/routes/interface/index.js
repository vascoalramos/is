const express = require("express");
const router = express.Router();

const request = require("../../controllers/request");
const patient = require("../../controllers/patient");

router.get("/", function (req, res) {
    request.list().then((data) => {
        res.render("index", { view: "listExams", data: data });
    });
});

router.get("/addRequest", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { view: "addRequest", data: data });
    });
});

router.get("/filter", function (req, res) {
    request.list().then((data) => {
        res.render("index", { view: "filter", data: data });
    });
});

router.get("/addPatient", function (req, res) {
    res.render("index", { view: "addPatient" });
});

router.post("/addRequest", function (req, res) {
    let [patient_id, patient_number] = req.body.patient_id.split(";");
    req.body.patient_id = patient_id;
    request
        .insert(req.body)
        .then(() => {
            res.redirect("/");
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

router.post("/addPatient", function (req, res) {
    console.log(req.body);
    patient
        .insert(req.body)
        .then(() => {
            res.redirect("/");
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

router.post("/filter", function (req, res) {
    request
        .filterByDate(req.body.date)
        .then((data) => {
            res.render("index", { view: "filter", date: req.body.date, data: data });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

module.exports = router;
