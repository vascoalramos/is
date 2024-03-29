const express = require("express");
const router = express.Router();
const axios = require("axios");

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
    req.body.info = req.body.info.replace(/\r/g, "");
    request
        .insert(req.body)
        .then((data) => {
            req.body.request_id = data.insertId;
            req.body.patient_id = patient_number;
            axios
                .post(`http://localhost:3001/api/requests`, req.body)
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit new patient to service 2", error: error });
                });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

router.post("/addPatient", function (req, res) {
    patient
        .insert(req.body)
        .then(() => {
            axios
                .post(`http://localhost:3001/api/patients`, req.body)
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit new patient to service 2", error: error });
                });
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

router.post("/cancel/:id", function (req, res) {
    request
        .updateStatus(req.params.id, "canceled")
        .then(() => {
            axios
                .put(`http://localhost:3001/api/requests/${req.params.id}`, { status: "canceled" })
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit new request to service 2", error: error });
                });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

module.exports = router;
