// Build 比赛介绍 decks (.pptx) for both leagues with pptxgenjs.
const pptxgen = require('pptxgenjs');
const path = require('path'); const fs = require('fs');
const { applyTheme } = require('/root/.claude/skills/synced/945a8792-87ea-440d-aeed-3ca5e5218242_a286977b-5084-471c-b116-73e0d78dbb3b/pptx/scripts/apply_theme.js');
const COMMON = require('./content_common');

const OUT = path.join(__dirname, '..', 'out');
const VI = path.join(OUT, '01_VI视觉识别系统', 'assets');
const GEN = path.join(__dirname, 'gen');
const PH = (n) => path.join(__dirname, 'photos', n + '.jpg');
const ICON = (n, c = 'FFFFFF') => path.join(GEN, 'icons', `${n}_${c}.png`);
const HEX = { blue: '04518E', navy: '0B2545', ink: '13202F', slate: '5A6B80', mist: 'E6EEF6', paper: 'F5F8FB', gold: 'F2B21B', green: '2FB45A', u6: 'FFC72C', u8: '2FB45A', u10: '1E9BD7', u11: 'F26A2E', red: 'E2231A' };

function makeDeck(M) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
  pres.author = COMMON.ORG.fa; pres.company = COMMON.ORG.fa; pres.title = `${M.full} 比赛介绍`;
  const THEME = { name: `Panda ${M.key}`, headFontFace: 'Microsoft YaHei', bodyFontFace: 'Microsoft YaHei',
    colors: { dk1: HEX.ink, lt1: 'FFFFFF', dk2: HEX.navy, lt2: HEX.mist, accent1: HEX.blue, accent2: M.accent, accent3: HEX.u10,
      accent4: HEX.u11, accent5: HEX.u6, accent6: HEX.slate, hlink: HEX.blue, folHlink: HEX.slate } };
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const logo = path.join(VI, 'logo', `panda-logo_${M.key}_badge.png`);
  const footer = `${M.cn} · ${M.season}比赛介绍`;

  pres.defineSlideMaster({ title: 'COVER', background: { path: path.join(GEN, `bg_dark_${M.key}.png`) },
    objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.2, w: 8, h: 1.2, fontSize: 54, bold: true, color: C.background1, valign: 'bottom', align: 'left', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.45, w: 8, h: 0.7, fontSize: 26, bold: true, color: C.accent2, align: 'left', margin: 0 }, text: '' } }] });
  pres.defineSlideMaster({ title: 'SECTION', background: { path: path.join(GEN, `bg_section_${M.key}.png`) },
    objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.6, w: 11.7, h: 1.2, fontSize: 44, bold: true, color: C.background1, align: 'left', margin: 0 }, text: '' } }] });
  pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' },
    objects: [{ image: { x: 12.2, y: 0.38, w: 0.62, h: 0.62, path: logo } },
      { text: { text: footer, options: { x: 0.6, y: 7.0, w: 8, h: 0.3, fontSize: 9, color: HEX.slate, margin: 0 } } },
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.38, w: 11.2, h: 0.7, fontSize: 30, bold: true, color: C.text2, margin: 0, valign: 'middle', align: 'left' }, text: '' } }],
    slideNumber: { x: 12.3, y: 6.98, w: 0.5, h: 0.3, fontSize: 10, color: HEX.blue, bold: true } });

  let sec = null;
  const section = (t) => { pres.addSection({ title: t }); sec = t; };
  const add = (master) => pres.addSlide({ masterName: master, sectionTitle: sec });
  const kicker = (s, en) => s.addText(en, { x: 0.6, y: 1.08, w: 9, h: 0.32, fontSize: 12, bold: true, color: C.accent6, charSpacing: 3, margin: 0, isTextBox: true, objectName: 'kicker' });
  const content = (title, en) => { const s = add('CONTENT'); s.addText(title, { placeholder: 'title' }); kicker(s, en); return s; };
  const card = (s, x, y, w, h, fill = HEX.paper, name = 'card') => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { type: 'none' }, rectRadius: 0.12, objectName: name });
  const iconC = (s, icon, x, y, d, fill = HEX.blue, ic = 'FFFFFF') => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: 'none' }, objectName: 'icon-bg' });
    s.addImage({ path: ICON(icon, ic), x: x + d * 0.22, y: y + d * 0.22, w: d * 0.56, h: d * 0.56, objectName: 'icon' });
  };
  const txt = (s, text, o) => s.addText(text, { margin: 0, isTextBox: true, valign: 'top', fontSize: 14, color: HEX.ink, paraSpaceAfter: 4, ...o });
  const bullets = (arr, size = 14, color = HEX.ink) => arr.map((t, i) => ({ text: t, options: { bullet: { indent: 14 }, fontSize: size, color, breakLine: i < arr.length - 1, paraSpaceAfter: 6 } }));
  const photo = (s, n, x, y, w, h, rounding = false) => s.addImage({ path: PH(n), x, y, w, h, sizing: { type: 'cover', w, h }, rounding, objectName: 'photo' });
  return { pres, THEME, C, section, add, content, card, iconC, txt, bullets, photo, logo };
}

function cover(D, M, sub, meta) {
  const { section, add, logo } = D;
  section('封面');
  const s = add('COVER');
  s.addText(M.cn, { placeholder: 'title' });
  s.addText(M.en + ' · ' + M.seasonEn, { placeholder: 'body' });
  s.addImage({ path: logo, x: 8.95, y: 1.55, w: 3.5, h: 3.5, objectName: 'logo' });
  D.txt(s, sub, { x: 0.7, y: 4.35, w: 7.5, h: 0.6, fontSize: 24, bold: true, color: 'FFFFFF' });
  D.txt(s, meta, { x: 0.7, y: 5.05, w: 8, h: 0.4, fontSize: 14, color: 'C9D6E6' });
  D.txt(s, `主办：${COMMON.ORG.fa}　${COMMON.ORG.co}`, { x: 0.7, y: 6.6, w: 9, h: 0.35, fontSize: 11, color: '9FB6D1' });
  s.addNotes(`${M.full}比赛介绍。核心理念：${COMMON.ORG.slogan}。`);
}

function closing(D, M) {
  D.section('结束');
  const s = D.add('COVER');
  s.addText('为了每个人更好的成长', { placeholder: 'title' });
  s.addText(COMMON.ORG.sloganEn, { placeholder: 'body' });
  s.addImage({ path: D.logo, x: 8.95, y: 1.55, w: 3.5, h: 3.5, objectName: 'logo' });
  D.txt(s, [{ text: '报名咨询  ', options: { bold: true, color: 'FFFFFF' } }, { text: `${COMMON.ORG.contact}　·　${COMMON.ORG.email}`, options: { color: 'C9D6E6' } }],
    { x: 0.7, y: 4.5, w: 8, h: 0.4, fontSize: 16 });
  D.txt(s, `比赛地点：${COMMON.ORG.venue}　·　${M.schedule}`, { x: 0.7, y: 5.0, w: 8, h: 0.4, fontSize: 14, color: 'C9D6E6' });
  s.addNotes('感谢聆听。欢迎各俱乐部、学校、班级、小区与好朋友组队报名。');
}

function statTiles(D, s, tiles, y, h = 1.55) {
  const n = tiles.length; const gap = 0.25; const w = (12.13 - gap * (n - 1)) / n;
  tiles.forEach(([big, lab], i) => {
    const x = 0.6 + i * (w + gap);
    D.card(s, x, y, w, h);
    D.txt(s, big, { x: x + 0.2, y: y + 0.18, w: w - 0.4, h: 0.75, fontSize: 30, bold: true, color: HEX.blue, fontFace: 'Arial Narrow' });
    D.txt(s, lab, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.5, fontSize: 12, color: HEX.slate });
  });
}

function iconCards(D, s, items, x0, y0, cols, w, h, gapX = 0.25, gapY = 0.25, fill = HEX.paper, ds = 14) {
  items.forEach(([ic, t, d], i) => {
    const x = x0 + (i % cols) * (w + gapX), y = y0 + Math.floor(i / cols) * (h + gapY);
    D.card(s, x, y, w, h, fill);
    D.iconC(s, ic, x + 0.22, y + 0.22, 0.6);
    D.txt(s, t, { x: x + 0.95, y: y + 0.22, w: w - 1.15, h: 0.6, fontSize: 17, bold: true, color: HEX.navy, valign: 'middle' });
    D.txt(s, d, { x: x + 0.22, y: y + 0.95, w: w - 0.44, h: h - 1.05, fontSize: ds, color: HEX.ink });
  });
}

function codesSlide(D, title) {
  const s = D.content(title, 'CODES OF CONDUCT · RESPECT');
  const cols = [['家长', 'TbHeart', HEX.green, COMMON.PARENT_RULES], ['教练员', 'TbMessageCircle', HEX.blue, COMMON.COACH_RULES], ['球员', 'TbBallFootball', HEX.navy, COMMON.PLAYER_RULES]];
  const strip = (t) => t.replace(/\*\*/g, '');
  cols.forEach(([t, ic, col, list], i) => {
    const x = 0.6 + i * 4.13, w = 3.88;
    D.card(s, x, 1.65, w, 5.1);
    D.iconC(s, ic, x + 0.25, 1.85, 0.62, col);
    D.txt(s, t + '守则', { x: x + 1.0, y: 1.85, w: 2.6, h: 0.62, fontSize: 18, bold: true, color: HEX.navy, valign: 'middle' });
    D.txt(s, D.bullets(list.map(strip), 12.5), { x: x + 0.25, y: 2.65, w: w - 0.45, h: 4.0 });
  });
  s.addNotes('三方守则来自本联赛《规则精要》，参照英格兰足总 Respect 计划和日本足协“最佳支持者”家长手册。核心：不遥控、多鼓励、尊重执裁。');
  return s;
}

function intlSlide(D, items, note) {
  const s = D.content('国际经验，本土实践', 'INTERNATIONAL REFERENCES');
  items.forEach(([org, flag, what, ours], i) => {
    const x = 0.6 + (i % 2) * 6.17, y = 1.65 + Math.floor(i / 2) * 2.6, w = 5.92, h = 2.35;
    D.card(s, x, y, w, h);
    D.txt(s, flag, { x: x + 0.25, y: y + 0.2, w: 1.2, h: 0.5, fontSize: 22, bold: true, color: HEX.blue, fontFace: 'Arial Narrow' });
    D.txt(s, org, { x: x + 1.35, y: y + 0.2, w: w - 1.6, h: 0.5, fontSize: 15, bold: true, color: HEX.navy, valign: 'middle' });
    D.txt(s, what, { x: x + 0.25, y: y + 0.8, w: w - 0.5, h: 0.85, fontSize: 13, color: HEX.ink });
    D.txt(s, [{ text: '本联赛  ', options: { bold: true, color: HEX.blue } }, { text: ours, options: { color: HEX.ink } }], { x: x + 0.25, y: y + 1.65, w: w - 0.5, h: 0.6, fontSize: 13 });
  });
  s.addNotes(note);
}

// ===================================================================== ELITE
function eliteDeck() {
  const M = { ...require('./content_elite').META, accent: HEX.gold };
  const D = makeDeck(M); const { pres } = D;
  cover(D, M, '2026 秋季赛季 · 比赛介绍', 'U10 / U11　·　8 人制　·　每周六下午　·　四川新北足球中心');

  D.section('关于联赛');
  let s = D.content('我们是谁', 'ABOUT THE LEAGUE');
  D.txt(s, [
    { text: '熊猫精英足球联赛', options: { bold: true, color: HEX.navy, fontSize: 20, breakLine: true } },
    { text: `由${COMMON.ORG.fa}与${COMMON.ORG.co}联合主办、新北体育赛区组委会运营，聚焦 U10、U11 两个年龄组的八人制比赛。`, options: { breakLine: true } },
    { text: '它是始于 2017 年的熊猫少儿足球联赛的进阶平台：当孩子从 3 人制、5 人制成长到 8 人制，熊猫联赛继续陪伴他们，在更大的场地上接受更完整的比赛。', options: {} },
  ], { x: 0.6, y: 1.75, w: 5.6, h: 3.2, fontSize: 15, paraSpaceAfter: 10 });
  D.photo(s, 'p5_x33', 6.6, 1.65, 6.13, 3.45);
  statTiles(D, s, [['2017', '熊猫联赛创办'], ['1500+', '年均组织比赛场次经验'], ['2 组', 'U10 · U11'], ['每周六', '下午 · 常态化联赛']], 5.3, 1.4);
  s.addNotes('熊猫精英联赛延续熊猫联赛“联赛制、常态化”的传统，2026 春季首届，本季为第二个赛季。');

  s = D.content('办赛理念：以球员成长为中心', 'PLAYER-CENTRED');
  D.txt(s, '为了每个人更好的成长', { x: 0.6, y: 1.75, w: 5.2, h: 1.0, fontSize: 34, bold: true, color: HEX.blue });
  D.txt(s, COMMON.ORG.sloganEn, { x: 0.6, y: 2.75, w: 5.2, h: 0.4, fontSize: 14, bold: true, color: HEX.slate, charSpacing: 2 });
  D.txt(s, '比赛是足球运动的核心。我们希望每一位教练和家长更关注孩子长期的成长，而不只是眼前一场比赛的输赢或一届比赛的名次。', { x: 0.6, y: 3.45, w: 5.0, h: 1.6, fontSize: 15 });
  D.photo(s, 'p4_x29', 0.6, 5.1, 5.0, 1.65);
  iconCards(D, s, [['TbSeedling', '成长', '以赛促练，每一次触球、每一次尝试都是成长。'], ['TbHeartHandshake', '尊重', '尊重对手、队友、执裁者；握手与致谢。'],
    ['TbMoodHappy', '快乐', '充足的上场时间，自由的决策空间。'], ['TbScale', '公平', '按实力分组、均等上场、保持竞争。']], 6.1, 1.65, 2, 3.2, 2.4);
  s.addNotes('四个关键词贯穿全部规则设计：成长、尊重、快乐、公平。');

  s = D.content('我们看到的问题，我们的解决办法', 'PROBLEMS → SOLUTIONS');
  const probs = [['组队难', '人数限制严苛、组队形式单一，小区队、好友队无法参赛'], ['强弱悬殊', '参赛队伍水平参差不齐，强弱差距过大'], ['唯胜负论', '少数主力打满全场，多数孩子没有上场机会'], ['训练脱节', '缺少真实比赛中的应变与团队配合'], ['功利心重', '过度强调成绩，忽视规则意识与体育精神']];
  const sols = [['降低组队门槛', '学校、俱乐部、小区、好朋友均可组队；允许混龄，可报大一岁女队员'], ['按实力分组', '级别组循环 + 阶段升降组，比赛双方实力接近'], ['全员均等上场', '每人上场 ≥ 全场一半，位置轮换（含守门员）'], ['以赛促练', '参考日本模式：放宽判罚尺度、保持比赛连贯，教练员执裁'], ['规则与礼仪引导', '赛场三方守则、赛后致谢礼、绿牌表彰']];
  probs.forEach(([t, d], i) => {
    const y = 1.65 + i * 1.02;
    D.card(s, 0.6, y, 5.5, 0.88, 'FDECEB');
    D.txt(s, t, { x: 0.8, y: y + 0.1, w: 1.4, h: 0.68, fontSize: 15, bold: true, color: HEX.red, valign: 'middle' });
    D.txt(s, d, { x: 2.2, y: y + 0.1, w: 3.75, h: 0.68, fontSize: 13, valign: 'middle' });
    s.addImage({ path: ICON('TbArrowsExchange', '04518E'), x: 6.27, y: y + 0.22, w: 0.44, h: 0.44, objectName: 'arrow' });
    D.card(s, 6.88, y, 5.85, 0.88, 'E7F0F9');
    D.txt(s, sols[i][0], { x: 7.08, y: y + 0.1, w: 1.75, h: 0.68, fontSize: 15, bold: true, color: HEX.blue, valign: 'middle' });
    D.txt(s, sols[i][1], { x: 8.85, y: y + 0.1, w: 3.75, h: 0.68, fontSize: 13, valign: 'middle' });
  });
  s.addNotes('左侧为当前同类赛事的常见问题，右侧为熊猫精英联赛的对应做法。');

  D.section('赛事概览');
  s = D.content('赛事概览', 'AT A GLANCE');
  statTiles(D, s, [['U10 · U11', '2016 / 2015 年 1 月 1 日后出生'], ['8 人制', '7 名场上球员 + 1 名守门员'], ['4 × 20′', '四节制，节间可指导'], ['4 号球', '适合本年龄段身体条件']], 1.7);
  statTiles(D, s, [['68 × 50 m', '参考场地尺寸 · 5 × 2 m 球门'], ['∞ 换人', '滚动换人，击掌上下'], ['≥ 50%', '每名球员最少上场时间'], ['周六下午', '四川新北足球中心']], 3.5);
  D.txt(s, [{ text: '本季变化  ', options: { bold: true, color: HEX.blue } }, { text: '组别名称改用国际通行“U + 年龄”计法（出生年份与春季 U9/U10 相同）；比赛用球由 5 号调整为 4 号（与日本 JFA U-12、英格兰 9v9 一致）；新增退守线、限制头球、头部伤害“有疑问就下场”。', options: {} }],
    { x: 0.6, y: 5.4, w: 12.1, h: 1.2, fontSize: 13 });
  s.addNotes('与 2026 春季相比，本季的主要调整在最后一行。');

  intlSlide(D, [
    ['日本足球协会 JFA', 'JP', 'U-12 全面推行 8 人制，场地约 68×50 m、4 号球、自由换人；以联赛（リーグ戦）代替一次性淘汰赛。', '8 人制 + 自由换人 + 联赛制；放宽判罚尺度、保持比赛连贯。'],
    ['英格兰足总 The FA', 'EN', '小场赛制、退守线、滚动换人；建议每名球员上场 ≥50%；Respect 行为守则；U12 及以下限制故意头球。', '均等上场、退守线、三方守则、不鼓励头球。'],
    ['西班牙足协及地区足协', 'ES', '低龄组 Fútbol 7 / 8 分节进行并要求全员参赛；安达卢西亚足协首创“绿牌”表彰公平竞赛。', '四节制、全员上场与位置轮换、绿牌。'],
    ['国际足球理事会 IFAB', 'IFAB', '青少年与草根足球可使用“暂时罚离（sin bin）”，时长约为比赛时间的 10%–15%。', '黄牌 = 暂时罚离 8 分钟到冷静区，球队可立即补人。'],
  ], '每一条特色规则都有国际实践作为依据，并结合成都本地青少年足球的实际情况调整。');

  D.section('特色规则');
  s = D.content('全员均等上场，位置轮换', 'EQUAL PLAYING TIME');
  D.card(s, 0.6, 1.65, 4.2, 5.1, HEX.blue, 'hero');
  D.txt(s, '≥ 50%', { x: 0.85, y: 1.95, w: 3.8, h: 1.3, fontSize: 60, bold: true, color: 'FFFFFF', fontFace: 'Arial Narrow' });
  D.txt(s, '每名到场球员的累计上场时间原则上相同，且不少于全场比赛时间的一半（40 分钟）。', { x: 0.85, y: 3.35, w: 3.7, h: 1.3, fontSize: 15, color: 'FFFFFF' });
  D.txt(s, '每队建议报名 12–15 人，最多 16 人：16 人 × 40 分钟 = 8 人 × 80 分钟。', { x: 0.85, y: 4.85, w: 3.7, h: 1.2, fontSize: 12, color: 'C9D6E6' });
  iconCards(D, s, [['TbRotate', '位置轮换', '每名球员每场至少在两个位置上场，体验不同角色。'], ['TbShirtSport', '守门员轮换', '每场至少更换一次守门员（建议每节）；赛季中人人有机会。'],
    ['TbChecklist', '上场时间记录表', '各队如实填写，赛后由比赛监督核查。'], ['TbArrowsExchange', '滚动换人', '不限次数、不用停表，在换人区击掌上下。']], 5.05, 1.65, 2, 3.72, 2.42);
  s.addNotes('“少数主力打满全场”是我们最想改变的现象。均等上场写进竞赛规程，未执行的球队将被警告，累计两次取消团体奖项评选资格。');

  s = D.content('保持竞争：落后可增员', 'KEEP IT COMPETITIVE');
  const steps = [['落后 3 球', '+1', '可额外增加 1 名场上队员'], ['落后 4 球及以上', '+2', '可额外增加 2 名场上队员（最多 2 人）'], ['分差回落', '−1', '最后上场的增加队员在下一次死球时就近下场']];
  steps.forEach(([a, b, c], i) => {
    const x = 0.6 + i * 4.13;
    D.card(s, x, 1.7, 3.88, 3.0, i === 2 ? HEX.paper : HEX.navy);
    D.txt(s, a, { x: x + 0.3, y: 1.9, w: 3.3, h: 0.5, fontSize: 18, bold: true, color: i === 2 ? HEX.navy : 'FFFFFF' });
    D.txt(s, b, { x: x + 0.3, y: 2.4, w: 3.3, h: 1.3, fontSize: 66, bold: true, color: i === 2 ? HEX.blue : HEX.gold, fontFace: 'Arial Narrow' });
    D.txt(s, c, { x: x + 0.3, y: 3.75, w: 3.3, h: 0.8, fontSize: 13, color: i === 2 ? HEX.ink : 'E6EEF6' });
  });
  D.txt(s, D.bullets(['增人须在死球时向执裁教练申请并经同意；新增队员须在本场上场名单内。', '目的：让大比分落后的一方依然有机会，让领先的一方面对更高的挑战——双方都在比赛中成长。', '与“比分保护”配合：积分排名中每场净胜球最多按 6 球计算。'], 14),
    { x: 0.6, y: 5.0, w: 12.1, h: 1.7 });
  s.addNotes('“保持竞争”是熊猫联赛自 2017 年以来的传统规则。');

  s = D.content('教练员执裁，放宽判罚尺度', 'COACH REFEREES · LET THEM PLAY');
  D.card(s, 0.6, 1.65, 5.95, 5.1);
  D.iconC(s, 'TbUserCheck', 0.85, 1.85, 0.7);
  D.txt(s, '为什么让教练员来做裁判', { x: 1.7, y: 1.85, w: 4.6, h: 0.7, fontSize: 18, bold: true, color: HEX.navy, valign: 'middle' });
  D.txt(s, D.bullets(['双方教练员各执裁半场（两节），可使用电子口哨，比赛监督在场协助。', '教练员最了解球员，执裁时能直观观察球员在实战中的优点与不足，赛后针对性指导，真正“以赛促练”。', '执裁加深教练员对规则的理解，训练中更好地传递规则意识。', '执裁时可安排换人、向本队队员提问，但不能指挥场上球员。'], 15),
    { x: 0.85, y: 2.75, w: 5.5, h: 3.9 });
  D.card(s, 6.78, 1.65, 5.95, 5.1);
  D.iconC(s, 'TbScale', 7.03, 1.85, 0.7, HEX.gold);
  D.txt(s, '为什么判罚尺度要大一些', { x: 7.88, y: 1.85, w: 4.6, h: 0.7, fontSize: 18, bold: true, color: HEX.navy, valign: 'middle' });
  D.txt(s, D.bullets(['参考日本青少年比赛：正常的身体对抗、单手轻微拉拽，只要不是故意犯规、不造成安全隐患，均不暂停比赛。', '过严的判罚会频繁中断比赛，让球员畏手畏脚、不敢尝试。', '报复性伤人、肘击、双手抱人或拉拽、从后方推人或铲人等，至少黄牌。', '保护头颈：不鼓励头球，故意头球判间接任意球。'], 15),
    { x: 7.03, y: 2.75, w: 5.5, h: 3.9 });
  s.addNotes('教练执裁与放宽尺度，是熊猫精英联赛最有特色、也最需要各方理解的两条规则。');

  s = D.content('冷静区 · 绿牌 · 比分保护', 'COOL-DOWN · GREEN CARD · SCORE CAP');
  const three = [['FFD200', 'TbSnowflake', '黄牌 = 暂时罚离', HEX.navy, ['球员暂时罚离 8 分钟，去冷静区冷静（参照 IFAB 指引）。', '球队可立即补上替补，仍是 8 对 8——不因一个孩子的失误让整队失去锻炼机会。', '时间到后先回替补席，再按滚动换人上场。']],
    [HEX.green, 'TbHeartHandshake', '绿牌 = 表彰', 'FFFFFF', ['主动承认球是自己碰出界的。', '主动扶起对手或向对手道歉。', '被误判时仍保持礼貌。', '绿牌计入“公平竞赛奖”。']],
    [HEX.blue, 'TbShieldCheck', '比分保护', 'FFFFFF', ['比分照常记录。', '积分排名中每场净胜球最多按 6 球计算。', '减少大比分对输球一方孩子的心理打击。']]];
  three.forEach(([col, ic, t, tc, list], i) => {
    const x = 0.6 + i * 4.13;
    D.card(s, x, 1.65, 3.88, 1.3, col);
    s.addImage({ path: ICON(ic, tc === 'FFFFFF' ? 'FFFFFF' : '0B2545'), x: x + 0.25, y: 1.95, w: 0.7, h: 0.7, objectName: 'icon' });
    D.txt(s, t, { x: x + 1.1, y: 1.85, w: 2.6, h: 0.9, fontSize: 20, bold: true, color: tc, valign: 'middle' });
    D.card(s, x, 3.1, 3.88, 3.65);
    D.txt(s, D.bullets(list, 15), { x: x + 0.25, y: 3.3, w: 3.4, h: 3.3 });
  });
  s.addNotes('三条规则共同的出发点：让孩子在出错后仍有机会，在诚实与善意中被看见。');

  s = D.content('场地与功能区', 'PITCH & ZONES');
  s.addImage({ path: path.join(GEN, 'pitch_8v8.png'), x: 0.6, y: 1.55, w: 5.45, h: 5.18, objectName: 'pitch' });
  iconCards(D, s, [['TbFlag', '越位区', '越位只在越位线（第一个五人制场地边线）与球门线之间判罚。'], ['TbSoccerField', '退守线', '球门球或守门员持球时，对方退到中线以后。'],
    ['TbArrowsExchange', '换人区', '在本队替补席一侧，下场队员离场后击掌交接。'], ['TbSnowflake', '冷静区', '暂时罚离的球员在此冷静，时间到后回替补席。'],
    ['TbHeart', '家长观赛区', '距边线 ≥ 2 米，只加油，不指挥，不进场。'], ['TbBallFootball', '多球制', '场边摆放比赛用球，出界就近取球；非比赛人员勿碰。']], 6.35, 1.65, 2, 3.07, 1.55, 0.25, 0.22, HEX.paper, 12);
  s.addNotes('场地布置示意，实际以比赛当日场地标识为准。');

  D.section('参赛须知');
  codesSlide(D, '三方守则：家长 · 教练员 · 球员');

  s = D.content('每一名球员都会被看见', 'AWARDS FOR EVERYONE');
  D.photo(s, 'p6_x45', 0.6, 1.65, 4.6, 5.1);
  iconCards(D, s, [['TbTrophy', '冠亚季军', '各级别组按积分（含比分保护）排名。'], ['TbHeartHandshake', '公平竞赛奖', '绿牌多、黄红牌少的球队。'],
    ['TbStar', '成长之星', '每队教练推选进步最大的 2 名球员。'], ['TbUserCheck', '执裁与志愿者', '最佳执裁教练、优秀志愿者：感谢让比赛更好的人。']], 5.45, 1.65, 2, 3.52, 1.55, 0.25, 0.22, HEX.paper, 13);
  D.card(s, 5.45, 5.2, 7.29, 1.55, HEX.navy);
  D.iconC(s, 'TbMedal', 5.7, 5.5, 0.9, HEX.gold, '0B2545');
  D.txt(s, [{ text: '所有队员都会上台', options: { bold: true, fontSize: 18, color: 'FFFFFF', breakLine: true } }, { text: '闭幕式上，颁奖嘉宾为每一名小球员颁发完赛奖牌、证书与纪念品。', options: { fontSize: 13, color: 'C9D6E6' } }],
    { x: 6.8, y: 5.4, w: 5.8, h: 1.2, valign: 'middle' });
  s.addNotes('冠亚季军之外，更多奖项面向每一名球员的付出与努力。');

  s = D.content('报名参赛', 'HOW TO JOIN');
  iconCards(D, s, [['TbBuildingCommunity', '谁可以报名', '学校、年级、班级、青训俱乐部、小区队伍、好朋友队伍；可混龄；可报名大一岁女队员（不限人数）。'],
    ['TbUsers', '报名人数', '教练 1 人 + 领队 / 翻译 1 人；队员建议 12–15 人，最多 16 人。'],
    ['TbChecklist', '报名资料', '参赛报名表；个人报名表（肖像权协议、参赛承诺书、个人资料、意外险证明）；球队集体照。'],
    ['TbShieldCheck', '参赛资格', '身体健康、持有效身份证明、已购买人身意外伤害保险、实名登记。']], 0.6, 1.65, 2, 5.95, 1.95, 0.22, 0.22);
  D.card(s, 0.6, 5.95, 12.13, 0.8, 'E7F0F9');
  D.txt(s, [{ text: '报名方式  ', options: { bold: true, color: HEX.blue } }, { text: `报名资料发送至 ${COMMON.ORG.email}　·　联系人 ${COMMON.ORG.contact}　·　截止时间与费用以《报名通知》为准`, options: {} }],
    { x: 0.85, y: 6.05, w: 11.7, h: 0.6, fontSize: 14, valign: 'middle' });
  s.addNotes('报名资料一经提交原则上不得更改；因伤病可在赛程过半前申请补报。');

  closing(D, M);
  return { D, M };
}

// ===================================================================== YOUTH
function youthDeck() {
  const Y = require('./content_youth');
  const M = { ...Y.META, accent: HEX.green };
  const D = makeDeck(M); const { pres } = D;
  cover(D, M, '2026 秋季赛季 · 比赛介绍', 'U6 3 人制　·　U8 / U10 5 人制　·　每周日上午　·　四川新北足球中心');

  D.section('关于联赛');
  let s = D.content('始于 2017 年', 'SINCE 2017');
  D.txt(s, [
    { text: '从第一届比赛开始，就坚持联赛制', options: { bold: true, color: HEX.navy, fontSize: 20, breakLine: true } },
    { text: '熊猫少儿足球联赛由成都高新区足球协会主办，自 2017 年起以单循环或双循环的联赛制进行比赛。多年来，年均 1500 场以上的比赛组织经验，加上家长、教练与俱乐部的支持与认可，让这个比赛平台持续、稳定地发展。', options: {} },
  ], { x: 0.6, y: 1.75, w: 5.6, h: 3.2, fontSize: 15, paraSpaceAfter: 10 });
  D.photo(s, 'p7_x49', 6.6, 1.65, 6.13, 3.45);
  statTiles(D, s, [['2017', '联赛创办'], ['1500+', '年均组织比赛场次'], ['3 组', 'U6 · U8 · U10'], ['每周日', '上午 · 常态化联赛']], 5.3, 1.4);
  s.addNotes('“年均 1500+ 场”沿用联赛 2021 年介绍资料中的数据。');

  s = D.content('为什么比赛？', 'WHY MATCHES MATTER');
  iconCards(D, s, [['TbBallFootball', '核心', '比赛是足球运动的核心。'], ['TbSeedling', '成长', '球员在比赛中获得成长。'], ['TbSparkles', '激情', '比赛让每个人都充满激情。']], 0.6, 1.65, 1, 5.3, 1.52, 0.25, 0.22);
  s.addChart(pres.charts.DOUGHNUT, [{ name: '传统选拔式比赛', labels: ['主力：比赛机会充足', '替补：偶尔上场', '没有比赛机会'], values: [10, 10, 80] }], {
    x: 6.2, y: 1.6, w: 6.5, h: 4.3, holeSize: 55, chartColors: [HEX.blue, HEX.u10, HEX.navy], showPercent: true, showValue: false, showLegend: true, legendPos: 'r', legendFontSize: 12,
    legendFontFace: '+mn-lt', dataLabelColor: 'FFFFFF', dataLabelFontSize: 12, dataLabelFontFace: '+mn-lt', showTitle: true, title: '传统选拔式比赛中的球员（示意）', titleFontSize: 14, titleColor: HEX.navy, titleFontFace: '+mn-lt' });
  D.txt(s, '对于这 90% 的孩子来说，他们是不是失去了在比赛中成长的机会？——这正是熊猫少儿联赛想要改变的。', { x: 6.4, y: 6.0, w: 6.3, h: 0.75, fontSize: 13, color: HEX.slate });
  s.addNotes('10% / 10% / 80% 为联赛 2021 年介绍资料中的示意比例，用来说明选拔式比赛的问题。');

  s = D.content('每个人都是冠军', 'EVERYONE IS A CHAMPION');
  D.photo(s, 'p9_x60', 0.6, 1.65, 5.2, 5.1);
  D.txt(s, '每名球员都通过比赛得到了成长，成为了更好的自己——所以，每个人都是冠军！', { x: 6.1, y: 1.7, w: 6.6, h: 1.0, fontSize: 18, bold: true, color: HEX.navy });
  [['TbTrophy', '不设冠军', '没有冠亚季军，只有一起成长的伙伴。'], ['TbChartLine', '不统计积分', '没有积分榜，比分只用于调整组别，让比赛双方实力接近。'], ['TbBan', '不公布赛果', '对外传播只讲成长：上场人数、精彩瞬间、勇敢的尝试。']].forEach(([ic, t, d], i) => {
    const y = 2.95 + i * 1.28;
    D.card(s, 6.1, y, 6.63, 1.1);
    D.iconC(s, ic, 6.3, y + 0.2, 0.7, HEX.green);
    D.txt(s, t, { x: 7.2, y: y + 0.12, w: 5.3, h: 0.45, fontSize: 16, bold: true, color: HEX.navy });
    D.txt(s, d, { x: 7.2, y: y + 0.55, w: 5.3, h: 0.45, fontSize: 12 });
  });
  s.addNotes('英格兰足总 U11 及以下、澳大利亚 MiniRoos、荷兰 6v6 也都不公布比分与排名。');

  D.section('三个组别');
  s = D.content('三个组别，三种比赛', 'THREE FORMATS');
  const gs = [['U6', HEX.u6, HEX.navy, '3 人制', ['2020.1.1 后出生', '不设守门员 · 3 号球', '4 节 × 8 分钟', '约 20 × 15 m · 迷你球门']], ['U8', HEX.u8, 'FFFFFF', '5 人制', ['2018.1.1 后出生', '设守门员（全员轮换）· 3 号球', '4 节 × 10 分钟', '约 30–37 × 20–25 m · 3 × 2 m']],
    ['U10', HEX.u10, 'FFFFFF', '5 人制', ['2016.1.1 后出生', '设守门员（全员轮换）· 4 号球', '4 节 × 12 分钟', '约 36–40 × 20–25 m · 3 × 2 m']]];
  gs.forEach(([g, col, tc, f, list], i) => {
    const x = 0.6 + i * 4.13;
    D.card(s, x, 1.65, 3.88, 1.75, col);
    D.txt(s, g, { x: x + 0.3, y: 1.75, w: 2.0, h: 1.0, fontSize: 54, bold: true, color: tc, fontFace: 'Arial Narrow' });
    D.txt(s, f, { x: x + 0.3, y: 2.75, w: 3.3, h: 0.5, fontSize: 18, bold: true, color: tc });
    D.card(s, x, 3.55, 3.88, 3.2);
    D.txt(s, D.bullets(list, 14), { x: x + 0.25, y: 3.8, w: 3.4, h: 2.8 });
  });
  s.addNotes('每个组别覆盖两个出生年份：U6 含 U5，U8 含 U7，U10 含 U9。可报名大一岁女队员，并可报名上一年龄段 9 月 1 日后出生的球员（U6 1 人、U8 2 人、U10 3 人）。');

  const groupSlide = (g, title, en, pitch, rules, note, col) => {
    const sl = D.content(title, en);
    sl.addImage({ path: path.join(GEN, pitch), x: 0.6, y: 1.75, w: 5.6, h: 5.6 * (pitch === 'pitch_u6.png' ? 0.86 : 0.7), sizing: { type: 'contain', w: 5.6, h: 4.5 }, objectName: 'pitch' });
    iconCards(D, sl, rules, 6.5, 1.65, 2, 3.0, 1.6, 0.23, 0.2, HEX.paper, 12.5);
    sl.addNotes(note);
  };
  groupSlide('U6', 'U6 组 · 3 人制', 'U6 · 3V3 · NO GOALKEEPER', 'pitch_u6.png', [
    ['TbClock', '4 节 × 8 分钟', '休息 1′ / 3′ / 1′；教练员只能在休息时指导。'], ['TbUsersGroup', '人人上场', '所有到场球员上场时间基本相同，不少于全场一半。'],
    ['TbArrowsExchange', '运球 / 传球入场', '界外球不掷球，运球或传球入场，防守队员退 3 米。'], ['TbSoccerField', '底线球', '防守方在本方球门线附近运球入场，对方退到中线以后。'],
    ['TbBallFootball', '开球', '可向任意方向，可直接运球；直接射门不得分。'], ['TbHandStop', '犯规', '一律间接任意球（退 3 米），不设点球；不铲球。']],
    '参照英格兰足总 3v3：无守门员、运球或传球重启、多触球。', HEX.u6);
  groupSlide('U8', 'U8 组 · 5 人制', 'U8 · 5V5', 'pitch_u8.png', [
    ['TbClock', '4 节 × 10 分钟', '休息 1′ / 3′ / 1′；每队每节可暂停 1 次（≤1 分钟）。'], ['TbShirtSport', '守门员轮换', '设守门员，鼓励所有队员轮换担任，穿组委会提供的背心。'],
    ['TbArrowsExchange', '踢球 / 运球入场', '界外球对方退 5 米，4 秒内发出；直接踢进不算得分。'], ['TbSoccerField', '退守线', '球门球由守门员发出，对方退到中线以后，直至本方另一人触球。'],
    ['TbFlag', '角球', '运球或传球入场，防守队员退 5 米。'], ['TbHandStop', '犯规', '按五人制规则判罚，罚球区内直接任意球犯规判点球。']],
    '今年 U8 由 4 人制升级为 5 人制并设守门员，参照英格兰足总 U8–U9 5v5。', HEX.u8);
  groupSlide('U10', 'U10 组 · 5 人制', 'U10 · 5V5', 'pitch_u10.png', [
    ['TbClock', '4 节 × 12 分钟', '休息 1′ / 3′ / 1′；每队每节可暂停 1 次（≤1 分钟）。'], ['TbBallFootball', '4 号球', '更大的球、更长的比赛，衔接周六的八人制精英联赛。'],
    ['TbArrowsExchange', '踢球 / 运球入场', '界外球对方退 5 米，4 秒内发出；直接踢进不算得分。'], ['TbSoccerField', '退守线', '球门球由守门员发出，对方退到中线以后，鼓励从后场组织。'],
    ['TbShirtSport', '守门员轮换', '所有队员轮换担任守门员，体验不同位置。'], ['TbHandStop', '犯规', '按五人制规则判罚，罚球区内直接任意球犯规判点球。']],
    'U10 组为 5 人制，适合刚接触比赛或希望更多触球的球队；希望挑战八人制的球队可报名周六的熊猫精英联赛。', HEX.u10);

  s = D.content('通用规则', 'RULES FOR ALL GROUPS');
  iconCards(D, s, Y.SUMMARY.general.map(([ic, t, d]) => [ic, t.replace(' · ', ''), d]), 0.6, 1.65, 4, 2.85, 2.42, 0.24, 0.25, HEX.paper, 13);
  s.addNotes('“保持竞争”、均等上场、不铲球、不判越位、绿牌，是三个组别共同的规则。');

  intlSlide(D, [
    ['英格兰足总 The FA', 'EN', '“Future Fit”赛制：U7 3v3，U8–U9 5v5；运球入场、退守线、滚动换人；U11 及以下不公布比分与积分榜。', 'U6 3v3、U8/U10 5v5；运球入场、退守线；不公布赛果。'],
    ['德国足协 DFB', 'DE', '2024/25 起推行儿童足球新赛制：小场、少人数、多球门、轮换上场，低龄段取消冠军联赛。', '小场地、少人数、全员均等上场、不设冠军。'],
    ['日本足球协会 JFA', 'JP', 'キッズ（U-6/U-8）节庆式比赛，不记录结果与名次；“最佳支持者”家长手册。', '每个人都是冠军；家长只加油、不指挥。'],
    ['荷兰 KNVB · 澳大利亚 MiniRoos', 'NL·AU', '6v6 场边引导员、不公布结果；MiniRoos 全年龄段不记比分、不设积分榜。', '场地引导员执裁，以教育与引导为主。'],
  ], '国际主流足协的低龄比赛，都在朝“更小的场地、更少的人数、更多的触球、更少的结果压力”方向改革。');

  D.section('参赛须知');
  s = D.content('为了每个人更好的成长', 'A BETTER ENVIRONMENT TO GROW');
  iconCards(D, s, [['TbUserPlus', '落后三球，多上一人', '保持竞争，每一场比赛都有悬念。'], ['TbUsersGroup', '到场球员上场时间相同', '每个人都有在比赛中成长的机会。'],
    ['TbRotate', '轮换比赛位置', '前锋、后卫、守门员，都试一试。'], ['TbMessageCircle', '提问代替遥控', '教练员向球员提问，让孩子自己作决定。']], 0.6, 1.65, 2, 3.4, 2.4, 0.24, 0.24);
  s.addImage({ path: path.join(VI, 'applications', 'growth-card_youth.png'), x: 7.95, y: 1.75, w: 4.75, h: 3.0, objectName: 'growth-card' });
  D.txt(s, '我的成长卡：教练赛后发给每个孩子——今天勇敢尝试了什么？帮助了谁？下次想做得更好的是什么？', { x: 7.95, y: 4.95, w: 4.75, h: 1.6, fontSize: 13, color: HEX.slate });
  s.addNotes('成长卡是本季新增的小工具，可在联赛 VI 素材包中找到模板。');

  codesSlide(D, '家长与教练员守则');

  s = D.content('丰富且受欢迎的纪念品', 'AWARDS & MEMORIES');
  D.photo(s, 'p9_x59', 0.6, 1.65, 5.2, 5.1);
  iconCards(D, s, [['TbMedal', '每一名小球员', '完赛奖牌 + 完赛证书 + 比赛纪念品 + 比赛手册。'], ['TbStar', '成长之星', '每队教练推选进步最大的 2 名球员，奖品 + 证书。'],
    ['TbAward', '优秀教练与执裁', '感谢陪伴孩子成长的大人们，奖品 + 证书。'], ['TbHeartHandshake', '公平竞赛与志愿者', '绿牌多、纪律好的球队；赛场上的志愿者。']], 6.1, 1.65, 2, 3.2, 2.42, 0.23, 0.26);
  s.addNotes('闭幕式上所有队员都会上台领奖。');

  s = D.content('现在报名', 'HOW TO JOIN');
  iconCards(D, s, [['TbBuildingCommunity', '报名单位', '俱乐部、学校、班级、小区、好朋友等组队均可；每个单位可同时报名多个年龄组。'],
    ['TbUsers', '报名人数', 'U6 建议 5–6 人（最多 6 人）；U8、U10 建议 8–10 人（最多 10 人）；教练 1 人 + 领队 / 翻译 1 人。'],
    ['TbChecklist', '报名资料', '参赛报名表；个人报名表（肖像权协议、参赛承诺书、个人资料、意外险证明）；球队集体照。'],
    ['TbShieldCheck', '保险与安全', '须购买人身意外伤害保险，组委会另免费提供附加意外险；头部伤害“有疑问，就下场”。']], 0.6, 1.65, 2, 5.95, 1.95, 0.22, 0.22);
  D.card(s, 0.6, 5.95, 12.13, 0.8, 'E8F6EC');
  D.txt(s, [{ text: '报名咨询  ', options: { bold: true, color: HEX.green } }, { text: `${COMMON.ORG.contact}　·　${COMMON.ORG.email}　·　比赛费用与保证金以《报名通知》为准`, options: {} }],
    { x: 0.85, y: 6.05, w: 11.7, h: 0.6, fontSize: 14, valign: 'middle' });
  s.addNotes('保证金在赛季结束后根据竞赛规程结算退还。');

  closing(D, M);
  return { D, M };
}

(async () => {
  for (const [fn, dir] of [[eliteDeck, '02_熊猫精英足球联赛'], [youthDeck, '03_熊猫少儿足球联赛']]) {
    const { D, M } = fn();
    const file = path.join(OUT, dir, `2026秋季${M.cn}_比赛介绍.pptx`);
    await D.pres.writeFile({ fileName: file });
    await applyTheme(file, D.THEME);
    console.log('ok', file);
  }
})();
