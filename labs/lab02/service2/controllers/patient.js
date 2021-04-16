const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM patient");
};

module.exports.insert = (patient) => {
    return db.query(
        "INSERT INTO patient (patient_number, patient_name, patient_address, patient_phone_number) VALUES (?, ?, ?, ?)",
        [patient.number, patient.name, patient.address, patient.phone_number],
    );
};
