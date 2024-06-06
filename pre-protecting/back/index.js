const port = 8080;
// const db = require('./db');
const morgan = require('morgan');
const cors = require('cors');
const express = require('express');
const app = express();

app.use(morgan('dev'));
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello world');
    }
);

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'admin' && password === 'admin') {
        res.send('Login success');
    } else {
        res.send('Login failed');
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
