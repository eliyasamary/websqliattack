require("dotenv").config();
const port = 8080;
const db = require("./db");
const morgan = require("morgan");
const cors = require("cors");
const express = require("express");
const helmet = require("helmet");
const { body, validationResult } = require("express-validator");
const app = express();

app.use(helmet());
app.use(morgan("dev"));
app.use(cors());
app.use(express.json());

const validateLogin = [
  body("userName").trim().isString().notEmpty(),
  body("password").trim().isString().notEmpty(),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }
    next();
  },
];

app.get("/", (req, res) => {
  res.send("Hello world");
});

app.post("/login", validateLogin, async (req, res) => {
  const { userName, password } = req.body;
  console.log("userName:", userName);
  console.log("password:", password);

  try {
    const user = db.login(userName, password, (err, result) => {
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
          data: user
      });
    });
  } catch (error) {
    console.log("Error:", error);
    res.status(500).send("Login failed");
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});