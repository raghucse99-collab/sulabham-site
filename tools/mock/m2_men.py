from mk import *
import math
S="men"
ASM=[("Only I is implicit","I మాత్రమే అంతర్లీనం"),("Only II is implicit","II మాత్రమే అంతర్లీనం"),("Both I and II are implicit","I, II రెండూ అంతర్లీనం"),("Neither I nor II is implicit","I, II రెండూ అంతర్లీనం కావు")]
ARG=[("Only argument I is strong","వాదన I మాత్రమే బలమైనది"),("Only argument II is strong","వాదన II మాత్రమే బలమైనది"),("Both I and II are strong","I, II రెండూ బలమైనవి"),("Neither I nor II is strong","I, II రెండూ బలమైనవి కావు")]
CON=[("Only conclusion I follows","ముగింపు I మాత్రమే అనుసరిస్తుంది"),("Only conclusion II follows","ముగింపు II మాత్రమే అనుసరిస్తుంది"),("Both I and II follow","I, II రెండూ అనుసరిస్తాయి"),("Neither I nor II follows","I, II రెండూ అనుసరించవు")]
COA=[("Only course of action I follows","చర్య I మాత్రమే అనుసరణీయం"),("Only course of action II follows","చర్య II మాత్రమే అనుసరణీయం"),("Both I and II follow","I, II రెండూ అనుసరణీయం"),("Neither I nor II follows","I, II రెండూ అనుసరణీయం కావు")]
# figure: a square with both diagonals
SQX='<svg viewBox="0 0 180 180" width="180" height="180" role="img" aria-label="figure"><g fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 15 H165 V165 H15 Z"/><path d="M15 15 L165 165 M165 15 L15 165"/></g></svg>'
# pie chart: monthly spending of a family (total Rs 40,000)
_PIE=[("Food / ఆహారం",35,"#2c6e8f"),("Rent / అద్దె",25,"#c0703a"),("Education / విద్య",15,"#5b8c3a"),("Transport / రవాణా",10,"#8a5a9e"),("Savings / పొదుపు",15,"#b8a03a")]
def U(ue,ut,*v):return [("%s %s"%(x,ue),"%s %s"%(x,ut)) for x in v]
def _pie():
    cx,cy,r=80,85,70;a0=-90.0;out=[]
    for i,(lab,v,c) in enumerate(_PIE):
        a1=a0+v*3.6
        x0,y0=cx+r*math.cos(math.radians(a0)),cy+r*math.sin(math.radians(a0))
        x1,y1=cx+r*math.cos(math.radians(a1)),cy+r*math.sin(math.radians(a1))
        out.append('<path d="M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" fill="%s" stroke="#fff" stroke-width="1.5"/>'%(cx,cy,x0,y0,r,r,1 if v>50 else 0,x1,y1,c))
        out.append('<rect x="168" y="%d" width="12" height="12" fill="%s"/><text x="186" y="%d">%s — %d%%</text>'%(22+i*28,c,32+i*28,lab,v))
        a0=a1
    return ('<svg viewBox="0 0 340 175" width="340" height="175" role="img" aria-label="pie chart"><g font-family="sans-serif" font-size="11" fill="currentColor">'+''.join(out)+'</g></svg>')
PIE=_pie()
# line graph: two-wheeler production of a company (thousand units)
_LN=[("2022",120),("2023",150),("2024",135),("2025",180)]
def _line():
    X=lambda i:60+i*70;Y=lambda v:160-(v-100)*1.4
    pts=' '.join('%d,%.1f'%(X(i),Y(v)) for i,(y,v) in enumerate(_LN))
    s='<line x1="40" y1="160" x2="290" y2="160" stroke="currentColor"/><line x1="40" y1="20" x2="40" y2="160" stroke="currentColor"/>'
    s+='<polyline points="%s" fill="none" stroke="#2c6e8f" stroke-width="2.5"/>'%pts
    for i,(y,v) in enumerate(_LN):
        s+='<circle cx="%d" cy="%.1f" r="4" fill="#2c6e8f"/><text x="%d" y="%.1f" text-anchor="middle" font-weight="700">%d</text><text x="%d" y="176" text-anchor="middle">%s</text>'%(X(i),Y(v),X(i),Y(v)-9,v,X(i),y)
    return '<svg viewBox="0 0 300 190" width="300" height="190" role="img" aria-label="line graph"><g font-family="sans-serif" font-size="12" fill="currentColor">'+s+'</g></svg>'
LINE=_line()
Q=[
q("men-log-1","m","Statement: The school has announced extra classes on Saturdays for Class X students before the board examinations. Which of the following assumptions is/are implicit in the statement?","వాక్యం: బోర్డు పరీక్షలకు ముందు పదో తరగతి విద్యార్థులకు శనివారాల్లో అదనపు తరగతులు నిర్వహిస్తామని పాఠశాల ప్రకటించింది. ఈ వాక్యంలో అంతర్లీనంగా ఉన్న ఊహ(లు) ఏది/ఏవి?",
  ASM,0,
  "I is implicit: a school arranges extra classes only because it expects them to help students do better. II is not implicit: extra classes can be useful even when students do study at home — the statement says nothing about their home study.",
  "I అంతర్లీనం: అదనపు తరగతులు విద్యార్థులు బాగా రాయడానికి ఉపయోగపడతాయని భావించినందుకే పాఠశాల వాటిని ఏర్పాటు చేస్తుంది. II అంతర్లీనం కాదు: విద్యార్థులు ఇంట్లో చదువుకున్నా అదనపు తరగతులు ఉపయోగపడవచ్చు — ఇంటి చదువు గురించి వాక్యం ఏమీ చెప్పడం లేదు.",
  [("I. The extra classes will help the students perform better in the examinations.","I. అదనపు తరగతులు విద్యార్థులు పరీక్షల్లో బాగా రాయడానికి సహాయపడతాయి."),("II. The students do not study at home.","II. విద్యార్థులు ఇంట్లో చదువుకోరు.")]),
q("men-log-1","m","Statement: 'Book your train tickets online and avoid the long queues at the counter.' — an advertisement. Which of the following assumptions is/are implicit?","వాక్యం: 'రైలు టికెట్లు ఆన్‌లైన్‌లో బుక్ చేసుకోండి, కౌంటర్ దగ్గర పొడవైన క్యూలు తప్పించుకోండి.' — ఒక ప్రకటన. అంతర్లీనంగా ఉన్న ఊహ(లు) ఏది/ఏవి?",
  ASM,2,
  "Both are implicit. The advice to book online assumes that online booking is available (I), and the promise to 'avoid long queues' assumes that queues at the counter are long, at least at times (II).",
  "రెండూ అంతర్లీనం. ఆన్‌లైన్‌లో బుక్ చేయమనే సలహా ఆన్‌లైన్ బుకింగ్ అందుబాటులో ఉందని ఊహిస్తుంది (I); 'పొడవైన క్యూలు తప్పించుకోండి' అనే మాట కౌంటర్ దగ్గర కనీసం కొన్నిసార్లైనా క్యూలు పొడవుగా ఉంటాయని ఊహిస్తుంది (II).",
  [("I. Train tickets can be booked online.","I. రైలు టికెట్లను ఆన్‌లైన్‌లో బుక్ చేసుకోవచ్చు."),("II. The queues at the ticket counters are long at least at some times.","II. టికెట్ కౌంటర్ల దగ్గర కనీసం కొన్నిసార్లు క్యూలు పొడవుగా ఉంటాయి.")]),
q("men-log-2","h","Statement: Should all private coaching centres be banned? Which of the following arguments is/are strong?","వాక్యం: అన్ని ప్రైవేటు కోచింగ్ కేంద్రాలను నిషేధించాలా? కింది వాదనల్లో బలమైనది/బలమైనవి ఏది/ఏవి?",
  ARG,1,
  "Only II is strong: it gives a real and important reason against a total ban — many students do not get enough guidance in school. I is weak: dependence on coaching is at most a reason to improve schools or regulate coaching; it does not justify banning ALL centres (an extreme step).",
  "II మాత్రమే బలమైనది: పూర్తి నిషేధానికి వ్యతిరేకంగా నిజమైన, ముఖ్యమైన కారణం ఇస్తుంది — చాలా మంది విద్యార్థులకు పాఠశాలల్లో సరిపడా మార్గదర్శకత్వం లభించదు. I బలహీనం: కోచింగ్‌పై ఆధారపడడం పాఠశాలలను మెరుగుపరచడానికి లేదా కోచింగ్‌ను నియంత్రించడానికి కారణం కావచ్చు; అన్ని కేంద్రాలను నిషేధించడం (తీవ్ర చర్య) సమర్థనీయం కాదు.",
  [("I. Yes. They make students depend on them instead of on their own effort.","I. అవును. విద్యార్థులు సొంత కృషి కంటే వాటిపై ఆధారపడేలా చేస్తాయి."),("II. No. They help many students who do not get enough guidance in their schools.","II. వద్దు. పాఠశాలల్లో సరిపడా మార్గదర్శకత్వం లభించని చాలా మంది విద్యార్థులకు అవి సహాయపడతాయి.")]),
q("men-log-3","m","Statements: All keys are locks. Some locks are doors. Which of the following conclusions follow(s)?","వాక్యాలు: అన్ని తాళంచెవులు తాళాలు. కొన్ని తాళాలు తలుపులు. కింది ముగింపుల్లో ఏది/ఏవి అనుసరిస్తాయి?",
  CON,3,
  "Neither follows. The 'locks' that are doors may be locks that are not keys, so 'some doors are keys' is not certain (I fails). Nothing says every door is a lock — only SOME locks are doors (II fails). Draw the Venn diagram: 'keys' sits inside 'locks', and 'doors' may overlap 'locks' outside 'keys'.",
  "ఏదీ అనుసరించదు. తలుపులైన 'తాళాలు' తాళంచెవులు కాని తాళాలు కావచ్చు; కాబట్టి 'కొన్ని తలుపులు తాళంచెవులు' నిశ్చయం కాదు (I విఫలం). ప్రతి తలుపూ తాళం అని ఎక్కడా లేదు — కొన్ని తాళాలు మాత్రమే తలుపులు (II విఫలం). వెన్ చిత్రం: 'తాళంచెవులు' 'తాళాల' లోపల; 'తలుపులు' తాళంచెవుల బయటి తాళాల భాగాన్ని మాత్రమే తాకవచ్చు.",
  [("I. Some doors are keys.","I. కొన్ని తలుపులు తాళంచెవులు."),("II. All doors are locks.","II. అన్ని తలుపులు తాళాలు.")]),
q("men-log-3","m","Statements: All mangoes are fruits. No fruit is a vegetable. Which of the following conclusions follow(s)?","వాక్యాలు: అన్ని మామిడిపండ్లు పండ్లు. ఏ పండూ కూరగాయ కాదు. కింది ముగింపుల్లో ఏది/ఏవి అనుసరిస్తాయి?",
  CON,0,
  "Only I follows. Mangoes lie completely inside 'fruits', and 'fruits' and 'vegetables' do not touch at all, so no mango can be a vegetable (I). II says the opposite of I ('some vegetables are mangoes'), so it cannot follow.",
  "I మాత్రమే అనుసరిస్తుంది. మామిడిపండ్లు పూర్తిగా 'పండ్ల' లోపల ఉన్నాయి; 'పండ్లు', 'కూరగాయలు' అసలు కలవవు; కాబట్టి ఏ మామిడిపండూ కూరగాయ కాదు (I). II, I కి వ్యతిరేకం ('కొన్ని కూరగాయలు మామిడిపండ్లు'), కాబట్టి అనుసరించదు.",
  [("I. No mango is a vegetable.","I. ఏ మామిడిపండూ కూరగాయ కాదు."),("II. Some vegetables are mangoes.","II. కొన్ని కూరగాయలు మామిడిపండ్లు.")]),
q("men-log-4","e","Statement: A large number of students in a district failed in Mathematics in the Class X examination. Which of the following courses of action follow(s)?","వాక్యం: ఒక జిల్లాలో పదో తరగతి పరీక్షలో పెద్ద సంఖ్యలో విద్యార్థులు గణితంలో తప్పారు. కింది చర్యల్లో ఏది/ఏవి అనుసరణీయం?",
  COA,0,
  "Only I follows: finding the reasons and arranging remedial classes deals directly with the problem. II is not practical or desirable — removing a core subject from the syllabus does not solve the learning problem.",
  "I మాత్రమే అనుసరణీయం: కారణాలు కనుక్కొని పరిహార తరగతులు ఏర్పాటు చేయడం నేరుగా సమస్యను పరిష్కరిస్తుంది. II ఆచరణీయం కాదు, వాంఛనీయం కాదు — ప్రధాన సబ్జెక్టును సిలబస్ నుంచి తీసేస్తే అభ్యాస సమస్య తీరదు.",
  [("I. The District Educational Officer should study the reasons and arrange remedial classes.","I. జిల్లా విద్యాశాఖాధికారి కారణాలు అధ్యయనం చేసి పరిహార తరగతులు ఏర్పాటు చేయాలి."),("II. Mathematics should be removed from the Class X syllabus.","II. పదో తరగతి సిలబస్ నుంచి గణితాన్ని తొలగించాలి.")]),
q("men-log-4","m","Statement: Many accidents on a highway stretch take place at night because the road there is not lit. Which of the following courses of action follow(s)?","వాక్యం: ఒక రహదారి భాగంలో వెలుతురు లేకపోవడం వల్ల రాత్రిపూట చాలా ప్రమాదాలు జరుగుతున్నాయి. కింది చర్యల్లో ఏది/ఏవి అనుసరణీయం?",
  COA,2,
  "Both follow. I removes the stated cause (darkness) directly. II is also a practical step that reduces night-time accidents on that stretch while lights are being installed. Both are reasonable and within the authorities' power.",
  "రెండూ అనుసరణీయం. I చెప్పిన కారణాన్ని (చీకటి) నేరుగా తొలగిస్తుంది. లైట్లు ఏర్పాటయ్యే లోపు ఆ భాగంలో రాత్రి ప్రమాదాలను తగ్గించే ఆచరణీయ చర్య II కూడా. రెండూ సహేతుకమైనవి, అధికారుల పరిధిలోనివి.",
  [("I. Street lights and reflective signboards should be installed on that stretch.","I. ఆ భాగంలో వీధి దీపాలు, ప్రతిఫలించే సూచిక బోర్డులు ఏర్పాటు చేయాలి."),("II. Highway police should increase night patrolling on that stretch and fine speeding vehicles.","II. హైవే పోలీసులు ఆ భాగంలో రాత్రి గస్తీ పెంచి, అతివేగ వాహనాలకు జరిమానా విధించాలి.")]),
q("men-abl-1","e","Find the next number in the series: 5, 11, 23, 47, 95, ?","శ్రేణిలో తర్వాతి సంఖ్య కనుక్కోండి: 5, 11, 23, 47, 95, ?",
  M("191","189","190","193"),0,
  "Each term = previous term × 2 + 1: 5×2+1 = 11, 11×2+1 = 23, 23×2+1 = 47, 47×2+1 = 95, 95×2+1 = 191.",
  "ప్రతి పదం = ముందు పదం × 2 + 1: 5×2+1 = 11, 11×2+1 = 23, 23×2+1 = 47, 47×2+1 = 95, 95×2+1 = 191."),
q("men-abl-1","m","Find the wrong number in the series: 2, 5, 10, 17, 26, 38, 50","శ్రేణిలో తప్పు సంఖ్య కనుక్కోండి: 2, 5, 10, 17, 26, 38, 50",
  M("38","26","17","50"),0,
  "The terms are n² + 1: 1+1 = 2, 4+1 = 5, 9+1 = 10, 16+1 = 17, 25+1 = 26, 36+1 = 37, 49+1 = 50. So 38 is wrong; it should be 37. (Differences 3, 5, 7, 9, 11, 13 also show it.)",
  "పదాలు n² + 1: 1+1 = 2, 4+1 = 5, 9+1 = 10, 16+1 = 17, 25+1 = 26, 36+1 = 37, 49+1 = 50. కాబట్టి 38 తప్పు; 37 ఉండాలి. (తేడాలు 3, 5, 7, 9, 11, 13 కూడా ఇదే చూపిస్తాయి.)"),
q("men-abl-1","m","Find the next number in the series: 3, 4, 8, 17, 33, ?","శ్రేణిలో తర్వాతి సంఖ్య కనుక్కోండి: 3, 4, 8, 17, 33, ?",
  M("58","56","50","66"),0,
  "The differences are perfect squares: +1 (1²), +4 (2²), +9 (3²), +16 (4²), so the next difference is +25 (5²): 33 + 25 = 58.",
  "తేడాలు పూర్ణ వర్గాలు: +1 (1²), +4 (2²), +9 (3²), +16 (4²); కాబట్టి తర్వాతి తేడా +25 (5²): 33 + 25 = 58."),
q("men-abl-2","h","Find the next letter in the series: B, E, I, N, T, ?","శ్రేణిలో తర్వాతి అక్షరం కనుక్కోండి: B, E, I, N, T, ?",
  M("A","Z","Y","B"),0,
  "Positions: B = 2, E = 5, I = 9, N = 14, T = 20. The gaps are +3, +4, +5, +6, so the next gap is +7: 20 + 7 = 27. After Z (26) we start again from A, so 27 = A.",
  "స్థానాలు: B = 2, E = 5, I = 9, N = 14, T = 20. అంతరాలు +3, +4, +5, +6; తర్వాతి అంతరం +7: 20 + 7 = 27. Z (26) తర్వాత మళ్లీ A నుంచి లెక్కిస్తాం; కాబట్టి 27 = A."),
q("men-abl-3","e","Find the odd one out:","భిన్నమైనదాన్ని కనుక్కోండి:",
  M("144","125","216","343"),0,
  "125 = 5³, 216 = 6³ and 343 = 7³ are perfect cubes. 144 = 12² is a perfect square but not a cube, so it is the odd one.",
  "125 = 5³, 216 = 6³, 343 = 7³ పూర్ణ ఘనాలు. 144 = 12² పూర్ణ వర్గం, ఘనం కాదు; కాబట్టి అదే భిన్నమైనది."),
q("men-abl-4","m","In a certain code, PAPER is written as SDSHU. How is PENCIL written in that code?","ఒక సంకేత భాషలో PAPERను SDSHUగా రాస్తారు. అదే సంకేతంలో PENCILను ఎలా రాస్తారు?",
  M("SHQFLO","SHQFOL","RGPEKN","SHPFLO"),0,
  "Each letter moves 3 places forward: P→S, A→D, P→S, E→H, R→U. So PENCIL: P→S, E→H, N→Q, C→F, I→L, L→O = SHQFLO.",
  "ప్రతి అక్షరం 3 స్థానాలు ముందుకు: P→S, A→D, P→S, E→H, R→U. కాబట్టి PENCIL: P→S, E→H, N→Q, C→F, I→L, L→O = SHQFLO."),
q("men-abl-4","m","In a code language, 'sky is blue' is written as '4 7 9', 'blue and green' as '9 2 5' and 'green is good' as '5 7 3'. What is the code for 'and'?","ఒక సంకేత భాషలో 'sky is blue'ను '4 7 9'గా, 'blue and green'ను '9 2 5'గా, 'green is good'ను '5 7 3'గా రాస్తారు. 'and'కు సంకేతం ఏది?",
  M("2","5","9","3"),0,
  "'blue' is common to sentences 1 and 2 → 9; 'is' is common to 1 and 3 → 7; 'green' is common to 2 and 3 → 5. In sentence 2 ('blue and green' = 9 2 5), the code left for 'and' is 2.",
  "1, 2 వాక్యాల్లో ఉమ్మడి 'blue' → 9; 1, 3లో ఉమ్మడి 'is' → 7; 2, 3లో ఉమ్మడి 'green' → 5. రెండో వాక్యం ('blue and green' = 9 2 5)లో 'and'కు మిగిలిన సంకేతం 2."),
q("men-abl-5","m","A is the sister of B. C is the mother of B. D is the father of C. How is A related to D?","A, Bకి సోదరి. C, Bకి తల్లి. D, Cకి తండ్రి. Dకి A ఏమవుతుంది?",
  [("Granddaughter","మనవరాలు"),("Daughter","కుమార్తె"),("Niece","మేనకోడలు"),("Grandmother","అమ్మమ్మ")],0,
  "A and B are children of C (A is B's sister, C is B's mother). D is C's father, so D is the maternal grandfather of A. A is female, so A is D's granddaughter.",
  "A, B ఇద్దరూ C పిల్లలు (A, Bకి సోదరి; C, Bకి తల్లి). D, Cకి తండ్రి; కాబట్టి D, Aకి తాత (అమ్మ తండ్రి). A స్త్రీ కాబట్టి Dకి A మనవరాలు."),
q("men-abl-5","m","If 'P + Q' means P is the son of Q, 'P × Q' means P is the wife of Q and 'P ÷ Q' means P is the brother of Q, what does 'A ÷ B + C × D' mean?","'P + Q' అంటే P, Qకి కుమారుడు; 'P × Q' అంటే P, Qకి భార్య; 'P ÷ Q' అంటే P, Qకి సోదరుడు అయితే, 'A ÷ B + C × D' అంటే ఏమిటి?",
  [("A is the son of D","A, Dకి కుమారుడు"),("A is the brother of D","A, Dకి సోదరుడు"),("A is the nephew of D","A, Dకి మేనల్లుడు"),("A is the father of D","A, Dకి తండ్రి")],0,
  "A ÷ B: A is B's brother. B + C: B is C's son. C × D: C is D's wife. So B is the son of C and D, and A — B's brother — is also a son of C and D. Hence A is the son of D.",
  "A ÷ B: A, Bకి సోదరుడు. B + C: B, Cకి కుమారుడు. C × D: C, Dకి భార్య. కాబట్టి B, C–Dల కుమారుడు; Bకి సోదరుడైన A కూడా C–Dల కుమారుడే. అంటే A, Dకి కుమారుడు."),
q("men-abl-5","h","One morning after sunrise, Suresh was standing facing a pole. The shadow of the pole fell exactly to his right. Which direction was he facing?","ఒక రోజు ఉదయం సూర్యోదయం తర్వాత సురేష్ ఒక స్తంభానికి ఎదురుగా నిలబడ్డాడు. స్తంభం నీడ సరిగ్గా అతని కుడివైపు పడింది. అతను ఏ దిశకు తిరిగి ఉన్నాడు?",
  [("South","దక్షిణం"),("North","ఉత్తరం"),("East","తూర్పు"),("West","పడమర")],0,
  "In the morning the Sun is in the east, so shadows fall towards the WEST. The shadow is on his right, so his right hand points west. A person whose right side is west is facing SOUTH.",
  "ఉదయం సూర్యుడు తూర్పున ఉంటాడు; నీడలు పడమర వైపు పడతాయి. నీడ అతని కుడివైపు ఉంది, అంటే అతని కుడి చేయి పడమర వైపు. కుడివైపు పడమర ఉన్న వ్యక్తి దక్షిణం వైపు తిరిగి ఉంటాడు."),
dict(q("men-abl-6","m","How many triangles are there in the figure given below (a square with both its diagonals drawn)?","కింది పటంలో (రెండు కర్ణాలు గీసిన చతురస్రం) మొత్తం ఎన్ని త్రిభుజాలు ఉన్నాయి?",
  M("8","4","6","10"),0,
  "The diagonals cut the square into 4 small triangles meeting at the centre. Each diagonal also cuts the square into 2 large triangles — 2 diagonals × 2 = 4 large triangles. Total = 4 + 4 = 8.",
  "కర్ణాలు చతురస్రాన్ని కేంద్రం వద్ద కలిసే 4 చిన్న త్రిభుజాలుగా చేస్తాయి. ప్రతి కర్ణం చతురస్రాన్ని 2 పెద్ద త్రిభుజాలుగా కూడా విభజిస్తుంది — 2 కర్ణాలు × 2 = 4 పెద్ద త్రిభుజాలు. మొత్తం = 4 + 4 = 8."),fig=SQX),
q("men-num-1","m","What is the largest four-digit number that is exactly divisible by 12, 15 and 18?","12, 15, 18లతో నిశ్శేషంగా భాగించబడే అతిపెద్ద నాలుగు అంకెల సంఖ్య ఏది?",
  M("9900","9720","9980","9960"),0,
  "LCM of 12, 15 and 18 = 180. 9999 ÷ 180 = 55 remainder 99. So the largest multiple is 9999 − 99 = 9900 (= 180 × 55). 9980 and 9960 are not multiples of 180; 9720 is a multiple but smaller.",
  "12, 15, 18ల క.సా.గు. = 180. 9999 ÷ 180 = 55, శేషం 99. కాబట్టి అతిపెద్ద గుణిజం 9999 − 99 = 9900 (= 180 × 55). 9980, 9960 180 గుణిజాలు కావు; 9720 గుణిజమే కానీ చిన్నది."),
q("men-num-1","h","How many numbers from 1 to 100 (both included) are divisible by neither 2 nor 3?","1 నుంచి 100 వరకు (రెండూ కలిపి) ఉన్న సంఖ్యల్లో 2తో గానీ 3తో గానీ భాగించబడనివి ఎన్ని?",
  M("33","34","50","17"),0,
  "Divisible by 2: 50; by 3: 33; by both (i.e. by 6): 16. Divisible by 2 or 3 = 50 + 33 − 16 = 67. Neither = 100 − 67 = 33.",
  "2తో భాగించబడేవి: 50; 3తో: 33; రెండింటితో (అంటే 6తో): 16. 2 లేదా 3తో భాగించబడేవి = 50 + 33 − 16 = 67. ఏదీ కానివి = 100 − 67 = 33."),
q("men-num-2","m","The average age of 30 students in a class is 14 years. When the teacher's age is included, the average rises by 1 year. What is the teacher's age?","ఒక తరగతిలో 30 మంది విద్యార్థుల సగటు వయస్సు 14 ఏళ్లు. ఉపాధ్యాయుని వయస్సు కలిపితే సగటు 1 ఏడాది పెరుగుతుంది. ఉపాధ్యాయుని వయస్సు ఎంత?",
  U("years","ఏళ్లు","45","44","15","46"),0,
  "Total of 30 students = 30 × 14 = 420. With the teacher, 31 persons have an average of 15, total = 31 × 15 = 465. Teacher's age = 465 − 420 = 45 years. Shortcut: 15 + 30 × 1 = 45.",
  "30 మంది విద్యార్థుల మొత్తం = 30 × 14 = 420. ఉపాధ్యాయునితో 31 మంది సగటు 15, మొత్తం = 31 × 15 = 465. ఉపాధ్యాయుని వయస్సు = 465 − 420 = 45 ఏళ్లు. సులువు: 15 + 30 × 1 = 45."),
q("men-num-3","m","₹7,800 is divided among A, B and C in the ratio 1/2 : 1/3 : 1/4. What is B's share?","₹7,800ను A, B, Cలకు 1/2 : 1/3 : 1/4 నిష్పత్తిలో పంచారు. B వాటా ఎంత?",
  M("₹2,400","₹2,600","₹3,600","₹1,800"),0,
  "Multiply each part by the LCM 12: 1/2 : 1/3 : 1/4 = 6 : 4 : 3 (sum 13). B's share = 4/13 × 7,800 = ₹2,400. (A = ₹3,600, C = ₹1,800 — the traps.)",
  "ప్రతి భాగాన్ని క.సా.గు. 12తో గుణిస్తే: 1/2 : 1/3 : 1/4 = 6 : 4 : 3 (మొత్తం 13). B వాటా = 4/13 × 7,800 = ₹2,400. (A = ₹3,600, C = ₹1,800 — ఇవే ఉచ్చులు.)"),
q("men-num-4","e","A's salary is 25% more than B's salary. By what percentage is B's salary less than A's?","A జీతం B జీతం కంటే 25% ఎక్కువ. A జీతం కంటే B జీతం ఎంత శాతం తక్కువ?",
  M("20%","25%","15%","30%"),0,
  "Let B = 100, then A = 125. B is less than A by 25 out of 125: 25/125 × 100 = 20%. Trap: it is not 25%, because the base changes.",
  "B = 100 అనుకుంటే A = 125. 125లో B 25 తక్కువ: 25/125 × 100 = 20%. ఉచ్చు: ఆధారం మారుతుంది కాబట్టి 25% కాదు."),
q("men-num-5","m","A sum of money doubles itself in 8 years at simple interest. In how many years will it become four times itself at the same rate?","ఒక మొత్తం సాధారణ వడ్డీపై 8 ఏళ్లలో రెట్టింపు అవుతుంది. అదే రేటుతో అది నాలుగు రెట్లు కావడానికి ఎన్ని ఏళ్లు పడుతుంది?",
  U("years","ఏళ్లు","24","16","32","20"),0,
  "Doubling means interest = 100% of the principal in 8 years, so the rate = 100/8 = 12.5% a year. To become 4 times, interest must be 300%: 300/12.5 = 24 years. Trap: 16 years would be right only for compound interest (doubling twice).",
  "రెట్టింపు అంటే 8 ఏళ్లలో వడ్డీ = అసలులో 100%; కాబట్టి రేటు = 100/8 = ఏటా 12.5%. 4 రెట్లు కావాలంటే వడ్డీ 300% కావాలి: 300/12.5 = 24 ఏళ్లు. ఉచ్చు: 16 ఏళ్లు చక్రవడ్డీకి (రెండుసార్లు రెట్టింపు) మాత్రమే సరిపోతుంది."),
q("men-num-6","h","A and B together can do a piece of work in 12 days, B and C together in 15 days, and C and A together in 20 days. In how many days can A, B and C together do it?","A, B కలిసి ఒక పనిని 12 రోజుల్లో, B, C కలిసి 15 రోజుల్లో, C, A కలిసి 20 రోజుల్లో చేయగలరు. A, B, C ముగ్గురూ కలిసి ఆ పనిని ఎన్ని రోజుల్లో చేయగలరు?",
  U("days","రోజులు","10","5","15","8"),0,
  "Add the three one-day works: 1/12 + 1/15 + 1/20 = (5 + 4 + 3)/60 = 12/60 = 1/5. This is TWICE the work of (A + B + C) in a day, so A + B + C do 1/10 a day → 10 days. Trap: 5 days forgets to halve.",
  "మూడు జతల ఒక రోజు పనిని కలపండి: 1/12 + 1/15 + 1/20 = (5 + 4 + 3)/60 = 12/60 = 1/5. ఇది (A + B + C) ఒక రోజు పనికి రెట్టింపు; కాబట్టి A + B + C రోజుకు 1/10 → 10 రోజులు. ఉచ్చు: సగం చేయడం మర్చిపోతే 5 రోజులు వస్తుంది."),
q("men-num-6","e","Pipe A can fill a tank in 10 hours and pipe B can empty the full tank in 15 hours. If both are opened together when the tank is empty, in how many hours will the tank be full?","గొట్టం A ఒక ట్యాంకును 10 గంటల్లో నింపుతుంది; గొట్టం B నిండిన ట్యాంకును 15 గంటల్లో ఖాళీ చేస్తుంది. ఖాళీ ట్యాంకుకు రెండూ ఒకేసారి తెరిస్తే ఎన్ని గంటల్లో ట్యాంకు నిండుతుంది?",
  U("hours","గంటలు","30","6","25","12"),0,
  "Net filling per hour = 1/10 − 1/15 = (3 − 2)/30 = 1/30. So the tank fills in 30 hours. Trap: 6 hours is what you get if you ADD the two rates.",
  "గంటకు నికరంగా నిండేది = 1/10 − 1/15 = (3 − 2)/30 = 1/30. కాబట్టి 30 గంటల్లో నిండుతుంది. ఉచ్చు: రెండు రేట్లను కలిపితే 6 గంటలు వస్తుంది."),
q("men-num-7","m","The speed of a boat in still water is 15 km/h and the speed of the stream is 3 km/h. How long will the boat take to go 36 km downstream and come back?","నిశ్చల నీటిలో పడవ వేగం గంటకు 15 కి.మీ., ప్రవాహ వేగం గంటకు 3 కి.మీ. ప్రవాహ దిశలో 36 కి.మీ. వెళ్లి తిరిగి రావడానికి పడవకు ఎంత సమయం పడుతుంది?",
  U("hours","గంటలు","5","4.8","4","6"),0,
  "Downstream speed = 15 + 3 = 18 km/h → 36/18 = 2 hours. Upstream speed = 15 − 3 = 12 km/h → 36/12 = 3 hours. Total = 2 + 3 = 5 hours. Trap: 4.8 hours uses 15 km/h both ways (72/15).",
  "ప్రవాహ దిశ వేగం = 15 + 3 = 18 కి.మీ./గం. → 36/18 = 2 గంటలు. ఎదురు ప్రవాహ వేగం = 15 − 3 = 12 కి.మీ./గం. → 36/12 = 3 గంటలు. మొత్తం = 2 + 3 = 5 గంటలు. ఉచ్చు: రెండు వైపులా 15 కి.మీ./గం. తీసుకుంటే 4.8 గంటలు (72/15)."),
dict(q("men-num-8","m","The pie chart shows the monthly spending of a family whose total monthly spending is ₹40,000. How much more does the family spend on rent than on transport?","పై చార్ట్ ఒక కుటుంబ నెలవారీ ఖర్చును చూపిస్తుంది; మొత్తం నెల ఖర్చు ₹40,000. రవాణా కంటే అద్దెకు ఆ కుటుంబం ఎంత ఎక్కువ ఖర్చు చేస్తుంది?",
  M("₹6,000","₹4,000","₹10,000","₹15,000"),0,
  "Rent = 25%, transport = 10%; difference = 15% of ₹40,000 = 0.15 × 40,000 = ₹6,000. (₹10,000 is the rent alone; ₹4,000 is the transport alone.)",
  "అద్దె = 25%, రవాణా = 10%; తేడా = ₹40,000లో 15% = 0.15 × 40,000 = ₹6,000. (₹10,000 అద్దె మాత్రమే; ₹4,000 రవాణా మాత్రమే.)"),fig=PIE),
dict(q("men-num-8","m","From the same pie chart, what is the central angle of the sector for education?","అదే పై చార్ట్ ప్రకారం విద్య భాగం కేంద్ర కోణం ఎంత?",
  M("54°","45°","36°","60°"),0,
  "A full circle is 360°. Education = 15%, so its angle = 15/100 × 360° = 54°. (36° would be transport, 10%.)",
  "వృత్తం మొత్తం 360°. విద్య = 15%; కాబట్టి కోణం = 15/100 × 360° = 54°. (36° రవాణా, 10%.)"),fig=PIE),
dict(q("men-num-8","h","The line graph shows the production of two-wheelers by a company (in thousand units). In which year was the percentage increase in production over the previous year the highest?","రేఖా చిత్రం ఒక కంపెనీ ద్విచక్ర వాహనాల ఉత్పత్తిని (వేల యూనిట్లలో) చూపిస్తుంది. ముందు ఏడాదితో పోలిస్తే ఉత్పత్తిలో శాత పెరుగుదల ఏ సంవత్సరంలో అత్యధికం?",
  [("2025","2025"),("2023","2023"),("2024","2024"),("Equal in 2023 and 2025","2023, 2025లో సమానం")],0,
  "2023: (150 − 120)/120 = 25%. 2024: production fell (150 → 135, −10%). 2025: (180 − 135)/135 ≈ 33.3%. Highest = 2025. Trap: the rise in 2023 (30) is smaller in number than 2025 (45), and also smaller in percentage.",
  "2023: (150 − 120)/120 = 25%. 2024: ఉత్పత్తి తగ్గింది (150 → 135, −10%). 2025: (180 − 135)/135 ≈ 33.3%. అత్యధికం = 2025. ఉచ్చు: 2023 పెరుగుదల (30) సంఖ్యలోనూ 2025 (45) కంటే తక్కువ, శాతంలోనూ తక్కువ."),fig=LINE),
]
