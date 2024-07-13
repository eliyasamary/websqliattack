const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: process.env.DB_PASSWORD || "password",
  database: "webA",
  port: 3306,
});

db.connect((err) => {
  if (err) {
    console.log(err);
  } else {
    console.log("Database connected");
  }
});

const getUsers = (callback) => {
  db.query("SELECT * FROM users;", (err, result) => {
    if (err) {
      callback(err, null);
      return;
    }
    callback(null, result);
  });
};

const login = (user_name, password, callback) => {
  const query = "SELECT * FROM users WHERE user_name = ? AND password = ?";
  db.execute(query, [user_name, password], (err, result) => {
    if (err) {
      callback(err, null);
      return;
    }
    callback(null, result);
  });
};

module.exports = {
  getUsers,
  login,
};