import { chromium } from 'playwright-core';
import fs from 'node:fs/promises';
import path from 'node:path';
const out=path.dirname(new URL(import.meta.url).pathname), report=path.resolve(out,'../report.html');
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const results={generatedAt:new Date().toISOString(),browser:browser.version(),checks:[],consoleErrors:[]};
for(const [name,width,height] of [['desktop',1280,1000],['mobile',390,844],['narrow',320,740]]){
 const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1});const page=await context.newPage();
 page.on('pageerror',e=>results.consoleErrors.push(String(e))); await page.goto('file://'+report); await page.screenshot({path:path.join(out,name+'-collapsed.png'),fullPage:true});
 const collapsed=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h1,h2')].filter(e=>e.checkVisibility()).map(e=>e.innerText),mainWords:[...document.querySelector('main').children].filter(e=>!e.classList.contains('detail-intro')&&e.tagName!=='FOOTER').map(e=>e.innerText).join(' ').split(/\s+/).length,details:[...document.querySelectorAll('details')].length,scripts:document.scripts.length,networkAssets:[...document.querySelectorAll('[src],link[rel=stylesheet]')].map(e=>e.getAttribute('src')||e.getAttribute('href'))}));
 await page.locator('summary').first().click(); const opened=await page.locator('details').first().getAttribute('open'); await page.locator('summary').first().click();
 await page.evaluate(()=>document.querySelectorAll('details').forEach(x=>x.open=true)); await page.screenshot({path:path.join(out,name+'-expanded.png'),fullPage:true});
 const expanded=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,overflowingElements:[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1 && getComputedStyle(e).position!=='fixed').map(e=>({tag:e.tagName,text:e.innerText?.slice(0,60),width:e.getBoundingClientRect().width})).slice(0,25)}));
 results.checks.push({name,collapsed,summaryClickOpens:opened!==null,expanded});
 if(name==='desktop'){
  await page.evaluate(()=>document.querySelectorAll('details').forEach(x=>x.open=false));await page.emulateMedia({media:'print'});
  results.print=await page.evaluate(()=>({visibleDetailBodies:[...document.querySelectorAll('.detail-body')].filter(e=>e.checkVisibility({contentVisibilityAuto:true})).length,expected:document.querySelectorAll('.detail-body').length,contentVisibility:[...document.querySelectorAll('details')].map(e=>getComputedStyle(e,'::details-content').contentVisibility)}));
  await page.pdf({path:path.join(out,'print.pdf'),format:'A4',printBackground:true,margin:{top:'14mm',bottom:'14mm',left:'12mm',right:'12mm'}});
 }
 await context.close();
}
const content=await fs.readFile(report,'utf8'); const hrefs=[...content.matchAll(/href="([^"]+)"/g)].map(x=>x[1]); const local=hrefs.filter(x=>!x.startsWith('https:')&&!x.startsWith('#')); const missing=[];for(const h of local){if(h==='rendering/checks.json')continue;try{await fs.access(path.resolve(path.dirname(report),h));}catch{missing.push(h);}}
const ids=[...content.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);results.links={total:hrefs.length,missingLocal:missing,duplicateIds:ids.filter((id,i)=>ids.indexOf(id)!==i)};
results.diagram={figures:0,reason:'No chart or relationship diagram needed; simple metric totals chosen under diagram-design simpler-format guidance.',palette:'Default dark semantic tokens; Arial/Georgia/monospace system fallbacks; no remote fonts.'};
await fs.writeFile(path.join(out,'checks.json'),JSON.stringify(results,null,2));await browser.close();console.log(JSON.stringify(results,null,2));
