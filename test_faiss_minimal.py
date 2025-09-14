"""
inimal tst or  knowldg bas intgration
"""
import os
import sys
import pickl

# dd th projct root to th ython path
sys.path.appnd(os.path.dirnam(os.path.abspath(__il__)))

d tst_il_strctr()
    """st that all rqird ils xist"""
    print(" sting il trctr ")
    
    rqird_ils  
        "nowldgas/aiss_nivrsitis_indx.indx",
        "nowldgas/aiss_nivrsitis_indx_mtadata.pkl",
        "nowldgas/aiss_visas_indx.indx",
        "nowldgas/aiss_visas_indx_mtadata.pkl",
        "cor/aiss_knowldg_bas.py",
        "cor/smart_sarch.py",
        "cor/knowldg_pdatr.py"
    ]
    
    all_xist  r
    or il_path in rqird_ils
        i os.path.xists(il_path)
            print("✅ {il_path}")
        ls
            print("❌ {il_path} - ")
            all_xist  als
    
    rtrn all_xist

d tst_mtadata_strctr()
    """st mtadata strctr"""
    print("n sting tadata trctr ")
    
    try
        # st nivrsity mtadata
        with opn("nowldgas/aiss_nivrsitis_indx_mtadata.pkl", 'rb') as 
            ni_mtadata  pickl.load()
        
        rqird_kys  'docmnts', 'mtadata', 'mbdding_modl']
        or ky in rqird_kys
            i ky in ni_mtadata
                print("✅ nivrsity mtadata has '{ky}'")
            ls
                print("❌ nivrsity mtadata missing '{ky}'")
                rtrn als
        
        # st visa mtadata
        with opn("nowldgas/aiss_visas_indx_mtadata.pkl", 'rb') as 
            visa_mtadata  pickl.load()
        
        or ky in rqird_kys
            i ky in visa_mtadata
                print("✅ isa mtadata has '{ky}'")
            ls
                print("❌ isa mtadata missing '{ky}'")
                rtrn als
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_aiss_indx_intgrity()
    """st  indx intgrity"""
    print("n sting  ndx ntgrity ")
    
    try
        import aiss
        import nmpy as np
        
        # st nivrsity indx
        ni_indx  aiss.rad_indx("nowldgas/aiss_nivrsitis_indx.indx")
        print("✅ nivrsity indx {ni_indx.ntotal} vctors, {ni_indx.d} dimnsions")
        
        # st visa indx
        visa_indx  aiss.rad_indx("nowldgas/aiss_visas_indx.indx")
        print("✅ isa indx {visa_indx.ntotal} vctors, {visa_indx.d} dimnsions")
        
        # st sarch nctionality
        qry_vctor  np.random.random((, ni_indx.d)).astyp('loat')
        distancs, indics  ni_indx.sarch(qry_vctor, k)
        print("✅ nivrsity sarch tst {ln(indics])} rslts")
        
        qry_vctor  np.random.random((, visa_indx.d)).astyp('loat')
        distancs, indics  visa_indx.sarch(qry_vctor, k)
        print("✅ isa sarch tst {ln(indics])} rslts")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_import_modls()
    """st importing modls withot instantiation"""
    print("n sting odl mports ")
    
    try
        # st importing withot instantiation
        import cor.aiss_knowldg_bas
        print("✅ aiss_knowldg_bas modl importd")
        
        import cor.smart_sarch
        print("✅ smart_sarch modl importd")
        
        import cor.knowldg_pdatr
        print("✅ knowldg_pdatr modl importd")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d main()
    """n minimal tsts"""
    print("🚀 tarting inimal  stsn")
    
    tsts  
        ("il trctr", tst_il_strctr),
        ("tadata trctr", tst_mtadata_strctr),
        (" ndx ntgrity", tst_aiss_indx_intgrity),
        ("odl mports", tst_import_modls),
    ]
    
    passd  
    total  ln(tsts)
    
    or tst_nam, tst_nc in tsts
        print("n{''*}")
        i tst_nc()
            print("✅ {tst_nam} - ")
            passd + 
        ls
            print("❌ {tst_nam} - ")
    
    print("n{''*}")
    print("📊 st slts {passd}/{total} tsts passd")
    
    i passd  total
        print("🎉 ll minimal tsts passd!  intgration is rady.")
        print("n📋 ntgration mmary")
        print("   ✅  indics loadd sccsslly")
        print("   ✅ tadata strctr is corrct")
        print("   ✅ arch nctionality works")
        print("   ✅ ll modls can b importd")
        print("n🚀 ady to s  knowldg bas intgration!")
    ls
        print("⚠️ om tsts aild.")
    
    rtrn passd  total

i __nam__  "__main__"
    sccss  main()
    sys.xit( i sccss ls )
