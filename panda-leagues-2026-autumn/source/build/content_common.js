// Shared content blocks for both leagues (2026 Autumn).
// Strings may contain **bold** markup.

const ORG = {
  fa: '成都高新区足球协会',
  faShort: '高新足协',
  co: '四川新北体育文化传播有限公司',
  coShort: '新北体育',
  venue: '四川新北足球中心',
  email: 'PYLCTU@163.com',
  contact: '19980720350（杨老师）',
  slogan: '为了每个人更好的成长',
  sloganEn: 'FOR BETTER GROWTH OF EVERYONE',
  issued: '2026 年 10 月',
};

// Codes of conduct shared by both leagues (from 规则精要 20260314 + FA Respect / JFA ベストサポーター)
const PARENT_RULES = [
  '家长须停留在**家长观赛区**（与边线保持至少 2 米距离），可以为孩子加油、鼓掌。',
  '不得有干扰球员决策的行为：不在场边指挥、命令，不对任何球员打骂、讽刺、威胁、嘲笑。',
  '比赛进行中不进入场地为孩子擦汗、喂水、拿书包等（球员受伤等特殊情况除外，须经执裁人员示意）。',
  '尊重执裁人员（执裁教练 / 场地引导员）的判罚，不指责球员、教练员、执裁人员和组委会工作人员。',
  '赛后多问孩子“今天开心吗？尝试了什么？”，少问“赢了吗？进了几个球？”。',
];
const COACH_RULES = [
  '在比赛中可以：指导替补队员、安排换人、向队员**提问**、为队员加油。',
  '在比赛中不可以：**遥控**场上球员——如直接命令传球、射门、向左、加速、变向、向后、带球等剥夺球员自主决策的指令。',
  '不得对任何人有打骂、指挥式命令、讽刺、威胁、嘲笑等负面语言行为。',
  '技术战术指导在**节间休息、中场休息**进行；场边只做简短的鼓励性示意。',
  '保证每一名到场球员的上场时间与位置轮换，如实填写《上场时间记录表》。',
];
const PLAYER_RULES = [
  '尊重对手、队友、执裁人员和观众；赛前赛后与对手握手。',
  '全力以赴，胜不骄、败不馁；大胆尝试，不怕失误。',
  '诚实比赛：球出界、碰手球主动承认；对手摔倒主动扶起。',
  '服从执裁，有疑问请队长礼貌询问。',
];

// International references used across the documents (for the "参照" notes)
const REFS = [
  ['日本足球协会 JFA', 'U-12 推行 8 人制，场地约 68×50 m、4 号球、自由换人；推广“リーグ戦”联赛文化与“Players First”理念；低龄段（キッズ）节庆式比赛不记录结果与名次。'],
  ['英格兰足总 The FA', '“Future Fit”赛制：U7 3v3、U8–U9 5v5、U10–U11 7v7；无越位、退守线（retreat line）、滚动换人；建议每名球员上场 ≥50%；U11 及以下不公布比分与积分榜；Respect 行为守则。'],
  ['西班牙足协及地区足协 RFEF / FFCV / FCF', '低龄组采用 Fútbol 5 / 7 / 8，分节比赛并要求全员参赛；安达卢西亚足协首创“绿牌（Tarjeta Verde）”表彰公平竞赛。'],
  ['德国足协 DFB', '2024/25 起全国推行儿童足球新赛制：2v2–3v3（G 级）到 5v5–7v7（E 级），小场多球门、轮换上场，低龄段取消冠军联赛。'],
  ['荷兰足协 KNVB / 美国足协 / 澳大利亚 MiniRoos', '6v6 场边引导员、不公布结果；build-out line（退守线）；MiniRoos 全年龄段不记比分、不设积分榜。'],
  ['国际足球理事会 IFAB', '《足球竞赛规则》允许青少年与草根足球使用“暂时罚离（sin bin）”，时长约为比赛时间的 10%–15%。'],
];

module.exports = { ORG, PARENT_RULES, COACH_RULES, PLAYER_RULES, REFS };
