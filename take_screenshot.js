const puppeteer = require('puppeteer-core');
const http = require('http');
const fs = require('fs');

const filename = process.argv[2];

http.get('http://127.0.0.1:9222/json', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', async () => {
        const pages = JSON.parse(data);
        const awsPage = pages.find(p => p.url.includes('aws.amazon.com') && p.type === 'page');
        if (!awsPage) {
            console.error("AWS page not found");
            process.exit(1);
        }
        const browser = await puppeteer.connect({ browserWSEndpoint: awsPage.webSocketDebuggerUrl });
        const pagesList = await browser.pages();
        const page = pagesList.find(p => p.url() === awsPage.url) || pagesList[0];
        
        await page.screenshot({ path: filename });
        await browser.disconnect();
        console.log("Screenshot saved to " + filename);
    });
}).on('error', (err) => {
    console.error(err);
    process.exit(1);
});
