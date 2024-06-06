const mysql = require("mysql");

const db = mysql.createConnection({
  host: "",
  user: "",
  password: "",
  database: "",
});

db.connect((err) => {
  if (err) {
    console.log(err);
  } else {
    console.log("Database connected");
  }
});

const getUsers = (callback) => {
  db.query("SELECT * FROM users", (err, result) => {
    if (err) {
      callback(err, null);
      return;
    }
    callback(null, result);
  });
};

module.exports = {
  getUsers,
};
