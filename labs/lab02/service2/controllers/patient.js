const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM patient");
};

module.exports.getPatientByNumber = (number) => {
    return db.query("SELECT patient_id FROM patient WHERE patient_number=?", [number]);
};

module.exports.insert = (patient) => {
    return db.query(
        "INSERT INTO patient (patient_number, patient_name, patient_address, patient_phone_number) VALUES (?, ?, ?, ?)",
        [patient.number, patient.name, patient.address, patient.phone_number],
    );
};
