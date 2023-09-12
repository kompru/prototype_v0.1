const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const config = require('./config');
const ip = require('ip');
const path = require('path');
const ExcelJS = require('exceljs');  // Marked Change: Add ExcelJS

// Initialize Express
const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get('/server-ip', (req, res) => {
  res.send(ip.address());
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Restore: Endpoint to get Google Maps API Key
app.get('/get-google-maps-key', (req, res) => {
  const { googleMapsApiKey } = config;
  res.json({ googleMapsApiKey });
});

// Endpoint to save text
app.post('/save-text', async (req, res) => {
  console.log('Saving text...');
  const text = req.body.text;

  try {
    await appendToExcelSheet(text, 'Sheet1'); // Marked Change: Append to Excel
    res.json({ message: 'Text saved' });
  } catch (error) {
    console.error('Error saving text:', error);
    res.status(500).json({ message: 'Failed to save text', error: error.message });
  }
});

// Endpoint to save product
app.post('/save-product', async (req, res) => {
  console.log('Saving text...');
  const product = req.body.product;

  try {
    await appendToExcelSheet(product, 'Sheet2'); // Marked Change: Append to Excel
    res.json({ message: 'Text saved' });
  } catch (error) {
    console.error('Error saving text:', error);
    res.status(500).json({ message: 'Failed to save text', error: error.message });
  }
});

async function appendToExcelSheet(text, tabName) {
  const workbook = new ExcelJS.Workbook();
  
  // Reading the existing Excel file
  await workbook.xlsx.readFile('./Workbook.xlsx');
  
  // Get the tab (worksheet) by its name, or add it if it doesn't exist
  let worksheet = workbook.getWorksheet(tabName);
  if (!worksheet) {
    worksheet = workbook.addWorksheet(tabName);
  }
  
  // Append the new row
  worksheet.addRow([text]);
  
  // Write the Excel file back to disk
  await workbook.xlsx.writeFile('./Workbook.xlsx');
}

// Start the server
app.listen(3000, () => {
  console.log(`Server running on http://${ip.address()}:3000`);
});
