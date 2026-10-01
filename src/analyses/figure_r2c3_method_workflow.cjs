/* Editable SVG master and PNG rendered directly from that master.
 * Run with Node and sharp installed (or NODE_PATH pointing to bundled modules).
 * No empirical data or manuscript files are modified.
 */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const sharp = require('sharp');
const out = path.resolve(__dirname, '../../data/exp/r2c3_method_workflow');
fs.mkdirSync(out, {recursive: true});
const svgPath = path.join(out, 'Figure_methodological_workflow.svg');
const pngPath = path.join(out, 'Figure_methodological_workflow.png');
const esc = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;');
const inner = (x,y,w,h,lines) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7" fill="white" stroke="#91a3af" stroke-width="1.5"/>` + lines.map((t,i)=>`<text x="${x+w/2}" y="${y+h/2-(lines.length-1)*16+9+i*32}">${esc(t)}</text>`).join('');
const down = (x,y1,y2) => `<path class="arrow" d="M${x} ${y1} V${y2} M${x-6} ${y2-9} L${x} ${y2} L${x+6} ${y2-9}"/>`;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800">
<title>Methodological workflow for two-stage emergency medical access</title>
<desc>Three grouped frames contain connected process boxes.</desc>
<style>text{font-family:Arial,Helvetica,sans-serif;fill:#243747;font-size:25px;text-anchor:middle}.heading{font-weight:700;font-size:31px}.small{font-size:23px}.arrow{fill:none;stroke:#526878;stroke-width:2.5}</style>
<rect width="1200" height="800" fill="white"/>
<rect x="25" y="20" width="1150" height="205" rx="14" fill="#f1f5f8" stroke="#6b8193" stroke-width="2"/>
<text class="heading" x="600" y="66">Network and baseline</text>
${inner(50,95,325,100,['Roads and population','Dispatch bases','Hospitals'])}
${inner(435,95,305,100,['Junction-to-junction','road network'])}
${inner(800,95,350,100,['Baseline two-stage routing','Base → patient → hospital'])}
<path class="arrow" d="M375 145 H435 M426 139 L435 145 L426 151 M740 145 H800 M791 139 L800 145 L791 151"/>
<path class="arrow" d="M975 195 V255 H305 V290 M975 255 H895 V290 M299 281 L305 290 L311 281 M889 281 L895 290 L901 281"/>
<rect x="25" y="290" width="560" height="485" rx="14" fill="#eef6fb" stroke="#377b9c" stroke-width="2"/>
<rect x="615" y="290" width="560" height="485" rx="14" fill="#fbf5eb" stroke="#a37c41" stroke-width="2"/>
<text class="heading" x="305" y="335">Random-failure reliability</text>
<text class="heading" x="895" y="335">Single-section consequence</text>
${inner(55,360,500,65,['Length-dependent road failures'])}
${down(305,425,455)}
${inner(55,455,500,65,['Paired simulations and rerouting'])}
${down(305,520,550)}
${inner(55,550,500,80,['Grid, population and','hospital reliability'])}
${down(305,630,660)}
${inner(55,660,500,80,['Convergence and speed sensitivity'])}
${inner(645,360,500,65,['Remove each section from baseline'])}
${down(895,425,455)}
${inner(645,455,500,65,['Reroute and measure access loss'])}
${down(895,520,550)}
${inner(645,550,500,80,['Map consequence and expected risk'])}
<text class="small" x="895" y="693">Expected risk = potential loss ×</text>
<text class="small" x="895" y="725">section failure probability</text>
</svg>`;
fs.writeFileSync(svgPath,svg);
(async()=>{
  await sharp(Buffer.from(svg),{density:216}).resize(3600,2400).png().withMetadata({density:600}).toFile(pngPath);
  const metadata=await sharp(pngPath).metadata();
  if(metadata.width!==3600 || metadata.height!==2400 || metadata.density!==600) throw Error('Unexpected dimensions or DPI');
  await sharp(pngPath).resize(1200).png().toFile(path.join(out,'preview.png'));
  const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
  fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify({svg_sha256:hash(svgPath),png_sha256:hash(pngPath),width:metadata.width,height:metadata.height,dpi:metadata.density,svg_text_editable:true,rendered_from_svg:true,model_changed:false},null,2)+'\n');
  console.log(JSON.stringify({svgPath,pngPath,width:metadata.width,height:metadata.height,dpi:metadata.density}));
})().catch(e=>{console.error(e);process.exit(1);});
