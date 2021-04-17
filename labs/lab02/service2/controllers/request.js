const db = require("../db");

module.exports.list = () => {
    return db.query(
        "SELECT id, request_id as request_number, date, hour, episode_number, status, info, report, work.patient_id, patient_number, patient_name, patient_address, patient_phone_number FROM work JOIN patient ON work.patient_id = patient.patient_id",
    );
};

module.exports.get = (reqId) => {
    return db.query("SELECT * FROM work WHERE id=?", [reqId]);
};

module.exports.insert = (request) => {
    return db.query(
        "INSERT INTO work (request_id, date, hour, patient_id, episode_number, info) VALUES (?, ?, ?, ?, ?, ?)",
        [request.request_id, request.date, request.hour, request.patient_id, request.episode_number, request.info],
    );
};

module.exports.getStatus = (reqId) => {
    return db.query("SELECT status FROM work WHERE id=?", [reqId]);
};

module.exports.updateStatus = (reqId, status) => {
    return db.query("UPDATE work SET status=? WHERE id=?", [status, reqId]);
};

module.exports.writeReport = (reqId, report) => {
    return db.query("UPDATE work SET report=? WHERE id=?", [report, reqId]);
};
