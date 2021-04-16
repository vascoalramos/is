var express = require("express");
var router = express.Router();

const patient = require("../../controllers/patient");

/* GET home page. */
router.get("/", function (req, res) {
    patient.list().then((data) => {
        res.render("index", { title: "Express", data: data });
    });
});

module.exports = router;
