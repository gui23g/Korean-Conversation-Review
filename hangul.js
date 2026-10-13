(function(root){
'use strict';
const L=Array.from('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ');
const V=Array.from('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ');
const T=['',...Array.from('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')];
const vowelPairs={'ㅗㅏ':'ㅘ','ㅗㅐ':'ㅙ','ㅗㅣ':'ㅚ','ㅜㅓ':'ㅝ','ㅜㅔ':'ㅞ','ㅜㅣ':'ㅟ','ㅡㅣ':'ㅢ','ㅘㅣ':'ㅙ','ㅝㅣ':'ㅞ'};
const finalPairs={'ㄱㅅ':'ㄳ','ㄴㅈ':'ㄵ','ㄴㅎ':'ㄶ','ㄹㄱ':'ㄺ','ㄹㅁ':'ㄻ','ㄹㅂ':'ㄼ','ㄹㅅ':'ㄽ','ㄹㅌ':'ㄾ','ㄹㅍ':'ㄿ','ㄹㅎ':'ㅀ','ㅂㅅ':'ㅄ'};
const splitFinal=Object.fromEntries(Object.entries(finalPairs).map(([k,v])=>[v,Array.from(k)]));
const splitVowel={'ㅘ':['ㅗ','ㅏ'],'ㅙ':['ㅗ','ㅐ'],'ㅚ':['ㅗ','ㅣ'],'ㅝ':['ㅜ','ㅓ'],'ㅞ':['ㅜ','ㅔ'],'ㅟ':['ㅜ','ㅣ'],'ㅢ':['ㅡ','ㅣ']};
function syllable(l,v,t=''){return String.fromCharCode(0xac00+(L.indexOf(l)*21+V.indexOf(v))*28+T.indexOf(t));}
function parts(ch){const n=ch.charCodeAt(0)-0xac00;return n>=0&&n<11172?[L[Math.floor(n/588)],V[Math.floor(n/28)%21],T[n%28]]:null;}
function decompose(text){return Array.from(text.normalize('NFC')).map(ch=>{const p=parts(ch);if(!p)return ch;return p[0]+(splitVowel[p[1]]||[p[1]]).join('')+(splitFinal[p[2]]||[p[2]]).join('');}).join('');}
function compose(text){let out=[];for(const ch of Array.from(text)){
 const prev=out.at(-1),p=prev?parts(prev):null;
 if(V.includes(ch)){
  if(p){if(p[2]){const pair=splitFinal[p[2]],moving=pair?pair[1]:p[2],remain=pair?pair[0]:'';if(L.includes(moving)){out[out.length-1]=syllable(p[0],p[1],remain);out.push(syllable(moving,ch));}else out.push(ch);}
   else if(vowelPairs[p[1]+ch])out[out.length-1]=syllable(p[0],vowelPairs[p[1]+ch]);else out.push(ch);
  }else if(L.includes(prev))out[out.length-1]=syllable(prev,ch);else if(vowelPairs[(prev||'')+ch])out[out.length-1]=vowelPairs[prev+ch];else out.push(ch);
 }else if(L.includes(ch)){
  if(p&&!p[2]&&T.includes(ch))out[out.length-1]=syllable(p[0],p[1],ch);
  else if(p&&p[2]&&finalPairs[p[2]+ch])out[out.length-1]=syllable(p[0],p[1],finalPairs[p[2]+ch]);else out.push(ch);
 }else out.push(ch);
}return out.join('');}
function insert(value,start,end,key,literal=false){const prefix=value.slice(0,start),suffix=value.slice(end);const left=literal?prefix+key:compose(decompose(prefix)+key);return {value:left+suffix,cursor:left.length};}
function backspace(value,start,end,literal=false){if(start!==end)return {value:value.slice(0,start)+value.slice(end),cursor:start};if(!start)return {value,cursor:start};const prefix=value.slice(0,start);const left=literal?Array.from(prefix).slice(0,-1).join(''):compose(Array.from(decompose(prefix)).slice(0,-1).join(''));return {value:left+value.slice(end),cursor:left.length};}
function normalize(text){return text.normalize('NFC').replace(/[\s.,!?。？！·]/g,'').trim();}
const api={compose,decompose,insert,backspace,normalize,parts};if(typeof module!=='undefined')module.exports=api;root.Hangul=api;
})(typeof window!=='undefined'?window:globalThis);
