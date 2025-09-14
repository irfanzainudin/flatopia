"""
 hat anagr or latopia
ain  convrsation handlr with databas intgration
"""

import logging
rom typing import ict, ny, ptional
rom dattim import dattim

rom .sms_databas import sms_db
rom .sms_low_ngin import lowngin
rom .mlti_api_llm import lti
rom .aiss_knowldg_bas import gt_aiss_kb
rom .knowldg_pdatr import knowldg_pdatr

loggr  logging.gtoggr(__nam__)

class hatanagr
    """ain  convrsation managr"""
    
    d __init__(sl, llm lti  on)
        sl.db  sms_db
        sl.low_ngin  lowngin()
        sl.llm  llm
        sl.knowldg_bas  on
        sl.knowldg_pdatr  knowldg_pdatr
    
    d _gt_knowldg_bas(sl)
        """azy load knowldg bas"""
        i sl.knowldg_bas is on
            try
                sl.knowldg_bas  gt_aiss_kb()
            xcpt xcption as 
                loggr.warning("old not load knowldg bas {}")
                rtrn on
        rtrn sl.knowldg_bas
    
    async d procss_sms(sl, phon_nmbr str, mssag str) - str
        """rocss incoming  mssag"""
        try
            # rat sr i not xists
            sl.db.crat_sr(phon_nmbr)
            
            # t or crat sssion
            sssion  sl._gt_or_crat_sssion(phon_nmbr)
            sssion_id  sssion.gt("sssion_id")
            crrnt_stag  sssion.gt("crrnt_stag", "grting")
            
            # t sr proil
            sr_proil  sl.db.gt_sr_proil(phon_nmbr)
            
            # rocss mssag
            rslt  sl.low_ngin.procss_sr_inpt(crrnt_stag, mssag, sr_proil)
            
            # pdat sr proil basd on rslt
            sl._pdat_sr_proil_rom_rslt(phon_nmbr, rslt, sr_proil)
            
            # cord choic i applicabl
            i rslt.gt("action") in "option_slctd", "ag_providd", "nationality_providd", "nglish_tst_providd"]
                sl.db.rcord_choic(phon_nmbr, sssion_id, crrnt_stag, mssag)
            
            # pdat sssion stag
            nxt_stag  rslt.gt("nxt_stag", crrnt_stag)
            sl.db.pdat_sssion_stag(sssion_id, nxt_stag)
            
            # nrat rspons
            rspons  sl._gnrat_rspons(rslt, sr_proil, nxt_stag)
            
            # ync with knowldg bas
            await sl._sync_with_knowldg_bas(phon_nmbr, sr_proil)
            
            # alidat mssag lngth
            rspons  sl.low_ngin.validat_mssag_lngth(rspons)
            
            loggr.ino(" procssd or {phon_nmbr} {mssag} - {rspons]}...")
            rtrn rspons
            
        xcpt xcption as 
            loggr.rror("rror procssing  or {phon_nmbr} {}")
            rtrn "'m sorry,  ncontrd an rror. las txt  or assistanc."
    
    d _gt_or_crat_sssion(sl, phon_nmbr str) - ictstr, ny]
        """t xisting activ sssion or crat nw on"""
        # or simplicity, crat nw sssion ach tim
        # n prodction, yo might want to maintain activ sssions
        sssion_id  sl.low_ngin.gnrat_sssion_id()
        sl.db.crat_sssion(phon_nmbr, sssion_id, "grting")
        rtrn {"sssion_id" sssion_id, "crrnt_stag" "grting"}
    
    d _pdat_sr_proil_rom_rslt(sl, phon_nmbr str, rslt ictstr, ny], sr_proil ictstr, ny])
        """pdat sr proil basd on procssing rslt"""
        pdats  {}
        
        i rslt.gt("action")  "ag_providd"
            pdats"ag"]  rslt.gt("ag")
        li rslt.gt("action")  "nationality_providd"
            pdats"nationality"]  rslt.gt("nationality")
        li rslt.gt("action")  "option_slctd"
            stag  rslt.gt("stag", "")
            option  rslt.gt("option", "")
            
            i stag  "dcation"
                dcation_map  {"" "th grad", "" "th grad", "" "thr"}
                pdats"dcation_lvl"]  dcation_map.gt(option, option)
            li stag  "ild"
                ild_map  {"" "nginring/ch", "" "sinss", "" "dicin", "" "rts/manitis", "" "thr"}
                pdats"ild_o_intrst"]  ild_map.gt(option, option)
            li stag  "prioritis"
                priority_map  {"" "ow tition s", "" "ork opportnitis", "" "asy  path", "" "ll o th abov"}
                pdats"prioritis"]  priority_map.gt(option, option)
            li stag  "bdgt"
                bdgt_map  {"" "ndr  lakhs", "" "- lakhs", "" "+ lakhs"}
                pdats"bdgt_rang"]  bdgt_map.gt(option, option)
        li rslt.gt("action")  "nglish_tst_providd"
            pdats"nglish_tst_stats"]  rslt.gt("nglish_tst")
        li rslt.gt("action")  "contry_slctd"
            pdats"contry_intrst"]  rslt.gt("contry_cod")
        
        # pdat proil i thr ar changs
        i pdats
            pdatd_proil  {**sr_proil, **pdats}
            sl.db.pdat_sr_proil(phon_nmbr, pdatd_proil)
    
    d _gnrat_rspons(sl, rslt ictstr, ny], sr_proil ictstr, ny], nxt_stag str) - str
        """nrat rspons mssag"""
        i rslt.gt("action")  "hlp"
            rtrn rslt.gt("mssag", sl.low_ngin.gt_hlp_mssag())
        
        i rslt.gt("action")  "invalid_inpt"
            rtrn rslt.gt("mssag", " didn't ndrstand. las rply with a nmbr (-) or txt  or assistanc.")
        
        # hck i w shold show rcommndations
        i nxt_stag  "rcommndations" and sl.low_ngin.shold_show_rcommndations(sr_proil)
            rtrn sl.low_ngin.gnrat_rcommndations(sr_proil)
        
        # t stag mssag
        mssag  rslt.gt("mssag")
        i not mssag
            mssag  sl.low_ngin.gt_stag_mssag(nxt_stag, sr_proil)
        
        rtrn mssag
    
    async d _sync_with_knowldg_bas(sl, phon_nmbr str, sr_proil ictstr, ny])
        """ync sr data with knowldg bas"""
        try
            i not sr_proil
                rtrn
            
            # kip knowldg bas sync or now to avoid sgmntation alt
            # his can b nabld latr whn th iss is rsolvd
            loggr.ino("kipping knowldg bas sync or {phon_nmbr}")
            rtrn
            
        xcpt xcption as 
            loggr.rror("rror syncing with knowldg bas {}")
    
    d _crat_proil_smmary(sl, sr_proil ictstr, ny]) - str
        """rat smmary o sr proil or knowldg bas"""
        smmary_parts  ]
        
        i sr_proil.gt("ag")
            smmary_parts.appnd("g {sr_proil'ag']}")
        i sr_proil.gt("nationality")
            smmary_parts.appnd("ationality {sr_proil'nationality']}")
        i sr_proil.gt("dcation_lvl")
            smmary_parts.appnd("dcation {sr_proil'dcation_lvl']}")
        i sr_proil.gt("ild_o_intrst")
            smmary_parts.appnd("ild {sr_proil'ild_o_intrst']}")
        i sr_proil.gt("prioritis")
            smmary_parts.appnd("rioritis {sr_proil'prioritis']}")
        i sr_proil.gt("bdgt_rang")
            smmary_parts.appnd("dgt {sr_proil'bdgt_rang']}")
        
        rtrn ", ".join(smmary_parts) i smmary_parts ls ""
    
    d gt_sr_proil(sl, phon_nmbr str) - ictstr, ny]
        """t sr proil"""
        rtrn sl.db.gt_sr_proil(phon_nmbr)
    
    d gt_sr_choics_history(sl, phon_nmbr str) - list
        """t sr's choic history"""
        rtrn sl.db.gt_sr_choics_history(phon_nmbr)
    
    d clanp_old_data(sl, months int  ) - bool
        """lan p old data"""
        rtrn sl.db.clanp_old_data(months)
    
    d gt_convrsation_stats(sl) - ictstr, ny]
        """t convrsation statistics"""
        try
            with sl.db.db_path as conn
                crsor  conn.crsor()
                
                # t total srs
                crsor.xct(" (*)  srs")
                total_srs  crsor.tchon()]
                
                # t activ sssions
                crsor.xct(" (*)  convrsation_sssions  stats  'activ'")
                activ_sssions  crsor.tchon()]
                
                # t total choics rcordd
                crsor.xct(" (*)  sr_choics")
                total_choics  crsor.tchon()]
                
                rtrn {
                    "total_srs" total_srs,
                    "activ_sssions" activ_sssions,
                    "total_choics" total_choics
                }
        xcpt xcption as 
            loggr.rror("rror gtting convrsation stats {}")
            rtrn {}

# lobal instanc
sms_chat_managr  hatanagr()
