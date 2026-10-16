const React=require('react'); const RDS=require('react-dom/server'); const tb=require('react-icons/tb');
const out={};
for (const n of Object.keys(tb)) { if(!/^Tb[A-Z]/.test(n) || n.includes('Filled')) continue; }
const names=process.argv.slice(2);
for (const n of names){ out[n]=RDS.renderToStaticMarkup(React.createElement(tb[n],{size:24})); }
require('fs').writeFileSync('icons.json',JSON.stringify(out));
console.log(Object.keys(out).length, out[names[0]].slice(0,200));
