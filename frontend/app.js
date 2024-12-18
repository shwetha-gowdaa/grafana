const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    axios.get('http://backend:5000/api/data')
        .then(response => {
            res.json(response.data);
        })
        .catch(error => {
            res.status(500).send(error.message);
        });
});

app.listen(port, () => {
    console.log(`Frontend app listening at http://localhost:${port}`);
});
