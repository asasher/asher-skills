import {chromium} from 'playwright-core';
const started=performance.now();const browser=await chromium.launch({channel:'chrome',headless:true});const launchMs=performance.now()-started;const page=await browser.newPage({viewport:{width:1280,height:800}});const results=[];
for(const [host,url] of [['local','http://localhost:48765/'],['remote-over-ssh','http://127.0.0.1:48766/']]){
 const t=performance.now();await page.goto(url);await page.getByRole('textbox',{name:'Name'}).fill('Baseline');await page.getByRole('button',{name:'Sign in to test app'}).click();await page.getByRole('status').filter({hasText:'Signed in as Baseline'}).waitFor();const setupMs=performance.now()-t;
 for(let i=0;i<5;i++){const t=performance.now();await page.getByRole('button',{name:'Save change'}).click();await page.waitForFunction(()=>document.querySelector('#result').textContent==='Saved successfully');results.push({host,trial:i+1,ms:Math.round(performance.now()-t)})}
 console.log(JSON.stringify({host,setupMs:Math.round(setupMs)}));
}console.log(JSON.stringify({browser:browser.version(),launchMs:Math.round(launchMs),results}));await browser.close();
