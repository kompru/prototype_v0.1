const express = require('express');
const { google } = require('googleapis');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const config = require('./config');

// Initialize Express
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Use the service account credentials from config.js
const { client_email, private_key } = config;

// Initialize Google Auth Client using service account credentials
const auth = new google.auth.GoogleAuth({
  credentials: {
    client_email,
    private_key,
  },
  scopes: ['https://www.googleapis.com/auth/spreadsheets'],
});

// Initialize Google Sheets API
const sheets = google.sheets({ version: 'v4', auth });

// New endpoint to get Google Maps API Key
app.get('/get-google-maps-key', (req, res) => {
  const { googleMapsApiKey } = config;
  res.json({ googleMapsApiKey });
});

// Endpoint to save text
app.post('/save-text', async (req, res) => {
  console.log('Saving text...');
  const text = req.body.text;

  try {
    await saveTextToSheet(text, sheets, config.spreadsheetId, 'Sheet1');
    res.json({ message: 'Text saved' });
  } catch (error) {
    console.error(error);
    res.json({ message: 'Failed to save text' });
  }
});

// Marked Change: New endpoint to save product
app.post('/save-product', async (req, res) => {
  console.log('Saving product...');
  const product = req.body.product;

  try {
    await saveTextToSheet(product, sheets, config.spreadsheetId, 'Products'); // Save to 'Products' tab
    res.json({ message: 'Product saved' });
  } catch (error) {
    console.error(error);
    res.json({ message: 'Failed to save product' });
  }
});

// Save Text to Google Sheet
async function saveTextToSheet(text, sheetsAPI, spreadsheetId, sheetName) {
  const values = [[text]];

  // Append data to Google Sheet
  await sheetsAPI.spreadsheets.values.append({
    spreadsheetId,
    range: `${sheetName}!A:A`,
    valueInputOption: 'RAW',
    resource: { values }
  });
}

// Start the server
app.listen(3000, () => {
  console.log('Server running on https://18.223.171.150:3000');
});
