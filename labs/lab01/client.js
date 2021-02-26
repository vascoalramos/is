const net = require("net");

const client = new net.Socket();

client.connect(1337, "0.0.0.0", function () {
    console.log("Connected");
    client.write("Hello, server! Love, Client.");
    client.end();
});

client.on("data", (data) => {
    console.log("Received: " + data);
});

client.on("close", () => {
    console.log("Connection closed");
});

client.on("error", (err) => {
    console.error(err);
});
