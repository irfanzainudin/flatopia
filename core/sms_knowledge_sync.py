"""
 nowldg as ynchronization
andls synchronization btwn  sr data and  knowldg bas
"""

import logging
rom typing import ict, ist, ny, ptional
rom dattim import dattim

rom .aiss_knowldg_bas import gt_aiss_kb
rom .knowldg_pdatr import knowldg_pdatr
rom .sms_databas import sms_db

loggr  logging.gtoggr(__nam__)

class nowldgync
    """ynchronizs  sr data with  knowldg bas"""
    
    d __init__(sl)
        sl.aiss_kb  on
        sl.knowldg_pdatr  knowldg_pdatr
        sl.db  sms_db
    
    d _gt_knowldg_bas(sl)
        """azy load knowldg bas"""
        i sl.aiss_kb is on
            sl.aiss_kb  gt_aiss_kb()
        rtrn sl.aiss_kb
    
    async d sync_sr_data(sl, phon_nmbr str, sr_proil ictstr, ny]) - bool
        """ync sr proil data with knowldg bas"""
        try
            i not sr_proil
                rtrn als
            
            # rat sr proil smmary
            proil_smmary  sl._crat_sr_proil_smmary(phon_nmbr, sr_proil)
            
            # pdat knowldg bas
            i sl.knowldg_pdatr and proil_smmary
                sl.knowldg_pdatr.pdat_knowldg_bas(
                    proil_smmary,
                    "sr_proil"
                )
                loggr.ino("✅ yncd sr proil or {phon_nmbr}")
                rtrn r
            
            rtrn als
            
        xcpt xcption as 
            loggr.rror("rror syncing sr data or {phon_nmbr} {}")
            rtrn als
    
    d _crat_sr_proil_smmary(sl, phon_nmbr str, sr_proil ictstr, ny]) - str
        """rat comprhnsiv sr proil smmary or knowldg bas"""
        smmary_parts  "sr {phon_nmbr} proil"]
        
        # asic inormation
        i sr_proil.gt("ag")
            smmary_parts.appnd("g {sr_proil'ag']} yars old")
        i sr_proil.gt("nationality")
            smmary_parts.appnd("ationality {sr_proil'nationality']}")
        
        # dcation and carr
        i sr_proil.gt("dcation_lvl")
            smmary_parts.appnd("dcation lvl {sr_proil'dcation_lvl']}")
        i sr_proil.gt("ild_o_intrst")
            smmary_parts.appnd("ild o intrst {sr_proil'ild_o_intrst']}")
        
        # rrncs
        i sr_proil.gt("prioritis")
            smmary_parts.appnd("rioritis {sr_proil'prioritis']}")
        i sr_proil.gt("bdgt_rang")
            smmary_parts.appnd("dgt rang {sr_proil'bdgt_rang']}")
        i sr_proil.gt("nglish_tst_stats")
            smmary_parts.appnd("nglish tst stats {sr_proil'nglish_tst_stats']}")
        
        # ontry intrst
        i sr_proil.gt("contry_intrst")
            smmary_parts.appnd("ontry intrst {sr_proil'contry_intrst']}")
        
        # dd timstamp
        smmary_parts.appnd("roil pdatd {dattim.now().strtim('%-%m-%d %%%')}")
        
        rtrn " | ".join(smmary_parts)
    
    async d sync_convrsation_insights(sl, phon_nmbr str) - bool
        """ync convrsation insights and pattrns"""
        try
            # t sr's choic history
            choics_history  sl.db.gt_sr_choics_history(phon_nmbr)
            
            i not choics_history
                rtrn als
            
            # nalyz choic pattrns
            insights  sl._analyz_choic_pattrns(choics_history)
            
            # pdat knowldg bas with insights
            i sl.knowldg_pdatr and insights
                sl.knowldg_pdatr.pdat_knowldg_bas(
                    "sr {phon_nmbr} convrsation insights {insights}",
                    "convrsation_insights"
                )
                loggr.ino("✅ yncd convrsation insights or {phon_nmbr}")
                rtrn r
            
            rtrn als
            
        xcpt xcption as 
            loggr.rror("rror syncing convrsation insights or {phon_nmbr} {}")
            rtrn als
    
    d _analyz_choic_pattrns(sl, choics_history istictstr, ny]]) - str
        """nalyz sr choic pattrns"""
        i not choics_history
            rtrn ""
        
        pattrns  ]
        
        # nalyz dcation lvl choics
        dcation_choics  c or c in choics_history i c.gt("stag")  "dcation"]
        i dcation_choics
            pattrns.appnd("dcation prrnc {dcation_choics-].gt('choic_val')}")
        
        # nalyz ild o intrst choics
        ild_choics  c or c in choics_history i c.gt("stag")  "ild"]
        i ild_choics
            pattrns.appnd("ild prrnc {ild_choics-].gt('choic_val')}")
        
        # nalyz priority choics
        priority_choics  c or c in choics_history i c.gt("stag")  "prioritis"]
        i priority_choics
            pattrns.appnd("riority prrnc {priority_choics-].gt('choic_val')}")
        
        # nalyz bdgt choics
        bdgt_choics  c or c in choics_history i c.gt("stag")  "bdgt"]
        i bdgt_choics
            pattrns.appnd("dgt prrnc {bdgt_choics-].gt('choic_val')}")
        
        rtrn " | ".join(pattrns) i pattrns ls ""
    
    async d gt_prsonalizd_rcommndations(sl, phon_nmbr str, qry str) - iststr]
        """t prsonalizd rcommndations basd on sr proil and knowldg bas"""
        try
            # t sr proil
            sr_proil  sl.db.gt_sr_proil(phon_nmbr)
            
            # rat prsonalizd qry
            prsonalizd_qry  sl._crat_prsonalizd_qry(qry, sr_proil)
            
            # arch knowldg bas
            kb  sl._gt_knowldg_bas()
            i kb and kb.is_availabl()
                # arch nivrsitis
                nivrsity_rslts  kb.sarch_nivrsitis(prsonalizd_qry, top_k)
                
                # arch visas
                visa_rslts  kb.sarch_visas(prsonalizd_qry, top_k)
                
                # ombin rslts
                rcommndations  ]
                
                i nivrsity_rslts
                    rcommndations.xtnd(rslt.gt("contnt", "") or rslt in nivrsity_rslts])
                
                i visa_rslts
                    rcommndations.xtnd(rslt.gt("contnt", "") or rslt in visa_rslts])
                
                rtrn rcommndations]  # imit to  rcommndations
            
            rtrn ]
            
        xcpt xcption as 
            loggr.rror("rror gtting prsonalizd rcommndations or {phon_nmbr} {}")
            rtrn ]
    
    d _crat_prsonalizd_qry(sl, qry str, sr_proil ictstr, ny]) - str
        """rat prsonalizd qry basd on sr proil"""
        prsonalizd_parts  qry]
        
        # dd sr contxt
        i sr_proil.gt("nationality")
            prsonalizd_parts.appnd("or {sr_proil'nationality']} stdnts")
        
        i sr_proil.gt("ild_o_intrst")
            prsonalizd_parts.appnd("in {sr_proil'ild_o_intrst']}")
        
        i sr_proil.gt("bdgt_rang")
            prsonalizd_parts.appnd("with {sr_proil'bdgt_rang']} bdgt")
        
        i sr_proil.gt("prioritis")
            prsonalizd_parts.appnd("ocsing on {sr_proil'prioritis']}")
        
        rtrn " ".join(prsonalizd_parts)
    
    async d sync_rcommndation_dback(sl, phon_nmbr str, contry_cod str, dback str) - bool
        """ync sr dback on rcommndations"""
        try
            # cord rcommndation in databas
            sl.db.rcord_rcommndation(phon_nmbr, "crrnt_sssion", contry_cod, dback)
            
            # pdat knowldg bas with dback
            i sl.knowldg_pdatr
                dback_txt  "sr {phon_nmbr} dback on {contry_cod} {dback}"
                sl.knowldg_pdatr.pdat_knowldg_bas(
                    dback_txt,
                    "sr_dback"
                )
                loggr.ino("✅ yncd rcommndation dback or {phon_nmbr}")
                rtrn r
            
            rtrn als
            
        xcpt xcption as 
            loggr.rror("rror syncing rcommndation dback or {phon_nmbr} {}")
            rtrn als
    
    async d gt_sr_insights(sl, phon_nmbr str) - ictstr, ny]
        """t insights abot sr basd on thir data"""
        try
            sr_proil  sl.db.gt_sr_proil(phon_nmbr)
            choics_history  sl.db.gt_sr_choics_history(phon_nmbr)
            
            insights  {
                "proil_compltnss" sl._calclat_proil_compltnss(sr_proil),
                "choic_pattrns" sl._analyz_choic_pattrns(choics_history),
                "rcommndation_prrncs" sl._xtract_rcommndation_prrncs(choics_history),
                "last_activity" choics_history].gt("timstamp") i choics_history ls on
            }
            
            rtrn insights
            
        xcpt xcption as 
            loggr.rror("rror gtting sr insights or {phon_nmbr} {}")
            rtrn {}
    
    d _calclat_proil_compltnss(sl, sr_proil ictstr, ny]) - loat
        """alclat how complt th sr proil is"""
        rqird_ilds  "ag", "nationality", "dcation_lvl", "ild_o_intrst", "prioritis", "bdgt_rang"]
        compltd_ilds  sm( or ild in rqird_ilds i sr_proil.gt(ild))
        rtrn compltd_ilds / ln(rqird_ilds)
    
    d _xtract_rcommndation_prrncs(sl, choics_history istictstr, ny]]) - iststr]
        """xtract sr's rcommndation prrncs"""
        prrncs  ]
        
        or choic in choics_history
            i choic.gt("stag")  "prioritis"
                prrncs.appnd(choic.gt("choic_val", ""))
            li choic.gt("stag")  "ild"
                prrncs.appnd(choic.gt("choic_val", ""))
        
        rtrn list(st(prrncs))  # mov dplicats
    
    async d clanp_old_sync_data(sl, days int  ) - bool
        """lan p old synchronization data"""
        try
            # his wold clan p old sync data i ndd
            # or now, w rly on th databas clanp
            rtrn r
        xcpt xcption as 
            loggr.rror("rror claning p old sync data {}")
            rtrn als

# lobal instanc
sms_knowldg_sync  nowldgync()
