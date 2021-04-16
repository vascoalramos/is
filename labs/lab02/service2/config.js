const env = process.env;

const config = {
    db: {
        host: env.DB_HOST || "localhost",
        user: env.DB_USER || "service2",
        password: env.DB_PASSWORD || "svc2",
        database: env.DB_NAME || "medical_work_list",
    },
};

module.exports = config;
