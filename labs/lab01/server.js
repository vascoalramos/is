const net = require("net");
const mysql = require("mysql");

const server = net.createServer();

const con = mysql.createConnection({
    host: "localhost",
    user: "vr",
    password: "password",
    database: "medical_exams",
});

con.connect(function (err) {
    if (err) throw err;
    console.log("Connected!");
});

server.on("connection", (socket) => {
    con.query("SELECT 1 + 1 AS solution", function (error, results, fields) {
        if (error) throw error;
        console.log("The solution is: ", results[0].solution);
    });
    socket.write("Echo server\r\n");
    socket.end();
});

server.on("data", (data) => {
    console.log("Received: " + data);
});

server.on("close", () => {
    console.log("Server closed");
});

server.on("error", (err) => {
    console.error(err);
});

server.listen(1337, "0.0.0.0");
