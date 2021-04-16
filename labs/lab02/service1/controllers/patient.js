const db = require("../db");

module.exports.list = () => {
    return db.query("SELECT * FROM request");
};
