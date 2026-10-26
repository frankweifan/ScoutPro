"""Enrichment round 2: Jiaoyubao (教育宝) Chengdu football listings, fetched 2026-10-26."""
JYB = "https://cd.jiaoyubao.cn/zuqiu/"
JYBM = "https://m.jiaoyubao.cn/cd/zuqiu2/"
JYBB = "https://cd.jiaoyubao.cn/ban/zuqiu/"
E = [
 ("中达舒弘", dict(youth="已证实（有来源）", rating=3.0, rating_platform="教育宝", note_add="教育宝收录为“成都中达舒弘体育培训”（足球培训，评分3.0）", src=[JYBB])),
 ("众禾足球俱乐部", dict(rating=3.0, rating_platform="教育宝", note_add="教育宝收录为“成都众禾足球培训”", src=[JYBB])),
 ("成都大牛体育培训", dict(rating=3.0, rating_platform="教育宝", src=[JYBB])),
 ("皇家贝里斯足球俱乐部（皇贝青训）", dict(legal="成都皇家贝里斯足球俱乐部有限公司；四川皇贝体育发展有限公司（教育宝）",
     address="青羊区光华北一路561号1层（教育宝：成都皇贝体育培训）", note_add="教育宝另列贝森北路1号1栋5层514-1号", src=[JYB, JYBM])),
 ("成都杰冠体育培训", dict(legal="成都杰冠体育文化传播有限公司（教育宝）", src=[JYBM])),
]
ADD = [
 dict(name="四川顶点体育集训基地", brand="顶点体育", district="全市/多区", type="培训机构", youth="待核实（来源未证实青训业务）",
      rating=4.0, rating_platform="教育宝", scale_note="教育宝足球培训频道收录；名称为“集训基地”，可能以体育中考/特长生集训为主",
      sources=[JYBM], confidence="低", status="待核实", note="所在区未注明"),
 dict(name="成都童道型动体育培训", brand="童道型动", district="全市/多区", type="培训机构", youth="已证实（有来源）",
      rating=3.0, rating_platform="教育宝", scale_note="教育宝收录：足球培训，1个网点",
      sources=[JYBB], confidence="低", status="待核实", note="所在区未注明"),
]
