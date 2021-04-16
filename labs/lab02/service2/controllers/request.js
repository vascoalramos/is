const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM request");
};

module.exports.insert = (request) => {
    return db.query(
        "INSERT INTO work (request_id, date, hour, patient_id, episode_number, info) VALUES (?, ?, ?, ?, ?, ?)",
        [request.request_id, request.date, request.hour, request.patient_id, request.episode_number, request.info],
    );
};

module.exports.getStatus = (reqId) => {
    return db.query("SELECT status FROM work WHERE request_id=?", [reqId]);
};

module.exports.updateStatus = (reqId, status) => {
    return db.query("UPDATE work SET status=? WHERE request_id=?", [status, reqId]);
};

module.exports.writeReport = (reqId, report) => {
    return db.query("UPDATE work SET report=? WHERE request_id=?", [report, reqId]);
};
