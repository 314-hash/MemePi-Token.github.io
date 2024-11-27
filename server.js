const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());

// Serve static files from the docs directory
app.use(express.static(path.join(__dirname, 'docs')));

// Serve index.html for the root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'docs', 'index.html'));
});

// API routes can be added here
app.get('/api/tokenomics', (req, res) => {
    res.json({
        totalSupply: '314,159,265,359',
        burnRate: '2%',
        governanceWeight: 'Square root of holding time',
        transactionCooldown: '314 seconds'
    });
});

// Handle all other routes by serving index.html (for SPA)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'docs', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`
    🚀 MemePi Token Server running!
    
    Main Landing Page: http://localhost:${PORT}
    API Endpoint: http://localhost:${PORT}/api/tokenomics
    
    Ready to explore mathematical tokenomics!
    Press Ctrl+C to stop the server
    `);
});
