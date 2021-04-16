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
