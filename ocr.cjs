const {createWorker}=require('C:/Users/Inteli/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/tesseract.js');
const fs=require('fs');
(async()=>{const w=await createWorker('kor+eng',1,{cachePath:__dirname+'/tmp',langPath:__dirname+'/tmp',gzip:false}); for(const f of fs.readdirSync(__dirname+'/tmp').filter(x=>/^page-.*jpg$/.test(x)).sort()){const out=__dirname+'/tmp/'+f+'.txt'; if(fs.existsSync(out))continue; const r=await w.recognize(__dirname+'/tmp/'+f); fs.writeFileSync(out,r.data.text); console.log(f);} await w.terminate();})();

