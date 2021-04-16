const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM patient");
};

module.exports.insert = (patient) => {
    return db.query("INSERT INTO patient (number, name, address, phone_number) VALUES (?, ?, ?, ?)", [
        patient.number,
        patient.name,
        patient.address,
        patient.phone_number,
    ]);
};
