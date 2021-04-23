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

router.get("/today", function (req, res) {
    request.filterByDate(new Date().toISOString().slice(0, 10)).then((data) => {
        res.render("index", { view: "today", data: data });
    });
});

router.post("/report/:id", function(req, res){
    req.body.report = req.body.report.replace(/\r/g, "");
    request
        .writeReport(req.params.id, req.body.report)
        .then(() => {
            axios
                .put(`http://localhost:3000/api/requests/${req.params.id}`, { report: req.body.report })
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit report to service 1", error: error });
                });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit report", error: error });
        });
})
router.post("/cancel/:id", function (req, res) {
    request
        .updateStatus(req.params.id, "canceled")
        .then(() => {
            axios
                .put(`http://localhost:3000/api/requests/${req.params.id}`, { status: "canceled" })
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit new request to service 1", error: error });
                });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

router.post("/complete/:id", function (req, res) {
    request
        .updateStatus(req.params.id, "completed")
        .then(() => {
            axios
                .put(`http://localhost:3000/api/requests/${req.params.id}`, { status: "completed" })
                .then(() => {
                    res.redirect("/");
                })
                .catch((error) => {
                    res.render("error", { message: "Failed to submit new request to service 1", error: error });
                });
        })
        .catch((error) => {
            res.render("error", { message: "Failed to submit new request", error: error });
        });
});

module.exports = router;
