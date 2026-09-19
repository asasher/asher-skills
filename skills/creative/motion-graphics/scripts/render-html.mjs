#!/usr/bin/env node
// Capture a seekable local HTML scene at exact frame times, then encode it.
import { createRequire } from 'node:module';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { mkdtemp, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { spawn } from 'node:child_process';

const [input, output, w, h, rate, seconds] = process.argv.slice(2);
const width = Number(w), height = Number(h), fps = Number(rate), duration = Number(seconds);
if (!input || !output || ![width,height].every(n=>Number.isInteger(n)&&n>0&&n%2===0) || !Number.isFinite(fps) || fps<=0 || !Number.isFinite(duration) || duration<=0) {
  throw new Error('Usage: render-html.mjs scene.html clip.mp4 WIDTH HEIGHT FPS SECONDS (positive even dimensions)');
}
try { await access(resolve(output)); throw new Error(`Output already exists: ${output}`); }
catch (e) { if (e.code !== 'ENOENT') throw e; }
const require = createRequire(resolve(process.cwd(), 'package.json'));
const { chromium } = require('playwright');
const frames = Math.ceil(fps * duration);
const temp = await mkdtemp(join(tmpdir(), 'motion-frames-'));
let browser;
try {
  browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
  const page = await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(resolve(input)).href, {waitUntil:'networkidle'});
  await page.evaluate(async()=>{
    await document.fonts.ready;
    await Promise.all([...document.images].map(image=>image.decode()));
    if(typeof window.renderFrame!=='function') throw new Error('Scene must expose window.renderFrame(seconds)');
  });
  for(let n=0;n<frames;n++) {
    await page.evaluate(async time=>{await window.renderFrame(time);}, n/fps);
    if (errors.length) throw new Error(errors.join('\n'));
    const overflow = await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth||document.documentElement.scrollHeight>innerHeight);
    if (overflow) throw new Error(`Scene exceeds canvas at frame ${n}`);
    await page.screenshot({path:join(temp,`${String(n).padStart(7,'0')}.png`),animations:'allow'});
  }
  await browser.close();browser=null;
  await new Promise((ok,fail)=>{
    const proc=spawn('ffmpeg',['-v','error','-n','-framerate',String(fps),'-i',join(temp,'%07d.png'),'-frames:v',String(frames),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',resolve(output)],{stdio:'inherit'});
    proc.on('error',fail);proc.on('exit',code=>code===0?ok():fail(new Error(`ffmpeg exited ${code}`)));
  });
  console.log(JSON.stringify({output:resolve(output),width,height,fps,frames,duration:frames/fps,audio:false}));
} finally {
  if(browser) await browser.close();
  await rm(temp,{recursive:true,force:true});
}
