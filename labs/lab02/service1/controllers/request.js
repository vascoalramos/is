const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM request");
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
    return db.query("SELECT status FROM work WHERE id=?", [reqId]);
};

module.exports.cancel = (reqId) => {
    return db.query("UPDATE work SET status='canceled' WHERE id=?", [reqId]);
};

module.exports.complete = (reqId) => {
    return db.query("UPDATE work SET status='canceled' WHERE id=?", [reqId]);
};

module.exports.writeReport = (reqId, report) => {
    return db.query("UPDATE work SET report='?' WHERE id=?", [report, reqId]);
};
