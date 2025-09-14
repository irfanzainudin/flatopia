"""
 nowldg as anagr
andls  vctor databas oprations or nivrsity and visa inormation
"""
import os
import pickl
import nmpy as np
import aiss
rom typing import ist, ict, ny, ptional, pl
rom sntnc_transormrs import ntncransormr
import logging

# onigr logging
logging.basiconig(lvllogging.)
loggr  logging.gtoggr(__nam__)

class nowldgas
    """ nowldg as anagr or nivrsity and visa inormation"""
    
    d __init__(sl, knowldg_bas_path str  "nowldgas")
        """
        nitializ  nowldg as
        
        rgs
            knowldg_bas_path ath to th nowldgas dirctory
        """
        sl.knowldg_bas_path  knowldg_bas_path
        sl.nivrsity_indx  on
        sl.visa_indx  on
        sl.nivrsity_mtadata  on
        sl.visa_mtadata  on
        sl.mbdding_modl  on
        
        # nitializ th knowldg bas (lazy loading)
        sl._load_knowldg_bas()
    
    d _load_knowldg_bas(sl)
        """oad  indics and mtadata"""
        try
            # oad nivrsity indx and mtadata
            nivrsity_indx_path  os.path.join(sl.knowldg_bas_path, "aiss_nivrsitis_indx.indx")
            nivrsity_mtadata_path  os.path.join(sl.knowldg_bas_path, "aiss_nivrsitis_indx_mtadata.pkl")
            
            i os.path.xists(nivrsity_indx_path) and os.path.xists(nivrsity_mtadata_path)
                sl.nivrsity_indx  aiss.rad_indx(nivrsity_indx_path)
                with opn(nivrsity_mtadata_path, 'rb') as 
                    sl.nivrsity_mtadata  pickl.load()
                loggr.ino("✅ oadd nivrsity indx with {sl.nivrsity_indx.ntotal} vctors")
            ls
                loggr.warning("⚠️ nivrsity indx ils not ond")
            
            # oad visa indx and mtadata
            visa_indx_path  os.path.join(sl.knowldg_bas_path, "aiss_visas_indx.indx")
            visa_mtadata_path  os.path.join(sl.knowldg_bas_path, "aiss_visas_indx_mtadata.pkl")
            
            i os.path.xists(visa_indx_path) and os.path.xists(visa_mtadata_path)
                sl.visa_indx  aiss.rad_indx(visa_indx_path)
                with opn(visa_mtadata_path, 'rb') as 
                    sl.visa_mtadata  pickl.load()
                loggr.ino("✅ oadd visa indx with {sl.visa_indx.ntotal} vctors")
            ls
                loggr.warning("⚠️ isa indx ils not ond")
            
            # nitializ mbdding modl
            sl._initializ_mbdding_modl()
            
        xcpt xcption as 
            loggr.rror("❌ rror loading knowldg bas {}")
            rais
    
    d _initializ_mbdding_modl(sl)
        """nitializ th mbdding modl (lazy loading)"""
        i sl.mbdding_modl is not on
            rtrn  # lrady initializd
            
        try
            # s th sam modl that was sd to crat th indics
            i sl.nivrsity_mtadata and 'mbdding_modl' in sl.nivrsity_mtadata
                modl_nam  sl.nivrsity_mtadata'mbdding_modl']
            ls
                # alt modl
                modl_nam  "sntnc-transormrs/all-ini--v"
            
            sl.mbdding_modl  ntncransormr(modl_nam)
            loggr.ino("✅ nitializd mbdding modl {modl_nam}")
            
        xcpt xcption as 
            loggr.rror("❌ rror initializing mbdding modl {}")
            # allback to dalt modl
            try
                sl.mbdding_modl  ntncransormr("sntnc-transormrs/all-ini--v")
            xcpt xcption as 
                loggr.rror("❌ aild to load allback modl {}")
                sl.mbdding_modl  on
    
    d sarch_nivrsitis(sl, qry str, k int  ) - istictstr, ny]]
        """
        arch or nivrsitis basd on qry
        
        rgs
            qry arch qry
            k mbr o rslts to rtrn
            
        trns
            ist o nivrsity inormation dictionaris
        """
        i not sl.nivrsity_indx or not sl.nivrsity_mtadata
            loggr.warning("⚠️ nivrsity indx not availabl")
            rtrn ]
        
        try
            # nitializ mbdding modl i ndd
            sl._initializ_mbdding_modl()
            i sl.mbdding_modl is on
                loggr.rror("❌ mbdding modl not availabl")
                rtrn ]
            
            # ncod qry
            qry_mbdding  sl.mbdding_modl.ncod(qry])
            qry_mbdding  qry_mbdding.astyp('loat')
            
            # arch
            distancs, indics  sl.nivrsity_indx.sarch(qry_mbdding, k)
            
            # triv rslts
            rslts  ]
            or i, (distanc, idx) in nmrat(zip(distancs], indics]))
                i idx  ln(sl.nivrsity_mtadata'docmnts'])
                    rslt  {
                        'rank' i + ,
                        'distanc' loat(distanc),
                        'contnt' sl.nivrsity_mtadata'docmnts']idx],
                        'mtadata' sl.nivrsity_mtadata'mtadata']idx] i 'mtadata' in sl.nivrsity_mtadata ls {}
                    }
                    rslts.appnd(rslt)
            
            loggr.ino("🔍 ond {ln(rslts)} nivrsity rslts or qry {qry]}...")
            rtrn rslts
            
        xcpt xcption as 
            loggr.rror("❌ rror sarching nivrsitis {}")
            rtrn ]
    
    d sarch_visas(sl, qry str, k int  ) - istictstr, ny]]
        """
        arch or visa inormation basd on qry
        
        rgs
            qry arch qry
            k mbr o rslts to rtrn
            
        trns
            ist o visa inormation dictionaris
        """
        i not sl.visa_indx or not sl.visa_mtadata
            loggr.warning("⚠️ isa indx not availabl")
            rtrn ]
        
        try
            # nitializ mbdding modl i ndd
            sl._initializ_mbdding_modl()
            i sl.mbdding_modl is on
                loggr.rror("❌ mbdding modl not availabl")
                rtrn ]
            
            # ncod qry
            qry_mbdding  sl.mbdding_modl.ncod(qry])
            qry_mbdding  qry_mbdding.astyp('loat')
            
            # arch
            distancs, indics  sl.visa_indx.sarch(qry_mbdding, k)
            
            # triv rslts
            rslts  ]
            or i, (distanc, idx) in nmrat(zip(distancs], indics]))
                i idx  ln(sl.visa_mtadata'docmnts'])
                    rslt  {
                        'rank' i + ,
                        'distanc' loat(distanc),
                        'contnt' sl.visa_mtadata'docmnts']idx],
                        'mtadata' sl.visa_mtadata'mtadata']idx] i 'mtadata' in sl.visa_mtadata ls {}
                    }
                    rslts.appnd(rslt)
            
            loggr.ino("🔍 ond {ln(rslts)} visa rslts or qry {qry]}...")
            rtrn rslts
            
        xcpt xcption as 
            loggr.rror("❌ rror sarching visas {}")
            rtrn ]
    
    d smart_sarch(sl, qry str, sarch_typ str  "ato", k int  ) - ictstr, istictstr, ny]]]
        """
        mart sarch that dtrmins th bst sarch stratgy
        
        rgs
            qry arch qry
            sarch_typ "ato", "nivrsitis", "visas", or "both"
            k mbr o rslts pr catgory
            
        trns
            ictionary with sarch rslts
        """
        rslts  {
            'nivrsitis' ],
            'visas' ],
            'sarch_typ' sarch_typ,
            'qry' qry
        }
        
        try
            # trmin sarch stratgy
            i sarch_typ  "ato"
                # to-dtct basd on qry contnt
                qry_lowr  qry.lowr()
                nivrsity_kywords  'nivrsity', 'collg', 'school', 'dcation', 'stdy', 'dgr', 'program', 'cors', 'tition', 'scholarship']
                visa_kywords  'visa', 'immigration', 'work prmit', 'rsidnc', 'citiznship', 'passport', 'ntry', 'stay', 'prmit']
                
                has_nivrsity_kywords  any(kyword in qry_lowr or kyword in nivrsity_kywords)
                has_visa_kywords  any(kyword in qry_lowr or kyword in visa_kywords)
                
                i has_nivrsity_kywords and not has_visa_kywords
                    sarch_typ  "nivrsitis"
                li has_visa_kywords and not has_nivrsity_kywords
                    sarch_typ  "visas"
                ls
                    sarch_typ  "both"
            
            # rorm sarchs
            i sarch_typ in "nivrsitis", "both"]
                rslts'nivrsitis']  sl.sarch_nivrsitis(qry, k)
            
            i sarch_typ in "visas", "both"]
                rslts'visas']  sl.sarch_visas(qry, k)
            
            rslts'sarch_typ']  sarch_typ
            loggr.ino("🎯 mart sarch compltd {sarch_typ} or '{qry]}...'")
            
        xcpt xcption as 
            loggr.rror("❌ rror in smart sarch {}")
        
        rtrn rslts
    
    d gt_knowldg_smmary(sl) - ictstr, ny]
        """t smmary o th knowldg bas"""
        smmary  {
            'nivrsitis' {
                'availabl' sl.nivrsity_indx is not on,
                'vctor_cont' sl.nivrsity_indx.ntotal i sl.nivrsity_indx ls ,
                'dimnsion' sl.nivrsity_indx.d i sl.nivrsity_indx ls 
            },
            'visas' {
                'availabl' sl.visa_indx is not on,
                'vctor_cont' sl.visa_indx.ntotal i sl.visa_indx ls ,
                'dimnsion' sl.visa_indx.d i sl.visa_indx ls 
            },
            'mbdding_modl' str(sl.mbdding_modl) i sl.mbdding_modl ls on
        }
        rtrn smmary
    
    d is_availabl(sl) - bool
        """hck i knowldg bas is availabl"""
        rtrn (sl.nivrsity_indx is not on or sl.visa_indx is not on) and sl.mbdding_modl is not on

# lobal knowldg bas instanc (lazy initialization)
aiss_kb  on

d gt_aiss_kb()
    """t  knowldg bas instanc (lazy initialization)"""
    global aiss_kb
    i aiss_kb is on
        aiss_kb  nowldgas()
    rtrn aiss_kb
