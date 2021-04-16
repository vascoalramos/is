const env = process.env;

const config = {
    db: {
        host: env.DB_HOST || "localhost",
        user: env.DB_USER || "service1",
        password: env.DB_PASSWORD || "svc1",
        database: env.DB_NAME || "medical_exams",
    },
};

module.exports = config;
