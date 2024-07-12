require("dotenv").config();
const port = 8080;
const { User } = require("./db");
const { Sequelize } = require('sequelize');
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

  try {
    const user = await User.findOne({ where: { userName, password } });
    if (!user) {
      console.log("Login failed");
      res.status(401).send("Login failed");
      return;
    }

    console.log("Login successful");
    res.send({
      text: "Login successful",
      data: user,
    });
  } catch (error) {
    console.log("Error:", error);
    res.status(500).send("Login failed");
  }
});
Sequelize.sync().then(() => {
  app.listen(port, () => {
    console.log('Server is running on http://localhost:${port}');
  });
});