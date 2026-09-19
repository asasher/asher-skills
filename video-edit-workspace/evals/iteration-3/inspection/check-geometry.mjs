import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs';
const root='/Users/asher/Projects/random/obs-sep19-short';
const {chromium}=createRequire(root+'/package.json')('playwright');
const T=JSON.parse(fs.readFileSync(root+'/output/project/timeline.json','utf8'));
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
 const page=await browser.newPage({viewport:{width:1080,height:1920}});
 await page.goto(pathToFileURL(root+'/output/project/scene.html').href+'?preview=1');
 await page.evaluate(()=>document.fonts.ready);
 const result=await page.evaluate(T=>{
  const errors=[],region={left:120,top:288,right:780,bottom:1248};let tested=0;
  const selector='svg > text:not(#chapter), #screen text, #screen image, #risk text, #risk rect, #risk path, #flow text, #flow rect, #flow path, #previewCaption rect, #previewCaption text';
  for(let frame=0;frame<T.frames;frame++){
   window.renderFrame(frame/T.fps);
   for(const e of document.querySelectorAll(selector)){
    let opacity=1,visible=true;
    for(let n=e;n&&n instanceof Element;n=n.parentElement){const s=getComputedStyle(n);opacity*=Number(s.opacity);if(s.display==='none'||s.visibility==='hidden')visible=false;}
    if(!visible||opacity<.01)continue;
    const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;
    const s=getComputedStyle(e),pad=s.stroke!=='none'?parseFloat(s.strokeWidth)/2:0;
    const b={left:r.left-pad,top:r.top-pad,right:r.right+pad,bottom:r.bottom+pad};tested++;
    if(b.left<region.left-.1||b.top<region.top-.1||b.right>region.right+.1||b.bottom>region.bottom+.1){errors.push({frame,time:frame/T.fps,element:e.id||e.textContent||e.tagName,bounds:b});}
   }
  }
  return{frames:T.frames,fps:T.fps,tested_visible_elements:tested,region,errors,pass:errors.length===0,limits:'Checks authored scene geometry including preview caption plates. Real footage, actual libass rasterization, and organic app UI require separate inspection.'};
 },T);
 fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,errors:result.errors.slice(0,5)}));
}finally{await browser.close()}
