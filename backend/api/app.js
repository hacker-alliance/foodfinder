const express = require('express');
const { Spanner } = require('@google-cloud/spanner');

const app = express();

const spannerClient = new Spanner({ projectId: process.env.Spanner_Project });

const spannerInstance = spannerClient.instance(process.env.Spanner_Instance);
const spannerDatabase = spannerInstance.database(process.env.Spanner_Database);

const query = {
  sql: 'SELECT * FROM location',
};

function defaultRoute(req, res) {
  res.send(req.path);
}

async function distributorsRoute(req, res) {
  const [rows] = await spannerDatabase.run(query);
  res.send(rows);
}

app.use('/distributors', distributorsRoute);
app.use(defaultRoute);

exports.handler = app;
