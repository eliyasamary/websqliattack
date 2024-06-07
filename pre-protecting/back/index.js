require("dotenv").config();
const port = 8080;
const db = require("./db");
const morgan = require("morgan");
const cors = require("cors");
const express = require("express");
const app = express();

app.use(morgan("dev"));
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Hello world");
});

app.post("/login", (req, res) => {
  const { userName, password } = req.body;
  console.log("userName:", userName);
  console.log("password:", password);

  db.login(userName, password, (err, result) => {
    if (err) {
      console.log("Error:", err);
      res.status(500).send("Login failed");
      return;
    }

    if (result.length === 0) {
      console.log("Login failed");
      res.status(401).send("Login failed");
      return;
    }

    console.log("Login successful");
    res.send({text:"Login successful",
        data: result
    });
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
