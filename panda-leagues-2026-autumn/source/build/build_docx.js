// Build 竞赛规程 + 规则精要 (.docx) for both leagues.
const fs = require('fs'); const path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Header, Footer, PageNumber, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, TableOfContents, PageBreak, VerticalAlign,
  TabStopType, TableLayoutType, HeightRule } = D;
const COMMON = require('./content_common');

const ROOT = path.join(__dirname, '..', 'out');
const VI = path.join(ROOT, '01_VI视觉识别系统', 'assets');
const GEN = path.join(__dirname, 'gen');
const COL = { blue: '04518E', navy: '0B2545', ink: '13202F', slate: '5A6B80', mist: 'E6EEF6', paper: 'F5F8FB', line: 'C9D5E3', gold: 'F2B21B', green: '2FB45A' };
const F_H = { ascii: 'Arial', hAnsi: 'Arial', eastAsia: 'Microsoft YaHei', cs: 'Arial' };
const F_B = { ascii: 'Times New Roman', hAnsi: 'Times New Roman', eastAsia: 'SimSun', cs: 'Times New Roman' };
const MM = 3.7795; // px per mm for ImageRun
const PAGE_W = 11906, ML = 1531, MR = 1531; const CW = PAGE_W - ML - MR; // content width (twips)

const CN = (n) => { const d = '零一二三四五六七八九'; if (n < 10) return d[n]; if (n < 20) return '十' + (n % 10 ? d[n % 10] : ''); return d[Math.floor(n / 10)] + '十' + (n % 10 ? d[n % 10] : ''); };

function runs(text, base = {}) {
  // **bold** markup -> TextRuns
  const out = []; const parts = String(text).split(/(\*\*[^*]+\*\*)/);
  for (const p of parts) {
    if (!p) continue;
    if (p.startsWith('**')) out.push(new TextRun({ text: p.slice(2, -2), bold: true, color: base.boldColor || COL.navy, font: base.font || F_B, size: base.size || 22 }));
    else out.push(new TextRun({ text: p, font: base.font || F_B, size: base.size || 22, color: base.color || COL.ink, bold: base.bold }));
  }
  return out;
}

function para(text, o = {}) {
  let indent = o.indent;
  if (!indent) {
    if (/^[一二三四五六七八九十]+、/.test(text) || /^（[一二三四五六七八九十]+）/.test(text)) indent = { left: 480, hanging: 480 };
    else if (/^\d+\.\s?/.test(text)) indent = { left: 840, hanging: 300 };
    else if (o.noIndent) indent = undefined; else indent = { firstLine: 440 };
  }
  return new Paragraph({ children: runs(text, o), indent, alignment: o.align || AlignmentType.JUSTIFIED,
    spacing: { line: o.line || 340, before: o.before || 0, after: o.after ?? 60 }, keepNext: o.keepNext });
}

const img = (file, wmm, hmm) => new ImageRun({ type: 'png', data: fs.readFileSync(file), transformation: { width: wmm * MM, height: hmm * MM } });
const pngSize = (file) => { const b = fs.readFileSync(file); return [b.readUInt32BE(16), b.readUInt32BE(20)]; };
const imgW = (file, wmm) => { const [w, h] = pngSize(file); return img(file, wmm, wmm * h / w); };

const NB = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const NOB = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };
const LB = (c = COL.line) => ({ style: BorderStyle.SINGLE, size: 4, color: c });

function cell(children, w, o = {}) {
  return new TableCell({ children: Array.isArray(children) ? children : [children], width: { size: w, type: WidthType.DXA },
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined, verticalAlign: o.va || VerticalAlign.CENTER,
    margins: { top: o.mt ?? 80, bottom: o.mb ?? 80, left: o.ml ?? 120, right: o.mr ?? 120 }, borders: o.borders, columnSpan: o.span });
}
const ctext = (t, o = {}) => new Paragraph({ children: runs(t, { size: o.size || 20, font: o.font || F_B, bold: o.bold, color: o.color, boldColor: o.boldColor }), alignment: o.align || AlignmentType.LEFT, spacing: { line: o.line || 300, after: o.after ?? 0, before: 0 } });

function dataTable(head, rows, widths, o = {}) {
  const fillH = o.headFill || COL.blue;
  const tr = [new TableRow({ tableHeader: true, children: head.map((h, i) => cell(ctext(h, { bold: true, color: 'FFFFFF', boldColor: 'FFFFFF', font: F_H, size: 19, align: i ? AlignmentType.CENTER : AlignmentType.LEFT }), widths[i], { fill: fillH })) })];
  rows.forEach((r, ri) => tr.push(new TableRow({ cantSplit: true, children: r.map((c, i) => cell(ctext(c, { size: 19, bold: i === 0 && o.boldFirst, font: i === 0 && o.boldFirst ? F_H : F_B, align: i && o.center ? AlignmentType.CENTER : AlignmentType.LEFT }), widths[i], { fill: ri % 2 ? COL.paper : undefined })) })));
  return new Table({ rows: tr, width: { size: widths.reduce((a, b) => a + b), type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED,
    borders: { top: LB(COL.blue), bottom: LB(COL.blue), left: NB, right: NB, insideHorizontal: LB(), insideVertical: LB('FFFFFF') } });
}

function header(meta, docName) {
  const logo = path.join(VI, 'logo', `panda-logo_${meta.key}.png`);
  return new Header({ children: [new Paragraph({
    children: [img(logo, 8, 8), new TextRun({ text: `  ${meta.cn} · ${meta.season}`, font: F_H, size: 17, color: COL.navy, bold: true }),
      new TextRun({ text: `\t${docName}`, font: F_H, size: 17, color: COL.slate })],
    tabStops: [{ type: TabStopType.RIGHT, position: CW }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COL.blue, space: 4 } }, spacing: { after: 0 } })] });
}
function footer(code) {
  const f = { font: F_H, size: 15, color: COL.slate };
  return new Footer({ children: [new Paragraph({
    tabStops: [{ type: TabStopType.CENTER, position: CW / 2 }, { type: TabStopType.RIGHT, position: CW }],
    children: [new TextRun({ text: `${code} · v1.0`, ...f }), new TextRun({ text: '\t第 ', ...f }), new TextRun({ children: [PageNumber.CURRENT], ...f }),
      new TextRun({ text: ' 页 / 共 ', ...f }), new TextRun({ children: [PageNumber.TOTAL_PAGES], ...f }), new TextRun({ text: ' 页', ...f }),
      new TextRun({ text: `\t${COMMON.ORG.fa}`, ...f })] })] });
}

const STYLES = {
  default: { document: { run: { font: F_B, size: 22, color: COL.ink } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: F_H, size: 30, bold: true, color: COL.blue },
      paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0, keepNext: true,
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: COL.blue, space: 4 } } } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: F_H, size: 23, bold: true, color: COL.navy },
      paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1, keepNext: true } },
    { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', run: { font: F_H, size: 22, bold: true, color: COL.blue }, paragraph: { spacing: { before: 120, after: 40 } } },
    { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', run: { font: F_B, size: 20, color: COL.ink }, paragraph: { indent: { left: 420 }, spacing: { after: 20 } } },
  ],
};
const PAGE = { size: { width: PAGE_W, height: 16838 }, margin: { top: 1531, bottom: 1361, left: ML, right: MR, header: 720, footer: 620 } };

// ---------------------------------------------------------------- regulations
function regDoc(C) {
  const { META, REG } = C;
  // numbering map for {{title}} references
  const num = {}; let n = 0;
  for (const ch of REG) for (const a of ch.arts) num[a.t] = ++n;
  const fix = (s) => s.replace(/\{\{([^}]+)\}\}/g, (_, k) => { if (!num[k]) throw new Error('ref ' + k); return `第${CN(num[k])}条`; });

  // cover
  const lock = path.join(VI, 'lockup', `${META.key}_vertical_positive_2026autumn.png`);
  const infoRows = [['发布单位', `${COMMON.ORG.fa}　${COMMON.ORG.co}`], ['运营管理', `${META.short}赛区组委会`], ['文件编号', `${META.codeReg}`],
    ['版　　本', 'v1.0（基于 2026 春季竞赛规程修订）'], ['发布日期', COMMON.ORG.issued], ['适用范围', `${META.full}全部组别`]];
  const cover = [
    new Paragraph({ children: [imgW(lock, 62)], alignment: AlignmentType.CENTER, spacing: { before: 600, after: 500 } }),
    new Paragraph({ children: [new TextRun({ text: META.full, font: F_H, size: 36, bold: true, color: COL.navy })], alignment: AlignmentType.CENTER, spacing: { after: 160 } }),
    new Paragraph({ children: [new TextRun({ text: '竞 赛 规 程', font: F_H, size: 72, bold: true, color: COL.blue })], alignment: AlignmentType.CENTER, spacing: { after: 80 } }),
    new Paragraph({ children: [new TextRun({ text: 'COMPETITION REGULATIONS', font: F_H, size: 24, bold: true, color: COL.slate, characterSpacing: 60 })], alignment: AlignmentType.CENTER, spacing: { after: 900 } }),
    new Table({ width: { size: 7200, type: WidthType.DXA }, columnWidths: [1700, 5500], alignment: AlignmentType.CENTER, layout: TableLayoutType.FIXED,
      borders: { top: LB(COL.blue), bottom: LB(COL.blue), left: NB, right: NB, insideHorizontal: LB(), insideVertical: NB },
      rows: infoRows.map(([k, v]) => new TableRow({ children: [cell(ctext(k, { font: F_H, bold: true, color: COL.slate, boldColor: COL.slate, size: 19 }), 1700), cell(ctext(v, { size: 19 }), 5500)] })) }),
    new Paragraph({ children: [new TextRun({ text: `${COMMON.ORG.slogan}　·　${COMMON.ORG.sloganEn}`, font: F_H, size: 18, color: COL.blue, bold: true })], alignment: AlignmentType.CENTER, spacing: { before: 900 } }),
  ];

  const body = [
    new Paragraph({ children: [new TextRun({ text: '目　　录', font: F_H, size: 32, bold: true, color: COL.navy })], alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
    new TableOfContents('目录', { hyperlink: true, headingStyleRange: '1-2' }),
    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({ children: [new TextRun({ text: META.full, font: F_H, size: 36, bold: true, color: COL.navy })], alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: '竞赛规程', font: F_H, size: 32, bold: true, color: COL.blue })], alignment: AlignmentType.CENTER, spacing: { after: 240 } }),
  ];
  let k = 0;
  REG.forEach((ch, ci) => {
    body.push(new Paragraph({ text: `第${CN(ci + 1)}章　${ch.ch}`, heading: HeadingLevel.HEADING_1 }));
    for (const a of ch.arts) {
      k++;
      body.push(new Paragraph({ text: `第${CN(k)}条　${a.t}`, heading: HeadingLevel.HEADING_2 }));
      a.p.forEach((s) => body.push(para(fix(s))));
      if (a.table) {
        const t = a.table; const w0 = 1700; const wr = Math.floor((CW - w0) / (t.head.length - 1));
        body.push(dataTable(t.head, t.rows, [w0, ...Array(t.head.length - 1).fill(wr)], { boldFirst: true, center: true }));
        body.push(new Paragraph({ text: '', spacing: { after: 80 } }));
      }
    }
  });
  // appendices
  const appx = (title) => [new Paragraph({ children: [new PageBreak()] }), new Paragraph({ text: title, heading: HeadingLevel.HEADING_1 })];
  // 1 playing time sheet
  body.push(...appx('附件 1　上场时间记录表'));
  body.push(para('本表由各参赛队在每场比赛中如实填写，赛后交比赛监督核查。“上场”栏可填写上场分钟数，或在该节全程上场时打“✓”。守门员栏填写担任守门员的节次。', { noIndent: true }));
  const nRows = META.key === 'elite' ? 16 : 10;
  const info = new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [CW / 4, CW / 4, CW / 4, CW / 4], layout: TableLayoutType.FIXED, borders: NOB,
    rows: [new TableRow({ children: ['比赛日期：', '组别：', '本队：', '对手：'].map((s) => cell(ctext(s, { font: F_H, size: 19 }), CW / 4, { borders: { bottom: LB(COL.slate), top: NB, left: NB, right: NB } })) })] });
  body.push(info, new Paragraph({ text: '', spacing: { after: 100 } }));
  const ws = [800, 1500, 900, 900, 900, 900, 1100, 1100, CW - 8100];
  body.push(dataTable(['号码', '姓名', '第 1 节', '第 2 节', '第 3 节', '第 4 节', '守门员节次', '合计（分钟）', '担任位置'],
    Array.from({ length: nRows }, () => Array(9).fill(' ')), ws, { center: true }));
  body.push(new Paragraph({ children: runs(`教练员签字：________________　　　比赛监督签字：________________`, { font: F_H, size: 20 }), spacing: { before: 400 } }));
  // 2 pitch
  body.push(...appx('附件 2　比赛场地与功能区示意图'));
  if (META.key === 'elite') {
    body.push(new Paragraph({ children: [imgW(path.join(GEN, 'pitch_8v8.png'), 150)], alignment: AlignmentType.CENTER }));
    body.push(para('说明：场地尺寸为参考值，可根据场地条件调整；越位线以场地内第一个五人制场地的边线为标志；中线同时作为球门球退守线；比赛用球放置于场边多球点位。', { noIndent: true, size: 19 }));
  } else {
    body.push(new Paragraph({ children: [imgW(path.join(GEN, 'pitch_youth.png'), 160)], alignment: AlignmentType.CENTER }));
    body.push(para('说明：场地与球门尺寸为参考值，可根据场地条件调整；各组别均以中线为退守线；每块场地均设换人区、家长观赛区（距边线 ≥ 2 m）与场边多球点位。', { noIndent: true, size: 19 }));
  }
  // 3 codes of conduct
  body.push(...appx('附件 3　家长、教练员、球员守则'));
  const codes = [['家长守则', C.PARENT_RULES], ['教练员守则', C.COACH_RULES], ['球员守则', C.PLAYER_RULES]];
  for (const [t, list] of codes) {
    body.push(new Paragraph({ children: runs(t, { font: F_H, size: 23, bold: true, color: COL.navy }), spacing: { before: 200, after: 80 } }));
    list.forEach((s, i) => body.push(para(`${CN(i + 1)}、${s}`)));
  }
  // 4 international refs
  body.push(...appx('附件 4　国际青少年足球实践参照'));
  body.push(para('本规程在制定过程中参照了以下国际足球组织的青少年（U11 及以下）比赛实践，供参赛队、教练员与家长了解相关规则的来由。', { noIndent: true }));
  body.push(dataTable(['参照对象', '主要做法'], COMMON.REFS, [2600, CW - 2600], { boldFirst: true }));

  return new Document({
    creator: COMMON.ORG.fa, title: `${META.full} 竞赛规程`, description: `${META.codeReg} v1.0`, styles: STYLES,
    features: { updateFields: true },
    sections: [
      { properties: { page: PAGE }, children: cover },
      { properties: { page: PAGE }, headers: { default: header(META, '竞赛规程') }, footers: { default: footer(META.codeReg) }, children: body },
    ] });
}

// ---------------------------------------------------------------- summary
function iconRow(icon, title, text, accent) {
  const ic = path.join(GEN, 'icons', `${icon}_FFFFFF.png`);
  return new TableRow({ cantSplit: true, children: [
    cell(new Paragraph({ children: [img(ic, 7, 7)], alignment: AlignmentType.CENTER }), 700, { fill: COL.blue, ml: 60, mr: 60 }),
    cell(ctext(title, { font: F_H, bold: true, size: 21, color: COL.navy, boldColor: COL.navy }), 1900, { fill: COL.paper }),
    cell(ctext(text, { size: 20, line: 300 }), CW - 2600)] });
}
function iconTable(rows) {
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [700, 1900, CW - 2600], layout: TableLayoutType.FIXED,
    borders: { top: LB(COL.blue), bottom: LB(COL.blue), left: NB, right: NB, insideHorizontal: { style: BorderStyle.SINGLE, size: 12, color: 'FFFFFF' }, insideVertical: NB },
    rows: rows.map((r) => iconRow(...r)) });
}
const h1 = (t) => new Paragraph({ text: t, heading: HeadingLevel.HEADING_1 });

function summaryDoc(C) {
  const { META, SUMMARY } = C;
  const lock = path.join(VI, 'lockup', `${META.key}_horizontal_positive_2026autumn.png`);
  const body = [
    new Paragraph({ children: [imgW(lock, 92)], spacing: { after: 200 } }),
    new Paragraph({ children: [new TextRun({ text: '规则精要', font: F_H, size: 52, bold: true, color: COL.blue }), new TextRun({ text: '　比赛守则', font: F_H, size: 32, bold: true, color: COL.navy })], spacing: { after: 40 } }),
    new Paragraph({ children: [new TextRun({ text: 'LAWS OF THE GAME · QUICK GUIDE FOR COACHES & PARENTS', font: F_H, size: 18, bold: true, color: COL.slate, characterSpacing: 30 })], spacing: { after: 240 } }),
  ];
  // letter box
  const letter = SUMMARY.letter.map((s, i) => new Paragraph({ children: runs(s, { size: 20 }), indent: i ? { firstLine: 400 } : undefined, spacing: { line: 320, after: 60 }, alignment: AlignmentType.JUSTIFIED }));
  body.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [CW], borders: NOB, layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: [cell(letter, CW, { fill: COL.mist, mt: 200, mb: 200, ml: 280, mr: 280 })] })] }));

  if (META.key === 'elite') {
    body.push(h1('一、比赛基本信息'));
    const f = SUMMARY.facts; const rows = [];
    for (let i = 0; i < f.length; i += 2) rows.push([f[i][0], f[i][1], f[i + 1][0], f[i + 1][1]]);
    const w = [1300, CW / 2 - 1300, 1300, CW / 2 - 1300];
    body.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: w, layout: TableLayoutType.FIXED,
      borders: { top: LB(COL.blue), bottom: LB(COL.blue), left: NB, right: NB, insideHorizontal: LB(), insideVertical: NB },
      rows: rows.map((r) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(ctext(c, { font: i % 2 ? F_B : F_H, bold: !(i % 2), size: 19, color: i % 2 ? COL.ink : COL.slate, boldColor: COL.slate }), w[i], { fill: i % 2 ? undefined : COL.paper })) })) }));
    body.push(h1('二、特色规则'));
    body.push(iconTable(SUMMARY.rules));
    body.push(h1('三、场地与功能区'));
    body.push(new Paragraph({ children: [imgW(path.join(GEN, 'pitch_8v8.png'), 90)], alignment: AlignmentType.CENTER }));
  } else {
    body.push(h1('一、三个组别一览'));
    const t = C.FORMATS; const w0 = 1600; const wr = Math.floor((CW - w0) / 3);
    body.push(dataTable(t.head, t.rows.filter((r) => !['报名人数'].includes(r[0])), [w0, wr, wr, CW - w0 - 2 * wr], { boldFirst: true, center: true }));
    body.push(h1('二、各组别规则'));
    const gcol = { U6: 'FFC72C', U8: '2FB45A', U10: '1E9BD7' };
    const gw = Math.floor(CW / 3);
    const cols = Object.entries(SUMMARY.groups).map(([g, list]) => [
      new Paragraph({ children: runs(`${g} 组`, { font: F_H, bold: true, size: 26, color: g === 'U6' ? COL.navy : 'FFFFFF' }), spacing: { after: 20 } }),
      new Paragraph({ children: runs(list[0], { font: F_H, size: 17, color: g === 'U6' ? COL.navy : 'FFFFFF' }) })]);
    const bodies = Object.values(SUMMARY.groups).map((list) => list.slice(1).map((s) => new Paragraph({ children: runs('▪ ' + s, { size: 19 }), spacing: { line: 290, after: 60 }, indent: { left: 200, hanging: 200 } })));
    body.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [gw, gw, CW - 2 * gw], layout: TableLayoutType.FIXED,
      borders: { top: NB, bottom: LB(COL.line), left: NB, right: NB, insideHorizontal: NB, insideVertical: { style: BorderStyle.SINGLE, size: 24, color: 'FFFFFF' } },
      rows: [new TableRow({ children: cols.map((c, i) => cell(c, i < 2 ? gw : CW - 2 * gw, { fill: Object.values(gcol)[i] })) }),
        new TableRow({ children: bodies.map((c, i) => cell(c, i < 2 ? gw : CW - 2 * gw, { fill: COL.paper, va: VerticalAlign.TOP, mt: 120 })) })] }));
    body.push(h1('三、通用规则'));
    body.push(iconTable(SUMMARY.general));
    body.push(new Paragraph({ children: [imgW(path.join(GEN, 'pitch_youth.png'), 150)], alignment: AlignmentType.CENTER, spacing: { before: 200 } }));
  }
  body.push(h1(META.key === 'elite' ? '四、赛场守则' : '四、赛场守则'));
  const w3 = Math.floor(CW / 3);
  const lists = [['家长', C.PARENT_RULES, COL.green], ['教练员', C.COACH_RULES, COL.blue], ['球员', C.PLAYER_RULES, COL.navy]];
  body.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [w3, w3, CW - 2 * w3], layout: TableLayoutType.FIXED,
    borders: { top: NB, bottom: LB(COL.line), left: NB, right: NB, insideHorizontal: NB, insideVertical: { style: BorderStyle.SINGLE, size: 24, color: 'FFFFFF' } },
    rows: [new TableRow({ children: lists.map(([t, , c], i) => cell(ctext(t + '守则', { font: F_H, bold: true, size: 22, color: 'FFFFFF', boldColor: 'FFFFFF' }), i < 2 ? w3 : CW - 2 * w3, { fill: c })) }),
      new TableRow({ children: lists.map(([, l], i) => cell(l.map((s) => new Paragraph({ children: runs('▪ ' + s, { size: 18 }), spacing: { line: 280, after: 60 }, indent: { left: 180, hanging: 180 } })), i < 2 ? w3 : CW - 2 * w3, { fill: COL.paper, va: VerticalAlign.TOP, mt: 120 })) })] }));
  body.push(para('**赛场礼仪**：赛前赛后双方握手；比赛结束后，双方球队在队长带领下列队到对方技术区、观众区前集体行礼致谢。', { noIndent: true, before: 200 }));
  body.push(para(`未尽事宜以《${META.full}竞赛规程》为准。`, { noIndent: true, size: 19, color: COL.slate }));
  body.push(new Paragraph({ children: runs(`${META.short}赛区组委会`, { font: F_H, bold: true, size: 22 }), alignment: AlignmentType.RIGHT, spacing: { before: 300 } }));
  body.push(new Paragraph({ children: runs(COMMON.ORG.issued, { size: 20 }), alignment: AlignmentType.RIGHT }));

  return new Document({ creator: COMMON.ORG.fa, title: `${META.full} 规则精要`, description: `${META.codeSum} v1.0`, styles: STYLES,
    sections: [{ properties: { page: PAGE }, headers: { default: header(META, '规则精要') }, footers: { default: footer(META.codeSum) }, children: body }] });
}

(async () => {
  for (const key of ['elite', 'youth']) {
    const C = require(`./content_${key}`);
    const dir = path.join(ROOT, key === 'elite' ? '02_熊猫精英足球联赛' : '03_熊猫少儿足球联赛');
    fs.mkdirSync(dir, { recursive: true });
    const base = `2026秋季${C.META.cn}`;
    fs.writeFileSync(path.join(dir, `${base}_竞赛规程.docx`), await Packer.toBuffer(regDoc(C)));
    fs.writeFileSync(path.join(dir, `${base}_规则精要.docx`), await Packer.toBuffer(summaryDoc(C)));
    console.log('ok', key);
  }
})();
