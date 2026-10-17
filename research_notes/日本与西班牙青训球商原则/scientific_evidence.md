# Scientific evidence base for measuring youth "soccer IQ" behaviours from match video (球商行为的视频测量：科学证据)

Notes compiled 2026-10-17. Legend: **[PR]** = peer-reviewed journal; **[CONF]** = conference paper/abstract (not full peer review, or proceedings); **[THESIS]**; **[SECONDARY]** = blog/vendor/media; **[JP]** = Japanese study 日本研究; **[ES]** = Spanish study 西班牙研究. Numbers are reported only where seen in the source text (often abstract-level; flagged where full text was not read).

---

## Q1. Scanning / visual exploratory activity (VEA, 扫描/首振り): operational definitions, benchmark scan rates, youth findings

### Takeaway
The standard operational definition (Jordet school) is "an active head movement where the face (and hence eyes) is temporarily directed away from the ball" to gather information, counted in the ~10 s before the player receives the ball and expressed as scans per second. The best-documented elite benchmark is a mean of 0.44 scans/s (3.0 scans per possession) in an EPL club. Scanning is associated with somewhat better pass completion and forward play, but the effect is small. Youth studies (U13–U19) show the same direction of effects; scan frequency rises with age/level (U19 > U17) and is trainable (Swiss U19 women).

### Cited Findings

**Definitions and coding protocol (定义与编码规则)**
- **[PR] Jordet, Aksum, Pedersen, Walvekar, Trivedi, McCall, Ivarsson & Priestley (2020), *Frontiers in Psychology* 11:553813.** Scan = "active head movement where the face (and hence, the eyes) is temporarily directed away from the ball", intended to gather information about teammates/opponents before engaging the ball. Coding window = the 10 s before the target player receives the ball while his team has possession. If the team won the ball inside that window, the window starts at the moment of regain. For set plays it starts 2 s before the ball is put in play. Metric = scans per second over the window — [PMC7573254](https://pmc.ncbi.nlm.nih.gov/articles/PMC7573254/); [DOI](https://doi.org/10.3389/fpsyg.2020.553813)
- The older Jordet et al. (2013, MIT Sloan) definition was broader: exploratory behaviours are "body and head movements initiated to better see their surroundings" — **[CONF] Jordet, Bloomfield & Heijmerikx, MIT Sloan Sports Analytics Conference (filename indicates SSAC 2013)** — [Sloan page](https://sloansportsconference.com/research-papers/the-hidden-foundation-of-field-vision-in-english-premier-league-epl-soccer-players)
- Aksum et al. (2021) define a scan as a "deliberate head movement away from the ball" to gather information about areas of interest — [FIFA Training Centre research brief (SECONDARY summary of PR paper)](http://www.fifatrainingcentre.com/en/environment/research-brief/high-performance/play/aksum-scanning.php)
- Hintermann et al. (2025) use "an active head movement, during which the player's head was directed away from the ball" — **[PR] *Frontiers in Sports and Active Living*** — [DOI 10.3389/fspor.2025.1602099](https://doi.org/10.3389/fspor.2025.1602099)
- Sensor-based alternative: McGuckian et al. measure head turns (left/right head rotations) with head-mounted inertial measurement units (IMU), plus "head-turn excursion" (amplitude), in the 10 s before possession — **[PR] McGuckian, Cole, Jordet, Chalkley & Pepping (2018), *Frontiers in Psychology* 9:2520** — [DOI](https://doi.org/10.3389/fpsyg.2018.02520)
- Note: the user-quoted phrasing "a body and/or head movement in which the player's face is temporarily directed away from the ball" merges the 2013 (body + head) and 2020 (head, face away from ball) definitions. The exact combined wording was not seen in the sources read.

**Reliability of video coding (编码信度)**
- Jordet et al. 2020: 784 possessions double-coded. Scan count ICC = 0.979. Individual coder ICCs 0.825–0.993 (mean 0.960). Opponent-pressure ICC = 0.981. Cohen's κ: pass type 0.867, action type 0.851, action direction 0.916, successful action 0.978 — [PMC7573254](https://pmc.ncbi.nlm.nih.gov/articles/PMC7573254/)

**Elite benchmarks (精英基准值)**
- EPL club, 27 players, 21 matches, 9,574 possessions: mean **3.0 (±2.1) scans per possession = 0.44 (±0.30) scans/s** — Jordet et al. 2020 — [PMC7573254](https://pmc.ncbi.nlm.nih.gov/articles/PMC7573254/)
- By position: central midfielders scan most, forwards least (Kruskal–Wallis H = 669.97, p < 0.001, d = 0.55). Pairwise d ranges from 0.16 (central defenders vs wingers) to 0.56 (central midfielders vs side defenders). Per-position means appear only in a figure and were not extracted — same source
- By action type: before a pass 0.45 scans/s (N = 8,760), dribble 0.39, receiving 0.35, finishing 0.27. Direction: forward 0.46, sideward 0.43, backward 0.42 (trivial differences). Long penetrative passes had the highest scanning — same source
- Pressure: scanning lowest when the nearest opponent is 0–1 m away and rises with distance up to ~4 m (H = 319.90, d = 0.37; 0–1 m vs 10+ m d = 0.57) — same source
- Outcomes: possession maintained 0.46 vs lost 0.37 scans/s (d = 0.20). Pass completed 0.46 vs not completed 0.40 (d = 0.15). Bayesian model: scanning effect on pass completion μβ = 0.13 ± 0.06 after controlling for pass difficulty. The share of players with a positive effect is ~86% (mean estimate). The authors call the role of scanning in performance "small, but positive" — same source
- Game state effect trivial (losing 0.46 / drawing 0.44 / winning 0.45; d = 0.08) — same source
- 2013 EPL PlayerCam study: 118 midfielders/forwards, 1,279 game situations. Exploration frequency was positively related to pass completion, with the largest effect for midfielders making forward passes, and the "best players" (award winners) explored more — [Sloan page](https://sloansportsconference.com/research-papers/the-hidden-foundation-of-field-vision-in-english-premier-league-epl-soccer-players)
- **[SECONDARY]** Widely repeated numbers from the 2013 study (not verified in the primary text): the "much" exploration band is 0.41–1.80 explorations/s and "some" is 0.21–0.40. The highest band completed ~17% more passes than the lowest. Top scanners were Lampard 0.62/s and Gerrard 0.61/s — [mojo.sport](https://mojo.sport/coachs-corner/what-is-scanning)
- Eye-tracking (in-situ, 11v11): 4 elite midfielders. Fixations occurred in only ~2.3% of scans. The information is concentrated at the scan's stop point, and more opponents than teammates were in view. Scan duration depended on ball context — **[PR] Aksum et al. (2021), *PLOS ONE* 16(8)** — [PMC8378692](https://pmc.ncbi.nlm.nih.gov/articles/PMC8378692/); [DOI 10.1371/journal.pone.0244118](https://doi.org/10.1371/journal.pone.0244118)

**Youth findings (青少年研究)**
- **[PR] Aksum, Pokolm, Bjørndal, Rein, Memmert & Jordet (2021), *Journal of Sports Sciences* 39(21):2401–2410.** 53 outfield players from the four finalists of the 2018 UEFA U17 and U19 Euros, 1,686 possessions. U19 players scanned more than U17. Positional differences were significant. Tighter pressing reduced scanning. Scan frequency was positively associated with pass completion. No numeric means appear in the summary read — [DOI 10.1080/02640414.2021.1935115](https://doi.org/10.1080/02640414.2021.1935115); [FIFA research brief](http://www.fifatrainingcentre.com/en/environment/research-brief/high-performance/play/aksum-scanning.php)
- **[PR] McGuckian, Cole, Chalkley, Jordet & Pepping (2020), *Journal of Sports Sciences* 38(6):658–668.** 22 competitive-elite youth players (mean age ~16.25), 1,623 min of 11v11, IMU + GPS + notation. Exploration was greatest when the player had the ball and lowest during transitions. By pitch zone it was highest in the defensive third and lowest in the middle third — [DOI 10.1080/02640414.2020.1723375](https://doi.org/10.1080/02640414.2020.1723375); [ACU open manuscript](https://acuresearchbank.acu.edu.au/item/8q39q/constraints-on-visual-exploration-of-youth-football-players-during-11v11-match-play-the-influence-of-playing-role-pitch-position-and-phase-of-play)
- **[PR] McGuckian et al. 2018 (32 semi-elite players, 783 actions, 11v11, IMU):** above-average head-turn frequency/excursion before receiving was associated with higher likelihood of turning with the ball, passing forward, and passing to the area opposite the receiving side. Head-turn frequency and excursion were strongly related — [DOI 10.3389/fpsyg.2018.02520](https://doi.org/10.3389/fpsyg.2018.02520)
- **[PR] McGuckian et al. (2020), *Science and Medicine in Football* (U13 vs U23, Footbonaut passing task):** more head turns before receiving, and fewer once in possession, were linked to faster passing performance — [ACU record](https://acuresearchbank.acu.edu.au/item/8w1zv/the-association-between-visual-exploration-and-passing-performance-in-high-level-u13-and-u23-football-players) (DOI not verified)
- **[PR] Eldridge, Pulling & Robins (2013), *Journal of Human Sport and Exercise* 8(3):560–577.** 3 youth central midfielders, five 20-min training games, player-cam. Pre-reception scanning was associated with more forward passes, more passes into the attacking half, fewer defensive pressures, and more turns (p < 0.01). The sample is very small — [Chichester eprint](https://eprints.chi.ac.uk/id/eprint/992/)
- Jordet et al. 2020 summarise prior work: Eldridge et al. 2013 found scanning linked to forward passes and less pressure but not to maintained possession. McGuckian 2018/2019 found head-turn frequency linked to faster passes and more forward passes but not to pass success — [PMC7573254](https://pmc.ncbi.nlm.nih.gov/articles/PMC7573254/)
- Trainability: **[PR] Jordet (2005), *Journal of Applied Sport Psychology* 17(2):140–156**, imagery intervention with 3 elite players (single-case multiple-baseline, close-up match video). VEA increased in 2 players, but only 1 marginally improved on-ball performance — [DOI 10.1080/10413200590932452](https://doi.org/10.1080/10413200590932452); [record](https://lida.sport-iat.de/dfb/Record/4010064?lng=en). A follow-up PETTLEP imagery intervention (Pocock et al., 5 elite academy players, 6 weeks) improved VEA, especially in central midfielders — [St Mary's accepted version](https://research.stmarys.ac.uk/id/eprint/1881/7/Pocock%20et%20al.%20JASP%20Accepted%20Version.pdf)
- **[PR] Hintermann et al. 2025:** 36 Swiss U19 female players (16.7 ± 1.2 y), 5-week scanning programme, 4v4 video coding. Scans per game situation increased in the intervention group (p = 0.002) and not in controls (p = 0.088). The increase was significant in elite (p = 0.001) but not grassroots players, and it was maintained at the 3-week retention test. Elite players made more successful actions after scanning than grassroots players (p = 0.011), but the intervention effect on success was not significant (p = 0.074) — [DOI 10.3389/fspor.2025.1602099](https://doi.org/10.3389/fspor.2025.1602099)
- **[PR] Swiss U19 female players, verbal "head up"-type instructions in 4v4** (25 players): instructions significantly increased the number of scans before receiving — *Current Issues in Sport Science* (2025) — [DOAJ](https://doaj.org/article/26e65fa57566473ca5f83436a9fa259b)

**Japanese studies [JP] (日本研究：首振り/視覚探索)**
- **[JP][CONF] 夏原隆之, 國部雅大, 三枝巧, 小嶋岳, 松竹貴大, 小井土正亮, 中山雅雄 (2023)**, 「サッカーにおける首振り行動に関するセンサーベースの検出手法開発の試み」, 日本体育・スポーツ・健康学会予稿集 73. Motion sensors count head scans in small-sided games and are compared against manual observer coding — [DOI 10.20693/jspehssconf.73.0_283](https://doi.org/10.20693/jspehssconf.73.0_283)
- **[JP][PR] 小泉洋生 & 中山雅雄 (2025)**, 体育学研究 70:141–156, turn-success model for receptions "between the lines" (ライン間). 1,260 plays from the 2018 World Cup. Predictors include presence/absence of visual exploratory activity, defender/midfielder distance and pressing speed, pass type/speed/angle. Logistic regression prediction accuracy was 77.1%. Individual odds ratios are not in the abstract — [DOI 10.5432/jjpehss.008-24046](https://doi.org/10.5432/jjpehss.008-24046)
- **[JP][PR] Natsuhara, Kato, Nakayama, Yoshida, Sasaki, Matsutake & Asai (2020)**, *Perceptual and Motor Skills* 127(2):468–489. Life-size 5v4 film simulation with eye-tracking. High-level players made better pass decisions than middle-level players and attended more to unmarked attackers, the receiving teammate and opponents — [DOI 10.1177/0031512519900057](https://doi.org/10.1177/0031512519900057)
- **[JP][PR] 夏原隆之 他 (2017)**, review 「サッカーの状況判断における知覚認知スキルの研究動向と今後の課題」, コーチング学研究 31(1) — [DOI 10.24776/jcoaching.31.1_1](https://doi.org/10.24776/jcoaching.31.1_1)
- **[JP][CONF] 浦佑大 & 高井秀明 (2022)**, VR decision-making and visual search. Experienced players show 「特徴的な視覚探索」 enabling quick responses — [DOI 10.20693/jspehssconf.72.0_244](https://doi.org/10.20693/jspehssconf.72.0_244)
- **[JP] 加藤弘 & 岡村孝之 (2004)**, 和歌山大学教育学部 教育研究センター紀要 14:185–189, field of view in trapping/passing. Keywords include 首振り回数 and ルックアップ. Results not seen — [repository](https://repository.center.wakayama-u.ac.jp/415)

### Inferences
- For a video tool, the most defensible scan definition is Jordet 2020's (head movement with face away from the ball), counted in the 10 s pre-reception window (truncated at regain), reported as scans/s, and stratified by position and opponent distance. Raw scan rates confound role and pressure.
- 0.44 scans/s is an adult elite (EPL) mean, not a youth target. Youth rates likely sit below it and rise with age (U19 > U17), but no youth scans/s means were extracted, so age-specific thresholds should not be invented.
- Effect sizes for performance are small (d ≈ 0.15–0.20), so scan rate should be presented as a process indicator, not a performance score.

### Gaps
- Numeric youth benchmarks (scans/s by U13/U15/U17/U19) were not found in the texts read. Aksum et al. 2021 and McGuckian 2020 full texts are needed.
- A 3v3 U15 defensive-VEA study (successful sequences 0.267 vs unsuccessful 0.152) appeared in a search snippet, but the source could not be identified reliably, so it is excluded.
- J-STAGE full texts (e.g. 夏原 2023 sensor study accuracy) were not accessible. Japanese peer-reviewed papers specifically on youth 首振り frequency were not found.

---

## Q2. Body orientation / open body shape when receiving (接球身体朝向/半转身)

### Takeaway
Peer-reviewed match-performance evidence isolating receiver body orientation is thin. The strongest quantitative work is computational: Spanish (UPF/FC Barcelona-linked) papers show orientation improves pass-feasibility models and can be estimated from video. Japanese and Spanish observational studies include orientation-related variables.

### Cited Findings
- **[ES][PREPRINT/CONF] Arbués-Sangüesa, Martín, Fernández, Ballester & Haro (2020)**, "Using Player's Body-Orientation to Model Pass Feasibility in Soccer". A receiver who is close and unmarked can still struggle to receive if facing away. Adding an orientation-feasibility term significantly improved the pass-feasibility model, and the combination of all feasibility measures outperformed individual ones — [arXiv 2004.07209](https://arxiv.org/pdf/2004.07209)
- **[ES][PREPRINT] Arbués-Sangüesa et al. (2020)**, "Always Look on the Bright Side of the Field", estimates player orientation from monocular broadcast video by merging pose estimation with ball/contextual data — [arXiv 2003.00943](https://arxiv.org/pdf/2003.00943)
- **[ES][PREPRINT] "Learning Football Body-Orientation as a Matter of Classification" (2021)**: CNN with cyclic loss, trained on labels from wearable tracking devices. Median error < 12° per player — [arXiv 2106.00359](https://arxiv.org/abs/2106.00359)
- **[ES] Defensive orientation, Euro 2012** (Catalan; University of Vic): 572 situations. Body orientation was adequate in 64% and inadequate in 36%. The authors conclude orientation is important for defensive anticipation — [UVic repository](https://repositori.uvic-ucc.cat/handle/10854/2453)
- **[SECONDARY]** Barça Innovation Hub: player orientation as a key aspect of predictive models — [BIH](https://elearning.barcainnovationhub.com/player-orientation-a-key-aspect-of-predictive-models-in-football/). FIFA session plan (coaching material) states that receiving stance/orientation affects close control and signals where to pass — [FIFA PDF](https://www.fifatrainingcentre.com/media/native/test/FIFA_Session_Plan_D%C3%BCnker_first_touch-new-1.pdf)
- Scanning studies use "turning with the ball" and "forward pass" as outcomes, which proxy an open receiving orientation (McGuckian 2018; Eldridge 2013) — [DOI](https://doi.org/10.3389/fpsyg.2018.02520); [Chichester](https://eprints.chi.ac.uk/id/eprint/992/)

### Inferences
- A practical video metric: receiver torso/hip angle relative to the goal line or the passer at the moment of the pass and at the first touch, coded as closed/half-open/open (e.g. bins of the angle). It can be validated against "turn/forward action" outcomes. Automated estimation is feasible (< 12° median error in research settings).

### Gaps
- No peer-reviewed youth study was found that quantifies receiving orientation and links it to performance with benchmarks by age.

---

## Q3. Decision-making quality and speed (决策质量与速度): GPAI, FUT-SAT, TacticUP, video tests, reliability

### Takeaway
Validated observational instruments exist: GPAI, FUT-SAT, and the Spanish GPET and invasion-games tools. All rely on trained raters, with inter-/intra-observer agreement typically reported as κ or ICC > 0.7–0.8. Video-based off-field tests (TacticUP) give test–retest κ 0.62–1.0. Spanish research consistently finds that young players "do" (procedural decisions) better than they can "say" (declarative knowledge).

### Cited Findings
- **GPAI [PR] Oslin, Mitchell & Griffin (1998)**, *Journal of Teaching in Physical Education* 17(2):231–243. Codes decision making, skill execution and support as appropriate/inappropriate; indices = appropriate/(appropriate + inappropriate) — [DOI 10.1123/jtpe.17.2.231](https://doi.org/10.1123/jtpe.17.2.231). (Original reliability coefficients not seen.) A critique of the index calculations (Memmert & Harvey 2008) recommends raw scores rather than ratios; seen only via a secondary summary — [Prezi (SECONDARY)](https://prezi.com/dryklkbaeaao/gpai-game-performance-assessment-instrument/?fallback=1)
- **[ES][PR] Spanish invasion-games instrument (UCM/UA):** intra-observer reliability > 0.7 for all variables except receptive decision making (0.537), a warning that "decision at reception" is the hardest item to code reliably — [UCM record](https://produccioncientifica.ucm.es/documentos/678566520831ea00f9033cbd)
- **[ES][PR] GPET (Game Performance Evaluation Tool) in Soccer**, Spanish development/validation — [ULL portal](https://portalciencia.ull.es/documentos/5d5ba73d2999520e90d1068e) (coefficients not extracted)
- **FUT-SAT [PR] Costa, Garganta, Greco, Mesquita & Maia (2011)**, *Motricidade*. Scores 10 core tactical principles (5 offensive, 5 defensive) in a field test (GK+3v3+GK). Intra- and inter-observer reliability > 0.79. Correlations with coaches' evaluations > 0.63 — [Motricidade](https://revistas.rcaap.pt/motricidade/article/view/121)
- FUT-SAT age comparison: Borges et al. (2017), *Journal of Human Kinetics* 58:207–214, 48 male players across three age groups. Inter-rater re-analysis of 10.2% of actions with agreement > 81% — [PMC5548168](https://pmc.ncbi.nlm.nih.gov/articles/PMC5548168); [DOI 10.1515/hukin-2017-0078](https://doi.org/10.1515/hukin-2017-0078). Brazilian U14 vs U15: U15 performed less "width and length" and "concentration" but more "offensive unity" — [RBCM](https://portalrevistas.ucb.br/index.php/rbcm/article/download/5169/3865/25345)
- **TacticUP [PR] Machado & Teoldo da Costa (2020)**, *Frontiers in Psychology* 11:1690. Video clips of 11v11 offensive and defensive situations; the player picks the best option. Content validity from 9 experts in 4 countries. Experts outscored non-experts on 10 of 15 variables. Test–retest Cohen's κ = 0.622–1.0 — [DOI 10.3389/fpsyg.2020.01690](https://doi.org/10.3389/fpsyg.2020.01690); [PMC7422863](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7422863/)
- **[ES][PR] González-Víllora, García-López, Pastor-Vicedo & Contreras-Jordán (2011)**, *Revista de Psicología del Deporte*: 13 Albacete Balompié U10 players, video-coded 3v3 plus knowledge interviews. Decision making and execution exceeded declarative domain knowledge — [UAB DDD](https://ddd.uab.cat/record/70180)
- **[ES][PR] González-Víllora et al. (2010)**, *Infancia y Aprendizaje*: 14 Albacete U12 players, 5v5 plus interviews. High performance, especially in decision making, with theoretical knowledge lagging — [REDINED](https://redined.educacion.gob.es/xmlui/handle/11162/80831)
- **[ES][PR] Real Sociedad academy (2024, *Apunts*)**: declarative tactical knowledge by playing position, 163 players (~16.7 y) — [record](https://research.science.eus/documentos/66fae61e39f11b4c6fbead1a)
- **[ES][PR] U10 vs U12 elite Spanish players (LaLiga tournament)**, 1,247 individual possessions. U10s had higher odds of running with the ball versus passing than U12s — [PMC9693199](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9693199/)
- **Decision speed [JP][PR]**: Natsuhara et al. 2020 (above), plus a 2024 *Brain Sciences* study (Natsuhara co-author) reporting faster, less variable pass-decision reaction times and stronger inhibitory control in higher-skilled Japanese university players. Seen via a search summary only; no stable URL was captured, so treat as unverified.

### Inferences
- For match-video "decision quality", a GPAI-style appropriate/inappropriate coding with ≥2 raters and κ/ICC reporting is the methodological norm. Decision speed can be operationalised as time from first touch (or reception) to release, conditioned on pressure.
- Receiving-moment decisions have the weakest reliability (0.537), so the tool should give coders explicit rules for that moment.

### Gaps
- No age-normed benchmarks were found for decision-quality indices from match video. TacticUP and FUT-SAT norms by age were not extracted.

---

## Q4. Number of options / affordances, off-ball movement, pitch-control models (选项数/可供性、无球跑动、控球区域模型)

### Takeaway
Passing options and space creation are measured mainly with tracking-data models (pitch control, pass probability, space generation, off-ball scoring opportunity). Most of these are conference or industry work rather than peer-reviewed. "Decoy runs" have no validated academic definition; vendors use proprietary run taxonomies.

### Cited Findings
- Pitch control: "the probability that a player can control the ball, assuming it was at this location" (W. Spearman, Liverpool). Off-ball scoring opportunity (OBSO) extends pitch control to value off-ball movement — [Training Ground Guru (SECONDARY)](https://archive.trainingground.guru/articles/william-spearman-how-liverpool-create-pitch-control). "Beyond Expected Goals" (Spearman 2018) is cited by SciSports — [SciSports](https://support.scisports.com/en/articles/3584444-spc-potential). The venue was not confirmed. A tutorial implementation of pass probability exists — [Soccermatics](https://soccermatics.readthedocs.io/en/latest/lesson6/PassProbability.html)
- **[ES][CONF] Fernández & Bornn**, "Wide Open Spaces": a statistical technique quantifying space occupation and space generation by off-ball movement (PDF labelled 2017) — [PDF mirror](https://code.garrettmills.dev/Archives/papers-we-love_papers-we-love/raw/commit/6f92d68b5e4bea94d9453e93e3801b6fd2dbb49a/sports_analytics/2017-A-statistical-technique-for-measuring-space-creation-in-professional-soccer.pdf)
- **[PR] Martens, Dick & Brefeld (2021)**, "Space and Control in Soccer", *Frontiers in Sports and Active Living*: data-driven pitch control/value and a new space-generation measure — [DOI 10.3389/fspor.2021.676179](https://doi.org/10.3389/fspor.2021.676179)
- Orientation-aware pass feasibility for counting realistic options (Arbués-Sangüesa et al. 2020) — [arXiv 2004.07209](https://arxiv.org/pdf/2004.07209)
- **[SECONDARY]** World Cup 2022 (Gradient tracking): a "causal" space-creating run is one where a dragged defender among the three closest to the pass target moved ≥1 m further away by the time of the pass. 405/3,142 runs (12.9%) qualified, with ~3.3 runners per pass; "ghost runs" are runners who found space and were ignored — [The Cutback blog](https://the-cutback.beehiiv.com/p/off-ball-movement-football-tracking-data). Run detection thresholds: >15 km/h with ≥2.5 m/s² acceleration, or >20 km/h — [Gradient Sports blog](https://www.gradientsports.com/blog/measuring-off-ball-movement-using-broadcast-tracking-event-data)
- **[SECONDARY]** SkillCorner detects 10 off-ball run types. For centre-forwards, runs in behind are 32%, cross-receiver runs 23% and runs ahead of the ball 22% — [SkillCorner](https://skillcorner.com/blog/forward-off-ball-runs)

### Inferences
- A video tool can count "options" as teammates with pass probability or pitch control above a threshold at the moment of reception. This requires homography plus tracking of all players, not just the focal player.

### Gaps
- No peer-reviewed youth benchmarks were found for number of options or off-ball run frequency. Decoy-run definitions are proprietary.

---

## Q5. First touch quality and deception (第一脚触球质量、假动作)

### Takeaway
Reception quality is usually rated by coaches against criteria; one small U18 study supports reliability across game formats. Deception research is mostly lab-based (video occlusion/anticipation) rather than match coding.

### Cited Findings
- **[PR] Sørensen, Sørensen & Dalen (2021)**, *Sports*: 13 male U18 players, coach-scored reception quality. Scores correlated between 4v1 and 5v5 (rs = −0.61). There was a weaker trend versus an isolated ball-projection test (rs = −0.48, p = 0.10). Reception frequency in 5v5 correlated with reception score (rs = −0.70). The authors note a lack of studies on reception technique — [PMC8156114](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8156114/)
- **[PR] Wright & Jackson (2014)**, *PLoS ONE* "Deceptive body movements reverse spatial cueing in soccer": less-skilled players were below chance on deceptive step-over turns. Higher-skilled players were more accurate but still impaired — [Loughborough repository](https://repository.lboro.ac.uk/articles/journal_contribution/Deceptive_body_movements_reverse_spatial_cueing_in_soccer/9618764/1)
- **[PR] Jackson, Barton, Ashford & Abernethy (2018)**, *Frontiers in Psychology*, "Stepovers and signal detection" (sensitivity vs bias for deceptive actions) — [PDF](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.02043/pdf)
- Bishop, Wright, Jackson & Abernethy (2013, *J Sports Sci*, fMRI occlusion with stepovers) and Jackson, Warren & Abernethy (2006, *Acta Psychologica*, rugby sidestep) are foundational but were seen only via search listings — [Brunel record](https://bura.brunel.ac.uk/handle/2438/9841)

### Gaps
- No validated match-video coding scheme for deception success (e.g. defender displaced by feint) was found, nor youth benchmarks for first-touch quality in matches.

---

## Q6. Transition reaction / counter-pressing (攻防转换反应、反抢)

### Takeaway
"Defensive reaction time" (time from losing to regaining the ball) is the main peer-reviewed metric. Top Bundesliga teams regain about 1 s faster. Short defensive transitions (≤15 s) predict direct regains. Youth data are lacking.

### Cited Findings
- **[PR] Vogelbein, Nopp & Hökelmann (2014)**, *Journal of Sports Sciences* 32: 1076–1083, all 306 games of the 2010/11 Bundesliga. Top teams regained possession quickest, roughly 1 s faster than other groups in every match status. All groups were fastest when trailing — [DOI 10.1080/02640414.2013.879671](https://doi.org/10.1080/02640414.2013.879671) (issue number not verified)
- **[ES][PR] 2010 World Cup defensive transitions (University of Barcelona)**: 804 transitions. Transitions lasting 0–15 s were associated with higher chance of direct regain — [UB repository](https://diposit.ub.edu/items/94588039-0f93-4812-9e6c-930f16896fb5/full)
- **[ES][PR] *Journal of Human Sport and Exercise* (2021)**: the model with the best chance of regaining possession had a defensive transition ≤15 s, ending in the defensive-midfield zone with the attacking team under pressure — [UB PDF](https://diposit.ub.edu/dspace/bitstream/2445/181574/1/716151.pdf)
- McGuckian 2020: youth players scan least during transitions, so transitions may be a perceptual weak point — [DOI](https://doi.org/10.1080/02640414.2020.1723375)
- **[SECONDARY]** Soccerment "Gegenpressing Intensity": losses in the attacking 40% of the pitch trigger a check for defensive actions within 6 s — [Soccerment](https://blog.soccerment.com/?p=27977)

### Inferences
- A per-player metric could be time from team ball loss to the player's first pressing action (or closing distance to the ball carrier) within a 5–6 s window. Team-level time-to-regain can follow Vogelbein's method.

### Gaps
- No peer-reviewed study validating the "5-second rule" and no youth transition-time benchmarks were found.

---

## Q7. On-pitch verbal communication (场上语言沟通)

### Takeaway
There is little match-observation research on player-to-player talk in youth soccer. Evidence comes from controlled tasks, coach-instruction studies and other sports.

### Cited Findings
- **[PR] *Frontiers in Psychology* (2019)**: 46 U18/U21 players in dyads. Shared knowledge increased with practice while overall verbal communication, and orienting information specifically, decreased — [DOAJ](https://doaj.org/article/0bff04209448404886362257fd7d089a)
- **[PR] *Journal of Human Kinetics***: communication and passing contributions by playing position in a professional team (network approach) — [JHK](https://jhk.termedia.pl/The-Communication-and-Passing-Contributions-of-Playing-Positions-in-a-Professional,158508,0,2.html)
- **[PREPRINT]** Coach verbal instruction in U13 small-sided games: mostly direct instructions (~90%) helped defensive but hurt offensive tactical behaviour — [SciELO preprint](https://preprints.scielo.org/index.php/scielo/preprint/download/5796/11152/11711)
- An adjacent netball method video- and audio-recorded play and coded communication frequency — [QUT eprint](https://eprints.qut.edu.au/228656/1/106290388.pdf)

### Gaps
- No validated youth soccer match-coding scheme or frequency benchmarks for player talk were found. Audio capture from broadcast-style video is also generally impractical.

---

## Q8. Behaviour after errors / resilience (失误后的行为、心理韧性)

### Takeaway
A recent qualitative study provides an observable behaviour list for academy resilience, including reactions to mistakes. Errors are a top stressor for adolescent academy players. No validated quantitative match-coding tool exists yet.

### Cited Findings
- **[PR] Nottingham Trent University group, *Journal of Applied Sport Psychology* (~2024)**, "Exploring the behavioral indicators of resilience in professional academy youth soccer": focus groups/interviews with 60 people from six academies and one governing body, using video-clip prompts. 36 behaviours in six themes: teammate support, emotion, effort, rebound, robustness, learning. Examples include positive reaction to a mistake and verbal support of teammates after errors. The authors are developing a validated observation tool — [CORE](https://core.ac.uk/outputs/613036558); [NTU news](https://www.ntu.ac.uk/about-us/news/news-articles/2024/08/study-reveals-key-resilience-behaviours-in-young-footballers)
- **[PR] Reeves et al.**, academy players aged 12–18 (n = 40): making errors was a salient stressor, more prominent in middle adolescence, and coping differed between age groups — [Hull repository](https://hull-repository.worktribe.com/output/387026)
- **[THESIS]** Portuguese study of 10 athletes aged 11–15: past mistakes affected current perception of performance, confidence and motivation — [UFP](https://bdigital.ufp.pt/entities/publication/bd8cd971-15c0-41c5-97fc-26867b5bdc49)

### Inferences
- Codable video proxies drawn from the NTU list: time to re-engage (e.g. sprint or press within X s after own error), body language (head down, gestures), teammate support. These are observable but unvalidated.

### Gaps
- No inter-rater reliability or age benchmarks for post-error behaviours.

---

## Q9. Automation: detecting scanning/head and body orientation from video, pose estimation (自动化检测)

### Takeaway
Body orientation from broadcast video is a solved-in-research problem (< 12° median error). Head-scan detection from broadcast video has no validated published method. Japanese and Australian groups detect scans with IMU sensors instead.

### Cited Findings
- Body orientation classification, median error < 12° — [arXiv 2106.00359](https://arxiv.org/abs/2106.00359); pose plus context orientation — [arXiv 2003.00943](https://arxiv.org/pdf/2003.00943)
- IMU-based head-turn measurement (McGuckian 2018/2020) — [DOI](https://doi.org/10.3389/fpsyg.2018.02520); **[JP]** sensor-based 首振り detection validated against observers (夏原 et al. 2023) — [DOI](https://doi.org/10.20693/jspehssconf.73.0_283)
- Head pose estimation for soccer from high-speed video (Loughborough) — [repository](https://repository.lboro.ac.uk/articles/conference_contribution/Deep_learning_head_pose_estimation_for_soccer_head_impact_measurement_from_high_speed_video/27051409/1). DeepImpact header detection in broadcast video had 95.3% sensitivity in cross-validation but 21.1% precision on an independent test set (*Scientific Reports* 2022), a caution on precision in real footage — [PMC9166706](https://pmc.ncbi.nlm.nih.gov/articles/PMC9166706)
- Eye-tracking shows information is gathered mainly at the scan's stop point with few fixations (Aksum 2021 PLOS ONE). Head-yaw change is therefore a reasonable proxy for a scan — [PMC8378692](https://pmc.ncbi.nlm.nih.gov/articles/PMC8378692/)

### Inferences
- A pipeline of player tracking, then head-yaw estimation (pose keypoints: nose/ears relative to shoulders), then detection of yaw excursions away from the ball direction in the 10 s pre-reception window would mirror Jordet's definition. It needs validation against manual coding (target ICC ≥ 0.9, as in Jordet 2020). Youth amateur footage (single wide camera, low resolution) will make head keypoints unreliable.

### Gaps
- No published accuracy figures for scan detection from broadcast/wide-angle video. No validated pass-option counting on youth footage.
