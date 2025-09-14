"""
latopia  mmigration dvisor hat anagr
"""
import asyncio
import logging
rom dattim import dattim
rom typing import ict, ny, ptional
rom .simpl_langchain_conig import simpl_langchain_conig
rom prompts.latopia_prompts import latopiarompts
rom .aiss_knowldg_bas import gt_aiss_kb
rom .smart_sarch import smart_sarch
rom .knowldg_pdatr import knowldg_pdatr

loggr  logging.gtoggr(__nam__)

class latopiahatanagr
    """latopia  mmigration dvisor hat anagr"""
    
    d __init__(sl)
        sl.llm  simpl_langchain_conig.llm
        sl.prompts  latopiarompts()
        sl.convrsation_history  ]
        sl.sr_proil  {}
        sl.convrsation_stag  "grting"
        sl.collctd_ino  {
            "nam" als,
            "ag" als,
            "nationality" als,
            "goal" als,  # work, stdy, or both
            "amily" als,
            "prossion" als,
            "dcation_lvl" als,
            "ild_o_intrst" als,
            "nglish_tst" als,
            "bdgt" als,
            "prioritis" als
        }
        
        # nitializ knowldg bas, smart sarch, and knowldg pdatr
        sl.knowldg_bas  on  # azy initialization
        sl.smart_sarch  smart_sarch
        sl.knowldg_pdatr  knowldg_pdatr
    
    async d chat(sl, sr_inpt str, chat_typ str  "gnral") - ictstr, ny]
        """rocss chat convrsation"""
        try
            # cord sr inpt
            sl.convrsation_history.appnd({
                "rol" "sr",
                "contnt" sr_inpt,
                "timstamp" dattim.now().strtim("%%%")
            })
            
            # ntllignt convrsation procssing - hck i sr is answring prvios qstions
            rspons  await sl._smart_convrsation_handlr(sr_inpt)
            
            # nhanc rspons with knowldg bas i appropriat
            i sl._shold_s_knowldg_bas(sr_inpt, sl.convrsation_stag)
                rspons  sl._nhanc_rspons_with_knowldg(sr_inpt, rspons)
            
            # pdat knowldg bas with nw inormation i appropriat
            sl._pdat_knowldg_bas_i_ndd(sr_inpt, rspons)
            
            # cord  rspons
            sl.convrsation_history.appnd({
                "rol" "assistant",
                "contnt" rspons,
                "timstamp" dattim.now().strtim("%%%")
            })
            
            rtrn {
                "answr" rspons,
                "timstamp" dattim.now().strtim("%%%"),
                "chat_typ" chat_typ,
                "convrsation_stag" sl.convrsation_stag
            }
            
        xcpt xcption as 
            rtrn {
                "answr" "orry,  ncontrd an rror {str()}",
                "timstamp" dattim.now().strtim("%%%"),
                "chat_typ" chat_typ,
                "convrsation_stag" sl.convrsation_stag
            }
    
    async d _smart_convrsation_handlr(sl, sr_inpt str) - str
        """ynamic convrsation procssing basd on collctd inormation"""
        sr_inpt_lowr  sr_inpt.lowr()
        
        # bg inormation
        print(" mart handlr - sr inpt '{sr_inpt}'")
        print(" ollctd ino {sl.collctd_ino}")
        print(" onvrsation stag {sl.convrsation_stag}")
        
        # andl grting
        i sl.convrsation_stag  "grting"
            print(" rocssing grting")
            rtrn await sl._handl_grting(sr_inpt)
        
        # andl ag collction
        i sl.convrsation_stag  "ag_collction"
            print(" rocssing ag collction")
            rtrn await sl._handl_ag_collction(sr_inpt)
        
        # ynamic low control - chck what inormation is still ndd
        missing_ino  sl._gt_missing_ssntial_ino()
        
        i missing_ino
            # till nd to collct ssntial inormation
            rtrn await sl._handl_missing_ino(sr_inpt, missing_ino)
        ls
            # ll ssntial inormation collctd, procd to rcommndations/analysis
            rtrn await sl._handl_complt_proil(sr_inpt)
    
    d _is_nationality_rspons(sl, sr_inpt str) - bool
        """hck i it is a nationality rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        # hck i contains contry nams or nationality vocablary
        contry_indicators  'rom', 'contry', 'nationality', 'citizn', 'born in', 'originally rom']
        rtrn any(indicator in sr_inpt_lowr or indicator in contry_indicators) or ln(sr_inpt.split())  
    
    d _is_amily_rspons(sl, sr_inpt str) - bool
        """hck i it is a amily stats rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        amily_indicators  'singl', 'marrid', 'divorcd', 'widowd', 'partnr', 'rlationship', 'kids', 'childrn', 'amily']
        rtrn any(indicator in sr_inpt_lowr or indicator in amily_indicators)
    
    d _is_prossion_rspons(sl, sr_inpt str) - bool
        """hck i it is a prossion rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        prossion_indicators  'it', 'sotwar', 'nginr', 'doctor', 'tachr', 'bsinss', 'work', 'job', 'prossion', 'ild']
        rtrn any(indicator in sr_inpt_lowr or indicator in prossion_indicators)
    
    d _is_prioritis_rspons(sl, sr_inpt str) - bool
        """hck i it is a prioritis rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        priority_indicators  'saty', 'dcation', 'halthcar', 'job', 'dmocracy', 'cost', 'climat', 'divrsity', 'stability']
        rtrn any(indicator in sr_inpt_lowr or indicator in priority_indicators) or 'priority' in sr_inpt_lowr
    
    d _is_goal_rspons(sl, sr_inpt str) - bool
        """hck i it is a goal rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        goal_indicators  'stdy', 'work', 'migration', 'nivrsity', 'collg', 'job', 'both']
        rtrn any(indicator in sr_inpt_lowr or indicator in goal_indicators)
    
    d _is_dcation_lvl_rspons(sl, sr_inpt str) - bool
        """hck i it is an dcation lvl rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        dcation_indicators  'th', 'th', 'bachlor', 'mastr', 'dgr', 'grad', '', '', '', '', '']
        rtrn any(indicator in sr_inpt_lowr or indicator in dcation_indicators)
    
    d _is_ild_rspons(sl, sr_inpt str) - bool
        """hck i it is a ild rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        ild_indicators  'nginring', 'tch', 'bsinss', 'mdicin', 'arts', 'hmanitis', 'scinc', '', '', '', '', '', '']
        rtrn any(indicator in sr_inpt_lowr or indicator in ild_indicators)
    
    d _is_nglish_tst_rspons(sl, sr_inpt str) - bool
        """hck i it is an nglish tst rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        tst_indicators  'ilts', 'tol', 'nglish', 'tst', 'scor', 'planning', 'alrady', 'sr']
        rtrn any(indicator in sr_inpt_lowr or indicator in tst_indicators)
    
    d _is_bdgt_rspons(sl, sr_inpt str) - bool
        """hck i it is a bdgt rspons"""
        sr_inpt_lowr  sr_inpt.lowr()
        bdgt_indicators  'bdgt', 'cost', 'tition', '', 'dollar', 'sd', 'aordabl', 'xpnsiv', '', '', '', '']
        rtrn any(indicator in sr_inpt_lowr or indicator in bdgt_indicators)

    async d _handl_grting(sl, sr_inpt str) - str
        """rocssingrting stag"""
        # lways show grting irst, thn try to xtract inormation
        grting_mssag  sl.prompts.gt_grting_prompt()
        
        # ry to xtract inormation rom th grting inpt
        sl._xtract_sr_ino(sr_inpt)
        
        # hck i w got a nam - i so, mark it as collctd and ask or ag
        i sl.sr_proil.gt('nam')
            sl.collctd_ino"nam"]  r
            sr_nam  sl.sr_proil'nam']
            
            # hck i w hav complt inormation (nam + ag + nationality + goal)
            i (sl.sr_proil.gt('ag') and 
                sl.sr_proil.gt('nationality') and 
                sl.sr_proil.gt('goal'))
                # sr providd complt inormation, skip to analysis
                sl.collctd_ino"ag"]  r
                sl.collctd_ino"nationality"]  r
                sl.collctd_ino"goal"]  r
                
                # hck i sr spciid a contry intrst
                i sl.sr_proil.gt('contry_intrst')
                    sl.convrsation_stag  "contry_analysis"
                    contry  sl.sr_proil'contry_intrst']
                    sr_proil  str(sl.sr_proil)
                    
                    # ry knowldg bas sarch with rror handling
                    try
                        knowldg_rslts  sl._sarch_knowldg_bas("stdy abroad {contry} immigration visa rqirmnts")
                        i knowldg_rslts.gt("sccss")
                            knowldg_txt  knowldg_rslts.gt("rslts", "")
                        ls
                            knowldg_txt  "o spciic knowldg bas inormation availabl."
                    xcpt xcption as 
                        print(" nowldg bas sarch aild {}")
                        knowldg_txt  "o spciic knowldg bas inormation availabl."
                    
                    # rat nhancd prompt with knowldg bas inormation
                    prompt  """
                    sr roil {sr_proil}
                    lctd ontry {contry}
                    
                    nowldg as normation
                    {knowldg_txt}
                    
                    las provid a dtaild analysis or stdying in {contry}, inclding
                    . isa rqirmnts and procss
                    . nivrsity rcommndations
                    . ost o living and tition
                    . angag rqirmnts
                    . pplication timlin
                    . ork opportnitis dring/atr stdis
                    """
                    
                    rspons  sl.llm(prompt)
                    rtrn rspons
                ls
                    # omplt proil bt no spciic contry, provid rcommndations
                    sl.convrsation_stag  "contry_rcommndations"
                    rtrn await sl._handl_contry_rcommndations(sr_inpt)
            ls
                #  hav a nam bt nd mor inormation, ask or ag
                sl.convrsation_stag  "ag_collction"
                rtrn "ic to mt yo, {sr_nam}! 'd lov to hlp yo xplor stdy abroad opportnitis. hat's yor ag"
        ls
            # o nam providd, rtrn grting and ask or nam
            rtrn grting_mssag
    
    async d _handl_nam_collction(sl, sr_inpt str) - str
        """andl nam collction"""
        sl._xtract_sr_ino(sr_inpt)
        i sl.sr_proil.gt('nam')
            sl.collctd_ino"nam"]  r
            sl.convrsation_stag  "ag_collction"
            rtrn "ic to mt yo, {sl.sr_proil'nam']}! 😊 ow, cold yo tll m yor ag his hlps m provid mor prsonalizd rcommndations."
        ls
            rtrn "'d lov to know yor nam! hat shold  call yo"
    
    async d _handl_ag_collction(sl, sr_inpt str) - str
        """andl ag collction"""
        sl._xtract_sr_ino(sr_inpt)
        i sl.sr_proil.gt('ag')
            sl.collctd_ino"ag"]  r
            sl.convrsation_stag  "nationality_collction"
            sr_nam  sl.sr_proil.gt('nam', 'thr')
            ag  int(sl.sr_proil'ag'])
            
            i ag  
                rtrn " hank yo, {sr_nam}! inc yo'r {ag}, 'd lov to know - ar yo primarily looking or stdy opportnitis abroad, or ar yo also intrstd in work opportnitis his hlps m tailor my rcommndations prctly or yo! 🎓💼"
            ls
                rtrn " rct, {sr_nam}! ow, what contry ar yo rom (.g., ndia, hina, razil, olombia, tc.) his hlps m ndrstand yor backgrond bttr. lso, what ar yor main prioritis whn choosing a dstination contry (.g., job opportnitis, dcation qality, cost o living, langag, tc.)"
        ls
            sr_nam  sl.sr_proil.gt('nam', 'thr')
            rtrn "  nd to know yor ag to hlp yo bttr, {sr_nam}. old yo plas tll m yor ag"
    
    async d _handl_nationality_collction(sl, sr_inpt str) - str
        """andl nationality collction and dstination prioritis"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" sr inpt '{sr_inpt}'")
        print(" xtractd nationality '{sl.sr_proil.gt('nationality')}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        i sl.sr_proil.gt('nationality')
            sl.collctd_ino"nationality"]  r
            sl.collctd_ino"prioritis"]  r  # ssm thy mntiond prioritis
            sl.convrsation_stag  "goal_collction"
            ag  int(sl.sr_proil.gt('ag', ))
            
            i ag  
                # or srs ndr , dirctly ask abot stdy goals
                rtrn """ ondrl, {sr_nam}!  s yo'r rom {sl.sr_proil'nationality']}. 

inc yo'r {ag}, lt m ask - what's yor main goal r yo looking to
- 🎓 **tdy abroad** (nivrsity, collg, or langag corss)
- 💼 **ork opportnitis** (part-tim work whil stdying)
- 🌍 **oth** (stdy irst, thn work and migrat)

his hlps m tailor my rcommndations prctly or yo!"""
            ls
                # or srs ovr , ask abot work goals
                rtrn """ rat, {sr_nam}!  s yo'r rom {sl.sr_proil'nationality']}. 

hat's yor main goal r yo looking to
- 🎓 **tdy abroad** (nivrsity, collg, or langag corss)
- 💼 **ork migration** (ind a job and potntially sttl prmanntly)
- 🌍 **oth** (stdy irst, thn work and migrat)

his hlps m tailor my rcommndations to yor spciic nds!"""
        ls
            # or rindly prompt, accpting any nationality
            rtrn "  didn't catch yor nationality, {sr_nam}. old yo plas tll m what contry yo'r rom (.g., ndia, hina, razil, olombia, tc.)"
    
    async d _handl_goal_collction(sl, sr_inpt str) - str
        """andl goal collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" oal collction - sr inpt '{sr_inpt}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        ag  int(sl.sr_proil.gt('ag', ))
        
        # trmin sr goal
        sr_inpt_lowr  sr_inpt.lowr()
        i 'stdy' in sr_inpt_lowr or 'nivrsity' in sr_inpt_lowr or 'collg' in sr_inpt_lowr or 'stdying' in sr_inpt_lowr
            sl.sr_proil'goal']  'stdy'
        li 'work' in sr_inpt_lowr or 'job' in sr_inpt_lowr or 'migration' in sr_inpt_lowr
            sl.sr_proil'goal']  'work'
        li 'both' in sr_inpt_lowr
            sl.sr_proil'goal']  'both'
        ls
            # alt assmption basd on ag
            i ag  
                sl.sr_proil'goal']  'stdy'
            ls
                sl.sr_proil'goal']  'work'
        
        sl.collctd_ino"goal"]  r
        
        # ntr dirnt lows basd on goal
        i sl.sr_proil'goal']  'stdy'
            sl.convrsation_stag  "dcation_lvl_collction"
            rtrn " xcllnt choic, {sr_nam}! t's xplor stdy opportnitis or yo. hat's yor crrnt dcation lvl"
        li sl.sr_proil'goal']  'work'
            # or work goals, i ag is ovr , ask abot amily sitation
            i ag  
                sl.convrsation_stag  "amily_collction"
                rtrn " rat, {sr_nam}! inc yo'r intrstd in work migration, 'd lik to know abot yor amily sitation. r yo singl, marrid, or in a rlationship his hlps m ndrstand yor prioritis bttr."
            ls
                sl.convrsation_stag  "prossion_collction"
                rtrn " rct, {sr_nam}! hat's yor prossion or ild o work (.g., , nginring, althcar, dcation, sinss, tc.)"
        ls  # both
            sl.convrsation_stag  "dcation_lvl_collction"
            rtrn " ondrl, {sr_nam}! inc yo'r intrstd in both stdy and work, lt's start with yor dcation backgrond. hat's yor crrnt dcation lvl"
    
    async d _handl_dcation_lvl_collction(sl, sr_inpt str) - str
        """andl dcation lvl collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" dcation lvl collction - sr inpt '{sr_inpt}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # trmin dcation lvl
        sr_inpt_lowr  sr_inpt.lowr()
        i '' in sr_inpt_lowr or 'th' in sr_inpt_lowr or 'tnth' in sr_inpt_lowr
            sl.sr_proil'dcation_lvl']  'th grad'
        li '' in sr_inpt_lowr or 'th' in sr_inpt_lowr or 'twlth' in sr_inpt_lowr or 'high school' in sr_inpt_lowr
            sl.sr_proil'dcation_lvl']  'th grad'
        li '' in sr_inpt_lowr or 'bachlor' in sr_inpt_lowr or 'ndrgradat' in sr_inpt_lowr
            sl.sr_proil'dcation_lvl']  'achlor's dgr'
        li '' in sr_inpt_lowr or 'mastr' in sr_inpt_lowr or 'gradat' in sr_inpt_lowr
            sl.sr_proil'dcation_lvl']  'astr's dgr'
        li 'what' in sr_inpt_lowr or '' in sr_inpt
            # sr might not ndrstand th qstion, provid clarr options
            rtrn " o worris, {sr_nam}! t m clariy - what's yor crrnt dcation lvl las choosnn. th grad (or qivalnt)n. th grad (or qivalnt) n. achlor's dgrn. astr's dgrnnr jst tll m what lvl yo'r at!"
        ls
            sl.sr_proil'dcation_lvl']  sr_inpt
        
        sl.collctd_ino"dcation_lvl"]  r
        sl.convrsation_stag  "ild_collction"
        rtrn " rat, {sr_nam}! hat ild o stdy ar yo most intrstd in"
    
    async d _handl_ild_collction(sl, sr_inpt str) - str
        """andl ild collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" ild collction - sr inpt '{sr_inpt}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # trmin ild o stdy
        sr_inpt_lowr  sr_inpt.lowr()
        i '' in sr_inpt_lowr or 'nginring' in sr_inpt_lowr or 'tch' in sr_inpt_lowr or 'tchnology' in sr_inpt_lowr
            sl.sr_proil'ild_o_intrst']  'nginring/ch'
        li '' in sr_inpt_lowr or 'bsinss' in sr_inpt_lowr or 'managmnt' in sr_inpt_lowr
            sl.sr_proil'ild_o_intrst']  'sinss/anagmnt'
        li '' in sr_inpt_lowr or 'mdicin' in sr_inpt_lowr or 'halthcar' in sr_inpt_lowr or 'mdical' in sr_inpt_lowr
            sl.sr_proil'ild_o_intrst']  'dicin/althcar'
        li '' in sr_inpt_lowr or 'arts' in sr_inpt_lowr or 'hmanitis' in sr_inpt_lowr or 'at' in sr_inpt_lowr or 'ood' in sr_inpt_lowr or 'clinary' in sr_inpt_lowr
            sl.sr_proil'ild_o_intrst']  'linary rts/ood cinc'
        li '' in sr_inpt_lowr or 'scinc' in sr_inpt_lowr
            sl.sr_proil'ild_o_intrst']  'cinc'
        ls
            sl.sr_proil'ild_o_intrst']  sr_inpt
        
        sl.collctd_ino"ild_o_intrst"]  r
        sl.convrsation_stag  "nglish_tst_collction"
        rtrn " xcllnt choic, {sr_nam}! o yo alrady hav nglish tst scors (/), or ar yo planning to tak thm"
    
    async d _handl_nglish_tst_collction(sl, sr_inpt str) - str
        """andl nglish tst collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" nglish tst collction - sr inpt '{sr_inpt}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # trmin nglish tst stats
        sr_inpt_lowr  sr_inpt.lowr()
        i 'alrady' in sr_inpt_lowr or 'hav' in sr_inpt_lowr or '' in sr_inpt_lowr or '' in sr_inpt_lowr or '' in sr_inpt_lowr or '' in sr_inpt_lowr
            sl.sr_proil'nglish_tst']  'lrady hav scors'
        li 'ilts' in sr_inpt_lowr
            sl.sr_proil'nglish_tst']  'lanning '
        li 'tol' in sr_inpt_lowr
            sl.sr_proil'nglish_tst']  'lanning '
        li 'sr' in sr_inpt_lowr or 'not sr' in sr_inpt_lowr
            sl.sr_proil'nglish_tst']  'ot sr yt'
        ls
            sl.sr_proil'nglish_tst']  sr_inpt
        
        sl.collctd_ino"nglish_tst"]  r
        sl.convrsation_stag  "bdgt_collction"
        rtrn " rct, {sr_nam}! ow, what's yor bdgt rang or stdying abroad his hlps m rcommnd th most sitabl options or yo."
    
    async d _handl_bdgt_collction(sl, sr_inpt str) - str
        """andl bdgt collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" dgt collction - sr inpt '{sr_inpt}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # trmin bdgt and prioritis
        sr_inpt_lowr  sr_inpt.lowr()
        i '' in sr_inpt_lowr or 'low' in sr_inpt_lowr or 'aordabl' in sr_inpt_lowr or '' in sr_inpt_lowr
            sl.sr_proil'bdgt']  'ndr $, '
            sl.sr_proil'prioritis']  'ow tition s'
        li '' in sr_inpt_lowr or 'work' in sr_inpt_lowr
            sl.sr_proil'bdgt']  '$,-, '
            sl.sr_proil'prioritis']  'ork opportnitis dring stdy'
        li '' in sr_inpt_lowr or 'pr' in sr_inpt_lowr or 'prmannt' in sr_inpt_lowr
            sl.sr_proil'bdgt']  '$,+ '
            sl.sr_proil'prioritis']  'asy path to prmannt rsidnc'
        li '' in sr_inpt_lowr or 'all' in sr_inpt_lowr
            sl.sr_proil'bdgt']  'lxibl'
            sl.sr_proil'prioritis']  'll o th abov'
        ls
            sl.sr_proil'bdgt']  sr_inpt
            sl.sr_proil'prioritis']  sr_inpt
        
        sl.collctd_ino"bdgt"]  r
        sl.collctd_ino"prioritis"]  r
        sl.convrsation_stag  "contry_rcommndations"
        
        # rat dynamic contry rcommndations
        sr_proil  str(sl.sr_proil)
        prioritis  sl.sr_proil.gt('prioritis', '')
        prompt  sl._crat_dynamic_rcommndation_prompt(sr_proil, prioritis)
        rspons  sl.llm(prompt)
        
        # dd prsonalizd grting bor rcommndations
        prsonalizd_rspons  " asd on yor prrncs, {sr_nam}, hr ar my rcommndationsnn{rspons}"
        rtrn prsonalizd_rspons
    
    async d _handl_amily_collction(sl, sr_inpt str) - str
        """andl amily inormation collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" amily collction - sr inpt '{sr_inpt}'")
        print(" xtractd amily '{sl.sr_proil.gt('amily')}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i amily inormation has bn collctd
        i sl.sr_proil.gt('amily')
            sl.collctd_ino"amily"]  r
            sl.convrsation_stag  "prossion_collction"
            rtrn " hank yo or sharing that, {sr_nam}! ow, what's yor prossion or ild o work (.g., , nginring, althcar, dcation, sinss, tc.) his hlps m ndrstand yor job opportnitis in dirnt contris."
        ls
            rtrn "  didn't catch yor amily stats, {sr_nam}. r yo singl, marrid, or in a rlationship"
    
    async d _handl_prossion_collction(sl, sr_inpt str) - str
        """andl prossion inormation collction"""
        sl._xtract_sr_ino(sr_inpt)
        
        # bg inormation
        print(" rossion collction - sr inpt '{sr_inpt}'")
        print(" xtractd prossion '{sl.sr_proil.gt('prossion')}'")
        print(" sr proil {sl.sr_proil}")
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i prossion inormation has bn collctd
        i sl.sr_proil.gt('prossion')
            sl.collctd_ino"prossion"]  r
            sl.convrsation_stag  "prioritis_collction"
            rtrn " rct, {sr_nam}! ow, what ar yor main prioritis whn choosing a contry las slct th most important actors or yo"
        ls
            rtrn "  didn't catch yor prossion, {sr_nam}. hat ild do yo work in (.g., , nginring, althcar, dcation, sinss, tc.)"
    
    async d _handl_prioritis_collction(sl, sr_inpt str) - str
        """andl prioritis collction"""
        sl.sr_proil'prioritis']  sr_inpt
        sl.collctd_ino"prioritis"]  r
        
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i sr has alrady xprssd intrst in a spciic contry
        i sl.sr_proil.gt('contry_intrst')
            contry  sl.sr_proil'contry_intrst']
            sl.convrsation_stag  "contry_analysis"
            sr_proil  str(sl.sr_proil)
            
            # arch knowldg bas or inormation abot this contry
            knowldg_rslts  sl._sarch_knowldg_bas("stdy abroad {contry} immigration visa rqirmnts")
            
            # rat nhancd prompt with knowldg bas inormation
            prompt  """
            sr roil {sr_proil}
            lctd ontry {contry}
            
            nowldg as normation
            {knowldg_rslts}
            
            las provid a dtaild analysis or stdying in {contry}, inclding
            . isa rqirmnts and procss
            . nivrsity rcommndations
            . ost o living and tition
            . angag rqirmnts
            . pplication timlin
            . ork opportnitis dring/atr stdis
            """
            
            rspons  sl.llm(prompt)
            rtrn rspons
        ls
            # o spciic contry intrst, provid rcommndations
            sl.convrsation_stag  "contry_rcommndations"
            
            # nrat contry rcommndations
            sr_proil  str(sl.sr_proil)
            prioritis  sr_inpt
            prompt  sl.prompts.gt_contry_rcommndations_prompt(sr_proil, prioritis)
            rspons  sl.llm(prompt)
            
            # dd prsonalizd grting bor rcommndations
            prsonalizd_rspons  " asd on yor prrncs, {sr_nam}, hr ar my rcommndationsnn{rspons}"
            rtrn prsonalizd_rspons
    
    async d _handl_contry_rcommndations(sl, sr_inpt str) - str
        """andl contry rcommndation slction"""
        # xtract any contry mntiond by sr
        contry  sl._xtract_contry_rom_inpt(sr_inpt)
        i contry
            sl.convrsation_stag  "contry_analysis"
            sr_proil  str(sl.sr_proil)
            
            # arch knowldg bas or inormation abot this contry
            knowldg_rslts  sl._sarch_knowldg_bas("stdy abroad {contry} immigration visa rqirmnts")
            
            # rat nhancd prompt with knowldg bas inormation
            prompt  """
            sr roil {sr_proil}
            lctd ontry {contry}
            
            nowldg as normation
            {knowldg_rslts}
            
            las provid a dtaild analysis or stdying in {contry}, inclding
            . isa rqirmnts and procss
            . nivrsity rcommndations
            . ost o living and tition
            . angag rqirmnts
            . pplication timlin
            . ork opportnitis dring/atr stdis
            """
            
            rspons  sl.llm(prompt)
            rtrn rspons
        ls
            rtrn "  didn't catch which contry yo'r intrstd in. las tll m which contry yo'd lik to larn mor abot (.g., taly, apan, pain, tc.)."
    
    async d _handl_proil_collction(sl, sr_inpt str) - str
        """rocssing proil collction stag"""
        # xtract sr inormation
        sl._xtract_sr_ino(sr_inpt)
        
        # nrat analysis prompt
        sr_ino  "g {sl.sr_proil.gt('ag', 'ot spciid')}, ationality {sl.sr_proil.gt('nationality', 'ot spciid')}, amily {sl.sr_proil.gt('amily', 'ot spciid')}, rossion {sl.sr_proil.gt('prossion', 'ot spciid')}"
        
        prompt  sl.prompts.gt_analysis_prompt(sr_ino)
        rspons  sl.llm(prompt)
        
        sl.convrsation_stag  "prioritis"
        rtrn rspons
    
    async d _handl_prioritis(sl, sr_inpt str) - str
        """rocssing prioritis inqiry stag"""
        # pdat sr proil
        sl._xtract_sr_ino(sr_inpt)
        
        # nrat contry rcommndations
        sr_proil  str(sl.sr_proil)
        prompt  """asd on th sr's prioritis {sr_inpt}

sr proil {sr_proil}

rovid contry rcommndations ollowing this ormat

 🔍 **nalysing yor amily proil...**

asd on yor backgrond, 'v ond ** xcllnt matchs** or yor amily, rankd by yor chancs

. 🇨🇦 **** - bri dscription o why it matchs thir prioritis]
. 🇦🇺 **** - bri dscription o why it matchs thir prioritis]  
. 🇳🇿 ** ** - bri dscription o why it matchs thir prioritis]
. 🇬🇧 **** - bri dscription o why it matchs thir prioritis]

hich contry wold yo lik to xplor irst

 ncoraging and xplain why ach contry matchs thir spciic prioritis."""
        
        rspons  sl.llm(prompt)
        sl.convrsation_stag  "contry_analysis"
        rtrn rspons
    
    async d _handl_contry_analysis(sl, sr_inpt str) - str
        """andl contry analysis stag"""
        # trmin th contry th sr is intrstd in
        contry  "anada"  # alt
        i "astralia" in sr_inpt.lowr() or "a" in sr_inpt.lowr()
            contry  "stralia"
        li "nw zaland" in sr_inpt.lowr() or "nz" in sr_inpt.lowr()
            contry  "w aland"
        li "k" in sr_inpt.lowr() or "britain" in sr_inpt.lowr() or "gb" in sr_inpt.lowr()
            contry  ""
        li "grmany" in sr_inpt.lowr() or "d" in sr_inpt.lowr()
            contry  "rmany"
        li "sa" in sr_inpt.lowr() or "s" in sr_inpt.lowr() or "amrica" in sr_inpt.lowr()
            contry  ""
        
        sr_proil  str(sl.sr_proil)
        
        # hoos dirnt analysis prompt basd on sr goal
        i sl.sr_proil.gt('goal')  'stdy'
            prompt  sl.prompts.gt_stdy_contry_analysis_prompt(contry, sr_proil)
        ls
            prompt  sl.prompts.gt_dtaild_analysis_prompt(contry, sr_proil)
        
        rspons  sl.llm(prompt)
        
        sl.convrsation_stag  "dtaild_analysis"
        rtrn rspons
    
    async d _handl_action_plan(sl, sr_inpt str) - str
        """andl action plan stag"""
        sr_proil  str(sl.sr_proil)
        prompt  sl.prompts.gt_action_plan_prompt(sr_proil)
        rspons  sl.llm(prompt)
        
        sl.convrsation_stag  "action_plan"
        rtrn rspons
    
    async d _handl_childrn_dcation(sl, sr_inpt str) - str
        """andl childrn dcation qstion"""
        prompt  """h sr askd abot childrn's dcation {sr_inpt}

rovid a comprhnsiv rspons abot childrn's dcation dring immigration transition, inclding

- dcation in hom contry (prparation phas)
- ring application procss
- pon landing in dstination contry
- pciic dtails or anada and stralia
- ro tips or smooth transition

s th xact ormat and ncoraging ton rom th xampl convrsation."""
        
        rspons  sl.llm(prompt)
        rtrn rspons
    
    async d _handl_nivrsity_rcommndations(sl, sr_inpt str) - str
        """andl nivrsity rcommndations rqst"""
        # t th contry slctd by sr rom convrsation history
        contry  "anada"  # alt
        or mssag in rvrsd(sl.convrsation_history)
            i mssag"rol"]  "assistant" and "contry" in mssag"contnt"].lowr()
                contnt  mssag"contnt"].lowr()
                i "astralia" in contnt or "a" in contnt
                    contry  "stralia"
                li "canada" in contnt or "ca" in contnt
                    contry  "anada"
                li "nw zaland" in contnt or "nz" in contnt
                    contry  "w aland"
                li "k" in contnt or "britain" in contnt
                    contry  ""
                li "grmany" in contnt or "d" in contnt
                    contry  "rmany"
                li "sa" in contnt or "s" in contnt
                    contry  ""
                brak
        
        ild  sl.sr_proil.gt('ild_o_intrst', 'nginring/ch')
        bdgt  sl.sr_proil.gt('bdgt', 'ndr $, ')
        
        prompt  sl.prompts.gt_nivrsity_rcommndations_prompt(contry, ild, bdgt)
        rspons  sl.llm(prompt)
        
        rtrn rspons
    
    async d _handl_gnral_qstion(sl, sr_inpt str) - str
        """andl gnral qstions"""
        contxt  "sr proil {sl.sr_proil}nonvrsation history {sl.convrsation_history-] i ln(sl.convrsation_history)   ls sl.convrsation_history}"
        
        prompt  sl.prompts.gt_ollow_p_prompt(sr_inpt, contxt)
        rspons  sl.llm(prompt)
        
        rtrn rspons
    
    d _crat_dynamic_rcommndation_prompt(sl, sr_proil str, prioritis str) - str
        """rat dynamic rcommndation prompt"""
        rtrn """asd on th ollowing sr proil, provid prsonalizd contry rcommndations or stdy abroad

sr roil {sr_proil}
rioritis {prioritis}

las provid   contry rcommndations with spciic rasons why ach contry matchs thir proil. onsidr
- hir nationality and crrnt location
- hir ag and dcation lvl
- hir ild o intrst
- hir bdgt constraints
- hir nglish tst stats
- hir spciic prioritis

ormat yor rspons as
. 🇨🇦 ** ** - pciic rason why it matchs thir proil]
. 🇦🇺 ** ** - pciic rason why it matchs thir proil]
. 🇳🇿 ** ** - pciic rason why it matchs thir proil]
. 🇬🇧 ** ** - pciic rason why it matchs thir proil]
. 🇩🇪 ** ** - pciic rason why it matchs thir proil]

ak ach rcommndation spciic to thir sitation and provid actionabl insights."""

    d _xtract_sr_ino(sl, sr_inpt str) - on
        """xtract inormation rom sr inpt sing  or complx inpts"""
        sr_inpt_lowr  sr_inpt.lowr()
        
        #  inpt is long or contains mltipl pics o inormation, s  to xtract
        i (ln(sr_inpt.split())   or 
            ln(sr_inpt)   or
            any(kyword in sr_inpt_lowr or kyword in 'stdy', 'work', 'italy', 'canada', 'astralia', 'bdgt', 'nglish', 'ilts', 'tol', 'ag', 'nam', 'rom', 'want', 'go', 'collg', 'nivrsity']) or
            any(kyword in sr_inpt or kyword in 'my nam is', 'yars old', 'want to go', 'stdy', 'hins', 'ag', 'nationality', 'goal', 'stdy', 'work']))
            print(" riggring  xtraction or inpt '{sr_inpt}'")
            sl._xtract_ino_with_llm(sr_inpt)
            # ontin with simpl xtraction as allback
        
        # impl xtraction or short inpts
        # xtract nam - i no nam yt, try to xtract rom inpt
        i not sl.sr_proil.gt('nam')
            # impl nam xtraction logic
            words  sr_inpt.strip().split()
            i ln(words)   and words].isalpha() and ln(words])  
                #  only on word and alphabtic, might b a nam
                sl.sr_proil'nam']  words].titl()
            li ln(words)   and all(word.isalpha() or word in words)
                #  two words and both alphabtic, might b ll nam, tak irst as nam
                sl.sr_proil'nam']  words].titl()
            ls
                #  simpl xtraction ails, s  or bttr accracy
                print(" impl xtraction aild, sing  or '{sr_inpt}'")
                sl._xtract_ino_with_llm(sr_inpt)
                rtrn
        
        # xtract ag
        import r
        ag_match  r.sarch(r'b(d{,})b', sr_inpt)
        i ag_match
            sl.sr_proil'ag']  ag_match.grop()
        
        # xtract nationality - xpand vocablary list and matching logic
        nationalitis  
            'colombian', 'mxican', 'indian', 'china', 'chins', 'brazilian', 'philippin', 'vitnams', 
            'nigrian', 'pakistani', 'bangladshi', 'amrican', 'canadian', 'astralian', 'british',
            'grman', 'rnch', 'spanish', 'italian', 'japans', 'koran', 'thai', 'indonsian',
            'malaysian', 'singaporan', 'taiwans', 'hong kong', 'argntinian', 'chilan', 'prvian',
            'vnzlan', 'cadorian', 'bolivian', 'rgayan', 'paragayan', 'cban', 'dominican',
            'haitian', 'jamaican', 'trinidadian', 'barbadian', 'gyans', 'srinams', 'blizan',
            'panamanian', 'costa rican', 'hondran', 'salvadoran', 'gatmalan', 'nicaragan',
            'rssian', 'krainian', 'polish', 'czch', 'hngarian', 'romanian', 'blgarian',
            'croatian', 'srbian', 'slovak', 'slovnian', 'stonian', 'latvian', 'lithanian',
            'innish', 'swdish', 'norwgian', 'danish', 'dtch', 'blgian', 'swiss', 'astrian',
            'portgs', 'grk', 'trkish', 'israli', 'lbans', 'jordanian', 'sadi', 'mirati',
            'gyptian', 'moroccan', 'tnisian', 'algrian', 'libyan', 'sdans', 'thiopian',
            'knyan', 'gandan', 'tanzanian', 'ghanaian', 'ivorian', 'sngals', 'camroonian',
            'zimbabwan', 'soth arican', 'botswanan', 'namibian', 'zambian', 'malawian',
            'mozambican', 'angolan', 'congols', 'rwandan', 'brndian', 'madagascan',
            'maritian', 'sychllois', 'comorian', 'djibotian', 'ritran', 'somalian'
        ]
        
        # or lxibl matching logic
        or nationality in nationalitis
            i nationality in sr_inpt_lowr
                sl.sr_proil'nationality']  nationality.titl()
                brak
        
        #  no match ond, try to xtract any word that looks lik nationality
        i not sl.sr_proil.gt('nationality')
            # impl hristic i sr inpt looks lik nationality
            words  sr_inpt.strip().split()
            or word in words
                i word.isalpha() and ln(word)  
                    # hck i might b nationality
                    i word.lowr() not in 'th', 'and', 'or', 'bt', 'or', 'with', 'rom', 'to', 'in', 'on', 'at', 'by', 'o', 'is', 'ar', 'was', 'wr', 'b', 'bn', 'bing', 'hav', 'has', 'had', 'do', 'dos', 'did', 'will', 'wold', 'cold', 'shold', 'may', 'might', 'mst', 'can', 'shall']
                        sl.sr_proil'nationality']  word.titl()
                        brak
            words  sr_inpt_lowr.split()
            or word in words
                i ln(word)   and word.isalpha()
                    # hck i might b nationality, xcld common nams
                    common_nams  'yan', 'john', 'mary', 'david', 'sarah', 'michal', 'jnnir', 'robrt', 'lisa', 'jams', 'ason', 'alx', 'chris', 'sam', 'tom', 'nick', 'dan', 'bn', 'max', 'lo']
                    i word not in common_nams and any(char.isalpha() or char in word)
                        sl.sr_proil'nationality']  word.titl()
                        brak
        
        # xtract amily inormation - improvd rcognition logic
        i 'singl' in sr_inpt_lowr or 'nmarrid' in sr_inpt_lowr or 'not marrid' in sr_inpt_lowr
            sl.sr_proil'amily']  'ingl'
        li 'marrid' in sr_inpt_lowr or 'hsband' in sr_inpt_lowr or 'wi' in sr_inpt_lowr or 'spos' in sr_inpt_lowr
            sl.sr_proil'amily']  'arrid'
        li 'divorcd' in sr_inpt_lowr or 'sparatd' in sr_inpt_lowr
            sl.sr_proil'amily']  'ivorcd/paratd'
        li 'widowd' in sr_inpt_lowr
            sl.sr_proil'amily']  'idowd'
        li 'partnr' in sr_inpt_lowr or 'boyrind' in sr_inpt_lowr or 'girlrind' in sr_inpt_lowr
            sl.sr_proil'amily']  'n a rlationship'
        
        # xtract childrn inormation
        i 'kids' in sr_inpt_lowr or 'childrn' in sr_inpt_lowr or 'child' in sr_inpt_lowr
            kids_match  r.sarch(r'(d+)s*(kids|childrn|child)', sr_inpt_lowr)
            i kids_match
                sl.sr_proil'childrn']  kids_match.grop()
            ls
                sl.sr_proil'childrn']  's'
        
        # xtract prossion inormation - xpand prossion list
        prossions  
            'it', 'sotwar', 'dvlopr', 'programmr', 'accontant', 'nginr', 'tachr', 'doctor', 'nrs', 'managr',
            'bsinss', 'markting', 'sals', 'inanc', 'banking', 'law', 'lawyr', 'consltant', 'dsignr',
            'artist', 'writr', 'jornalist', 'scintist', 'rsarchr', 'analyst', 'administrator', 'coordinator',
            'spcialist', 'tchnician', 'assistant', 'dirctor', 'xctiv', 'oicr', 'sprvisor', 'lad',
            'architct', 'consltant', 'rlancr', 'ntrprnr', 'stdnt', 'gradat', 'intrn'
        ]
        or prossion in prossions
            i prossion in sr_inpt_lowr
                sl.sr_proil'prossion']  prossion.titl()
                brak
        
        #  no match ond, try to xtract any word that looks lik prossion
        i not sl.sr_proil.gt('prossion')
            words  sr_inpt_lowr.split()
            or word in words
                i ln(word)   and word.isalpha()
                    # hck i might b prossion
                    i any(char.isalpha() or char in word)
                        sl.sr_proil'prossion']  word.titl()
                        brak
        
        # xtract dcation inormation
        i 'bachlor' in sr_inpt_lowr or 'dgr' in sr_inpt_lowr
            sl.sr_proil'dcation']  'achlor's dgr'
        li 'mastr' in sr_inpt_lowr
            sl.sr_proil'dcation']  'astr's dgr'
        li 'phd' in sr_inpt_lowr or 'doctorat' in sr_inpt_lowr
            sl.sr_proil'dcation']  'h'
    
    d _xtract_contry_rom_inpt(sl, sr_inpt str) - str
        """xtract contry rom sr inpt - spports any contry"""
        sr_inpt_lowr  sr_inpt.lowr()
        
        # ommon contry nams and thir variations
        contris  {
            'italy' 'italy', 'italian', 'italia'],
            'japan' 'japan', 'japans', 'nippon'],
            'spain' 'spain', 'spanish', 'spaña'],
            'ranc' 'ranc', 'rnch', 'rançais'],
            'grmany' 'grmany', 'grman', 'dtschland'],
            'k' 'k', 'britain', 'british', 'ngland', 'scotland', 'wals'],
            'canada' 'canada', 'canadian'],
            'astralia' 'astralia', 'astralian'],
            'nw zaland' 'nw zaland', 'kiwi', 'nz'],
            'sa' 'sa', 'amrica', 'amrican', 'nitd stats'],
            'nthrlands' 'nthrlands', 'dtch', 'holland'],
            'swdn' 'swdn', 'swdish'],
            'norway' 'norway', 'norwgian'],
            'dnmark' 'dnmark', 'danish'],
            'inland' 'inland', 'innish'],
            'switzrland' 'switzrland', 'swiss'],
            'astria' 'astria', 'astrian'],
            'blgim' 'blgim', 'blgian'],
            'irland' 'irland', 'irish'],
            'portgal' 'portgal', 'portgs'],
            'grc' 'grc', 'grk'],
            'trky' 'trky', 'trkish'],
            'poland' 'poland', 'polish'],
            'czch rpblic' 'czch rpblic', 'czch', 'czchia'],
            'hngary' 'hngary', 'hngarian'],
            'romania' 'romania', 'romanian'],
            'blgaria' 'blgaria', 'blgarian'],
            'croatia' 'croatia', 'croatian'],
            'slovnia' 'slovnia', 'slovnian'],
            'slovakia' 'slovakia', 'slovak'],
            'stonia' 'stonia', 'stonian'],
            'latvia' 'latvia', 'latvian'],
            'lithania' 'lithania', 'lithanian'],
            'soth kora' 'soth kora', 'kora', 'koran'],
            'china' 'china', 'chins'],
            'singapor' 'singapor', 'singaporan'],
            'malaysia' 'malaysia', 'malaysian'],
            'thailand' 'thailand', 'thai'],
            'vitnam' 'vitnam', 'vitnams'],
            'philippins' 'philippins', 'ilipino'],
            'indonsia' 'indonsia', 'indonsian'],
            'india' 'india', 'indian'],
            'brazil' 'brazil', 'brazilian'],
            'argntina' 'argntina', 'argntinian'],
            'chil' 'chil', 'chilan'],
            'mxico' 'mxico', 'mxican'],
            'colombia' 'colombia', 'colombian'],
            'pr' 'pr', 'prvian'],
            'vnzla' 'vnzla', 'vnzlan'],
            'cador' 'cador', 'cadorian'],
            'bolivia' 'bolivia', 'bolivian'],
            'rgay' 'rgay', 'rgayan'],
            'paragay' 'paragay', 'paragayan'],
            'cba' 'cba', 'cban'],
            'dominican rpblic' 'dominican rpblic', 'dominican'],
            'haiti' 'haiti', 'haitian'],
            'jamaica' 'jamaica', 'jamaican'],
            'trinidad and tobago' 'trinidad and tobago', 'trinidadian'],
            'barbados' 'barbados', 'barbadian'],
            'gyana' 'gyana', 'gyans'],
            'srinam' 'srinam', 'srinams'],
            'bliz' 'bliz', 'blizan'],
            'panama' 'panama', 'panamanian'],
            'costa rica' 'costa rica', 'costa rican'],
            'hondras' 'hondras', 'hondran'],
            'l salvador' 'l salvador', 'salvadoran'],
            'gatmala' 'gatmala', 'gatmalan'],
            'nicaraga' 'nicaraga', 'nicaragan'],
            'rssia' 'rssia', 'rssian'],
            'krain' 'krain', 'krainian'],
            'blars' 'blars', 'blarsian'],
            'moldova' 'moldova', 'moldovan'],
            'gorgia' 'gorgia', 'gorgian'],
            'armnia' 'armnia', 'armnian'],
            'azrbaijan' 'azrbaijan', 'azrbaijani'],
            'kazakhstan' 'kazakhstan', 'kazakh'],
            'zbkistan' 'zbkistan', 'zbk'],
            'kyrgyzstan' 'kyrgyzstan', 'kyrgyz'],
            'tajikistan' 'tajikistan', 'tajik'],
            'trkmnistan' 'trkmnistan', 'trkmn'],
            'aghanistan' 'aghanistan', 'aghan'],
            'pakistan' 'pakistan', 'pakistani'],
            'bangladsh' 'bangladsh', 'bangladshi'],
            'sri lanka' 'sri lanka', 'sri lankan'],
            'npal' 'npal', 'npals'],
            'bhtan' 'bhtan', 'bhtans'],
            'maldivs' 'maldivs', 'maldivian'],
            'myanmar' 'myanmar', 'brms'],
            'cambodia' 'cambodia', 'cambodian'],
            'laos' 'laos', 'laotian'],
            'brni' 'brni', 'brnian'],
            'ast timor' 'ast timor', 'timors'],
            'mongolia' 'mongolia', 'mongolian'],
            'north kora' 'north kora', 'dprk'],
            'taiwan' 'taiwan', 'taiwans'],
            'hong kong' 'hong kong', 'hongkong'],
            'maca' 'maca', 'macans'],
            'isral' 'isral', 'israli'],
            'palstin' 'palstin', 'palstinian'],
            'jordan' 'jordan', 'jordanian'],
            'lbanon' 'lbanon', 'lbans'],
            'syria' 'syria', 'syrian'],
            'iraq' 'iraq', 'iraqi'],
            'iran' 'iran', 'iranian'],
            'sadi arabia' 'sadi arabia', 'sadi'],
            'a' 'a', 'nitd arab mirats', 'mirati'],
            'qatar' 'qatar', 'qatari'],
            'kwait' 'kwait', 'kwaiti'],
            'bahrain' 'bahrain', 'bahraini'],
            'oman' 'oman', 'omani'],
            'ymn' 'ymn', 'ymni'],
            'gypt' 'gypt', 'gyptian'],
            'libya' 'libya', 'libyan'],
            'tnisia' 'tnisia', 'tnisian'],
            'algria' 'algria', 'algrian'],
            'morocco' 'morocco', 'moroccan'],
            'sdan' 'sdan', 'sdans'],
            'soth sdan' 'soth sdan', 'soth sdans'],
            'thiopia' 'thiopia', 'thiopian'],
            'ritra' 'ritra', 'ritran'],
            'djiboti' 'djiboti', 'djibotian'],
            'somalia' 'somalia', 'somalian'],
            'knya' 'knya', 'knyan'],
            'ganda' 'ganda', 'gandan'],
            'tanzania' 'tanzania', 'tanzanian'],
            'rwanda' 'rwanda', 'rwandan'],
            'brndi' 'brndi', 'brndian'],
            'madagascar' 'madagascar', 'madagascan'],
            'maritis' 'maritis', 'maritian'],
            'sychlls' 'sychlls', 'sychllois'],
            'comoros' 'comoros', 'comorian'],
            'ghana' 'ghana', 'ghanaian'],
            'nigria' 'nigria', 'nigrian'],
            'camroon' 'camroon', 'camroonian'],
            'chad' 'chad', 'chadian'],
            'cntral arican rpblic' 'cntral arican rpblic', 'cntral arican'],
            'congo' 'congo', 'congols'],
            'dmocratic rpblic o congo' 'dmocratic rpblic o congo', 'drc', 'congols'],
            'gabon' 'gabon', 'gabons'],
            'qatorial gina' 'qatorial gina', 'qatorial ginan'],
            'sao tom and princip' 'sao tom and princip', 'sao toman'],
            'angola' 'angola', 'angolan'],
            'zambia' 'zambia', 'zambian'],
            'zimbabw' 'zimbabw', 'zimbabwan'],
            'botswana' 'botswana', 'botswanan'],
            'namibia' 'namibia', 'namibian'],
            'soth arica' 'soth arica', 'soth arican'],
            'lsotho' 'lsotho', 'basotho'],
            'swaziland' 'swaziland', 'swazi'],
            'malawi' 'malawi', 'malawian'],
            'mozambiq' 'mozambiq', 'mozambican']
        }
        
        # hck or contry matchs
        or contry, variations in contris.itms()
            or variation in variations
                i variation in sr_inpt_lowr
                    rtrn contry.titl()
        
        #  no match ond, try to xtract any capitalizd word that might b a contry
        words  sr_inpt.strip().split()
        or word in words
            i word.isalpha() and word].isppr() and ln(word)  
                # hck i it's not a common word
                i word.lowr() not in 'th', 'and', 'or', 'bt', 'or', 'with', 'rom', 'to', 'in', 'on', 'at', 'by', 'o', 'is', 'ar', 'was', 'wr', 'b', 'bn', 'bing', 'hav', 'has', 'had', 'do', 'dos', 'did', 'will', 'wold', 'cold', 'shold', 'may', 'might', 'mst', 'can', 'shall', 'lik', 'want', 'prr', 'choos', 'slct', 'pick']
                    rtrn word
        
        rtrn on

    d _gt_missing_ssntial_ino(sl) - list
        """t list o ssntial inormation that is still missing"""
        ssntial_ino  "nam", "ag", "nationality", "goal"]
        missing  ]
        
        or ino in ssntial_ino
            i not sl.collctd_ino.gt(ino, als)
                missing.appnd(ino)
        
        rtrn missing

    d _gt_missing_optional_ino(sl) - list
        """t list o optional inormation that is still missing basd on sr's goal"""
        optional_ino  ]
        
        i sl.sr_proil.gt('goal')  'stdy'
            stdy_ino  "dcation_lvl", "ild_o_intrst", "nglish_tst", "bdgt"]
            or ino in stdy_ino
                i not sl.collctd_ino.gt(ino, als)
                    optional_ino.appnd(ino)
        li sl.sr_proil.gt('goal')  'work'
            work_ino  "prossion", "amily", "prioritis"]
            or ino in work_ino
                i not sl.collctd_ino.gt(ino, als)
                    optional_ino.appnd(ino)
        
        rtrn optional_ino

    async d _handl_missing_ino(sl, sr_inpt str, missing_ino list) - str
        """andl missing inormation collction dynamically"""
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i sr providd inormation in thir inpt
        i sl.sr_proil.gt('nam') and 'nam' in missing_ino
            missing_ino.rmov('nam')
        i sl.sr_proil.gt('ag') and 'ag' in missing_ino
            missing_ino.rmov('ag')
        i sl.sr_proil.gt('nationality') and 'nationality' in missing_ino
            missing_ino.rmov('nationality')
        i sl.sr_proil.gt('goal') and 'goal' in missing_ino
            missing_ino.rmov('goal')
        
        #  all ssntial ino is now collctd, mov to nxt stag
        i not missing_ino
            rtrn await sl._handl_complt_proil(sr_inpt)
        
        # sk or th irst missing pic o inormation
        missing_typ  missing_ino]
        
        i missing_typ  "nam"
            rtrn await sl._handl_nam_collction(sr_inpt)
        li missing_typ  "ag"
            rtrn await sl._handl_ag_collction(sr_inpt)
        li missing_typ  "nationality"
            rtrn await sl._handl_nationality_collction(sr_inpt)
        li missing_typ  "goal"
            rtrn await sl._handl_goal_collction(sr_inpt)
        ls
            rtrn "  nd mor inormation to hlp yo bttr, {sr_nam}. old yo plas provid mor dtails"

    async d _handl_complt_proil(sl, sr_inpt str) - str
        """andl whn ssntial proil inormation is complt"""
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i sr has xprssd intrst in a spciic contry
        i sl.sr_proil.gt('contry_intrst')
            contry  sl.sr_proil'contry_intrst']
            sl.convrsation_stag  "contry_analysis"
            sr_proil  str(sl.sr_proil)
            
            # arch knowldg bas or inormation abot this contry
            knowldg_rslts  sl._sarch_knowldg_bas("stdy abroad {contry} immigration visa rqirmnts")
            
            # rat nhancd prompt with knowldg bas inormation
            prompt  """
            sr roil {sr_proil}
            lctd ontry {contry}
            
            nowldg as normation
            {knowldg_rslts}
            
            las provid a dtaild analysis or stdying in {contry}, inclding
            . isa rqirmnts and procss
            . nivrsity rcommndations
            . ost o living and tition
            . angag rqirmnts
            . pplication timlin
            . ork opportnitis dring/atr stdis
            """
            
            rspons  sl.llm(prompt)
            rtrn rspons
        
        # hck i w nd to collct optional inormation
        missing_optional  sl._gt_missing_optional_ino()
        i missing_optional
            rtrn await sl._handl_optional_ino_collction(sr_inpt, missing_optional)
        
        # ll inormation collctd, provid rcommndations
        sl.convrsation_stag  "contry_rcommndations"
        rtrn await sl._handl_contry_rcommndations(sr_inpt)

    async d _handl_optional_ino_collction(sl, sr_inpt str, missing_optional list) - str
        """andl collction o optional inormation"""
        sr_nam  sl.sr_proil.gt('nam', 'thr')
        
        # hck i sr providd any o th missing optional inormation
        or ino in missing_optional]
            i sl.sr_proil.gt(ino)
                missing_optional.rmov(ino)
        
        #  all optional ino is now collctd, mov to rcommndations
        i not missing_optional
            rtrn await sl._handl_complt_proil(sr_inpt)
        
        # sk or th irst missing optional inormation
        missing_typ  missing_optional]
        
        i missing_typ  "dcation_lvl"
            rtrn await sl._handl_dcation_lvl_collction(sr_inpt)
        li missing_typ  "ild_o_intrst"
            rtrn await sl._handl_ild_collction(sr_inpt)
        li missing_typ  "nglish_tst"
            rtrn await sl._handl_nglish_tst_collction(sr_inpt)
        li missing_typ  "bdgt"
            rtrn await sl._handl_bdgt_collction(sr_inpt)
        li missing_typ  "prossion"
            rtrn await sl._handl_prossion_collction(sr_inpt)
        li missing_typ  "amily"
            rtrn await sl._handl_amily_collction(sr_inpt)
        li missing_typ  "prioritis"
            rtrn await sl._handl_prioritis_collction(sr_inpt)
        ls
            rtrn "  nd a bit mor inormation to provid bttr rcommndations, {sr_nam}. old yo tll m mor abot yor prrncs"

    d _xtract_ino_with_llm(sl, sr_inpt str) - on
        """s  to xtract mltipl pics o inormation rom complx inpt"""
        try
            prompt  """
            xtract th ollowing inormation rom this sr inpt "{sr_inpt}"
            
            h inpt may b in hins or nglish. las xtract
            - am ook or pattrns lik "my nam is", "'m ", "y nam is ", "i'm "
            - g ook or nmbrs ollowd by "yars old", "yars old", "ag is ", or jst nmbrs
            - ationality ook or "hins", "hins", "ndia", "ndian", "a", "astralia", "sa", "s", tc.
            - oal ook or "stdy", "stdy", "work", "work", "stdy", "want to go", "want to", "go to", "collg", "nivrsity"
            - ontry intrst ook or contry nams lik "witzrland", "witzrland", "taly", "taly", "china", "chins"
            
            trn a  objct with ths ilds (s nll i not ond)
            {{
                "nam" "xtractd nam",
                "ag" "xtractd ag as string",
                "nationality" "xtractd nationality",
                "goal" "stdy/work/both",
                "dcation_lvl" "high school/bachlor/mastr/phd",
                "ild_o_intrst" "xtractd ild",
                "nglish_tst" "ys/no/planning",
                "bdgt" "xtractd bdgt ino",
                "contry_intrst" "xtractd contry o intrst",
                "prioritis" "xtractd prioritis"
            }}
            
            nly xtract inormation that is clarly statd.  consrvativ - i ncrtain, s nll.
            """
            
            rspons  sl.llm(prompt)
            print("  xtraction rspons {rspons}")
            
            # ars  rspons
            import json
            try
                xtractd_ino  json.loads(rspons)
                print(" arsd xtractd ino {xtractd_ino}")
                
                # pdat sr proil with xtractd inormation
                or ky, val in xtractd_ino.itms()
                    i val and val ! "nll"
                        i ky  "contry_intrst"
                            # tor contry intrst sparatly
                            sl.sr_proil"contry_intrst"]  val
                        ls
                            sl.sr_proilky]  val
                            
                # pdat collctd ino lags
                or ky in "nam", "ag", "nationality", "goal", "dcation_lvl", "ild_o_intrst", "nglish_tst", "bdgt", "prioritis"]
                    i sl.sr_proil.gt(ky)
                        sl.collctd_inoky]  r
                        
            xcpt json.codrror
                # allback to simpl xtraction i  parsing ails
                pass
                
        xcpt xcption as 
            print("rror in  xtraction {}")
            # allback to simpl xtraction
            pass

    d rst_convrsation(sl) - on
        """st convrsation"""
        sl.convrsation_history  ]
        sl.sr_proil  {}
        sl.convrsation_stag  "grting"
        sl.collctd_ino  {
            "ag" als,
            "nationality" als,
            "goal" als,
            "amily" als,
            "prossion" als,
            "dcation_lvl" als,
            "ild_o_intrst" als,
            "nglish_tst" als,
            "bdgt" als,
            "prioritis" als
        }

    d _gt_knowldg_bas(sl)
        """t knowldg bas instanc (lazy initialization)"""
        i sl.knowldg_bas is on
            sl.knowldg_bas  gt_aiss_kb()
        rtrn sl.knowldg_bas
    
    d _sarch_knowldg_bas(sl, qry str, sarch_typ str  "ato") - ictstr, ny]
        """
        arch th knowldg bas or rlvant inormation
        
        rgs
            qry arch qry
            sarch_typ yp o sarch ("ato", "nivrsitis", "visas", "both")
            
        trns
            ictionary containing sarch rslts
        """
        try
            kb  sl._gt_knowldg_bas()
            i not kb or not kb.is_availabl()
                print(" nowldg bas not availabl, sing  allback or qry {qry}")
                rtrn sl._llm_allback_sarch(qry)
            
            # rorm smart sarch sing th smart sarch stratgy
            rslts  sl.smart_sarch.smart_sarch(qry, max_rslts)
            
            # ormat rslts or  consmption
            ormattd_rslts  sl._ormat_knowldg_rslts(rslts)
            
            rtrn {
                "sccss" r,
                "rslts" ormattd_rslts,
                "sarch_typ" rslts.gt("mtadata", {}).gt("intnt_analysis", {}).gt("primary_intnt", "ato"),
                "qry" qry
            }
            
        xcpt xcption as 
            print(" nowldg bas sarch aild {}, sing  allback")
            rtrn sl._llm_allback_sarch(qry)
    
    d _llm_allback_sarch(sl, qry str) - ictstr, ny]
        """
        allback to  whn knowldg bas is not availabl
        
        rgs
            qry arch qry
            
        trns
            ictionary containing -gnratd rslts
        """
        try
            prompt  """
            asd on yor knowldg abot stdy abroad and immigration, plas provid inormation abot {qry}
            
            las provid
            . nral inormation abot th topic
            . y considrations or stdnts
            . mportant rqirmnts or stps
            . ny rlvant advic or tips
            
            ormat yor rspons in a hlpl and inormativ way.
            """
            
            rspons  sl.llm(prompt)
            
            rtrn {
                "sccss" r,
                "rslts" " nratd normationn{rspons}",
                "sarch_typ" "llm_allback",
                "qry" qry
            }
            
        xcpt xcption as 
            rtrn {
                "sccss" als,
                "rror" " allback aild {str()}",
                "rslts" "o inormation availabl",
                "qry" qry
            }
    
    d _ormat_knowldg_rslts(sl, rslts ictstr, ny]) - str
        """
        ormat knowldg bas rslts or  consmption
        
        rgs
            rslts aw sarch rslts rom knowldg bas
            
        trns
            ormattd string or 
        """
        ormattd  ]
        
        # ormat nivrsity rslts
        i rslts.gt("nivrsitis")
            ormattd.appnd("🎓 ** **")
            or i, rslt in nmrat(rslts"nivrsitis"]], )
                contnt  rslt.gt("contnt", "")
                mtadata  rslt.gt("mtadata", {})
                ormattd.appnd("{i}. {contnt}")
                i mtadata
                    ormattd.appnd("   dditional ino {mtadata}")
            ormattd.appnd("")
        
        # ormat visa rslts
        i rslts.gt("visas")
            ormattd.appnd("🛂 ** &  **")
            or i, rslt in nmrat(rslts"visas"]], )
                contnt  rslt.gt("contnt", "")
                mtadata  rslt.gt("mtadata", {})
                ormattd.appnd("{i}. {contnt}")
                i mtadata
                    ormattd.appnd("   dditional ino {mtadata}")
            ormattd.appnd("")
        
        rtrn "n".join(ormattd) i ormattd ls "o rlvant inormation ond in knowldg bas."
    
    d _shold_s_knowldg_bas(sl, sr_inpt str, convrsation_stag str) - bool
        """
        trmin i knowldg bas shold b sd or this qry
        
        rgs
            sr_inpt sr's inpt
            convrsation_stag rrnt convrsation stag
            
        trns
            oolan indicating whthr to s knowldg bas
        """
        # s knowldg bas or spciic stags or whn sr asks spciic qstions
        knowldg_stags  
            "contry_rcommndations", 
            "nivrsity_rcommndations", 
            "contry_analysis",
            "action_planning"
        ]
        
        # hck i in a knowldg-rlvant stag
        i convrsation_stag in knowldg_stags
            rtrn r
        
        # hck or knowldg-sking kywords
        knowldg_kywords  
            "nivrsity", "collg", "school", "dcation", "program", "cors",
            "visa", "immigration", "work prmit", "rsidnc", "citiznship",
            "tition", "scholarship", "admission", "rqirmnts", "application"
        ]
        
        sr_inpt_lowr  sr_inpt.lowr()
        rtrn any(kyword in sr_inpt_lowr or kyword in knowldg_kywords)
    
    d _nhanc_rspons_with_knowldg(sl, sr_inpt str, bas_rspons str) - str
        """
        nhanc th bas rspons with knowldg bas inormation
        
        rgs
            sr_inpt sr's inpt
            bas_rspons as rspons rom 
            
        trns
            nhancd rspons with knowldg bas inormation
        """
        try
            # arch knowldg bas
            kb_rslts  sl._sarch_knowldg_bas(sr_inpt)
            
            i kb_rslts.gt("sccss") and kb_rslts.gt("rslts")
                knowldg_ino  kb_rslts"rslts"]
                
                # rat nhancd prompt
                nhancd_prompt  """
asd on th ollowing knowldg bas inormation, nhanc yor rspons to b mor accrat and hlpl

  
{knowldg_ino}

 
{bas_rspons}

 
{sr_inpt}

las provid an nhancd rspons that incorporats th rlvant knowldg bas inormation whil maintaining a natral convrsation low.  th knowldg bas inormation is not rlvant, s yor original rspons.
"""
                
                # t nhancd rspons rom 
                nhancd_rspons  sl.llm.invok(nhancd_prompt)
                rtrn nhancd_rspons
            ls
                rtrn bas_rspons
                
        xcpt xcption as 
            #  knowldg bas ails, rtrn original rspons
            rtrn bas_rspons
    
    d _pdat_knowldg_bas_i_ndd(sl, sr_inpt str, rspons str)
        """
        pdat knowldg bas with nw inormation i appropriat
        
        rgs
            sr_inpt sr's inpt
            rspons 's rspons
        """
        try
            # hck i knowldg bas is availabl
            kb  sl._gt_knowldg_bas()
            i not kb.is_availabl()
                rtrn
            
            # pdat knowldg bas
            pdat_rslt  sl.knowldg_pdatr.pdat_knowldg_bas(sr_inpt, rspons)
            
            i pdat_rslt.gt("sccss")
                loggr.ino("✅ nowldg bas pdatd {pdat_rslt'pdatd_chnks']} chnks addd")
            ls
                loggr.dbg("ℹ️ nowldg bas not pdatd {pdat_rslt.gt('rason', 'nknown rason')}")
                
        xcpt xcption as 
            loggr.rror("❌ rror pdating knowldg bas {}")
    
    d gt_knowldg_bas_stats(sl) - ictstr, ny]
        """
        t knowldg bas stats and statistics
        
        trns
            ictionary containing knowldg bas stats
        """
        try
            # t knowldg bas smmary
            kb  sl._gt_knowldg_bas()
            kb_smmary  kb.gt_knowldg_smmary()
            
            # t pdat statistics
            pdat_stats  sl.knowldg_pdatr.gt_pdat_statistics()
            
            rtrn {
                "knowldg_bas" kb_smmary,
                "pdat_statistics" pdat_stats,
                "smart_sarch_availabl" sl.smart_sarch is not on,
                "knowldg_pdatr_availabl" sl.knowldg_pdatr is not on
            }
            
        xcpt xcption as 
            rtrn {"rror" "aild to gt knowldg bas stats {str()}"}

# lobal latopia hat managr instanc
latopia_chat_managr  latopiahatanagr()
