const db = require("../db");

module.exports.list = () => {
    return db.query(
        "SELECT request.number AS number, date, hour, episode_number, status, info, report, patient_id, patient.number AS patient_number, name AS patient_name, address AS patient_address, phone_number AS patient_phone_number FROM request JOIN patient ON patient_id = patient.id",
    );
};

module.exports.get = (reqId) => {
    return db.query("SELECT * FROM request WHERE number=?", [reqId]);
};

module.exports.insert = (request) => {
    return db.query("INSERT INTO request (date, hour, patient_id, episode_number, info) VALUES (?, ?, ?, ?, ?)", [
        request.date,
        request.hour,
        request.patient_id,
        request.episode_number,
        request.info,
    ]);
};

module.exports.getStatus = (reqId) => {
    return db.query("SELECT status FROM request WHERE number=?", [reqId]);
};

module.exports.updateStatus = (reqId, status) => {
    return db.query("UPDATE request SET status=? WHERE number=?", [status, reqId]);
};

module.exports.writeReport = (reqId, report) => {
    return db.query("UPDATE request SET report=? WHERE number=?", [report, reqId]);
};
