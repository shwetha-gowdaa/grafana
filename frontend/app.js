const express = require('express');
const axios = require('axios');
const client = require('prom-client'); // Import prom-client
const app = express();
const port = 3000;

// Create a new counter metric for HTTP requests
const counter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'status']
});

// Setup metrics endpoint for Prometheus to scrape
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// Frontend route
app.get('/', (req, res) => {
  axios.get('http://backend:5000/api/data')
    .then(response => {
      counter.inc({ method: 'GET', status: 200 });
      res.set('X-Source', 'Frontend');
      res.json({
        source: 'frontend',
        backend_data: response.data
      });
    })
    .catch(error => {
      res.set('X-Source', 'Frontend');
      res.status(500).send({
        source: 'frontend',
        error: error.message
      });
    });
});

app.listen(port, () => {
  console.log(`Frontend app listening at http://localhost:${port}`);
});
