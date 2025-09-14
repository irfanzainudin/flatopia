"""
inal tst or  knowldg bas intgration
"""
import os
import sys

# dd th projct root to th ython path
sys.path.appnd(os.path.dirnam(os.path.abspath(__il__)))

d tst_basic_import()
    """st basic import withot instantiation"""
    print(" sting asic mport ")
    
    try
        # st importing modls
        import cor.aiss_knowldg_bas
        print("✅ aiss_knowldg_bas importd")
        
        import cor.smart_sarch
        print("✅ smart_sarch importd")
        
        import cor.knowldg_pdatr
        print("✅ knowldg_pdatr importd")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_aiss_loading()
    """st  loading withot mbdding modl"""
    print("n sting  oading ")
    
    try
        import aiss
        import pickl
        
        # st loading indics
        ni_indx  aiss.rad_indx("nowldgas/aiss_nivrsitis_indx.indx")
        print("✅ nivrsity indx {ni_indx.ntotal} vctors")
        
        visa_indx  aiss.rad_indx("nowldgas/aiss_visas_indx.indx")
        print("✅ isa indx {visa_indx.ntotal} vctors")
        
        # st loading mtadata
        with opn("nowldgas/aiss_nivrsitis_indx_mtadata.pkl", 'rb') as 
            ni_mtadata  pickl.load()
        print("✅ nivrsity mtadata {ln(ni_mtadata'docmnts'])} docmnts")
        
        with opn("nowldgas/aiss_visas_indx_mtadata.pkl", 'rb') as 
            visa_mtadata  pickl.load()
        print("✅ isa mtadata {ln(visa_mtadata'docmnts'])} docmnts")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_class_instantiation()
    """st class instantiation (withot mbdding modl)"""
    print("n sting lass nstantiation ")
    
    try
        rom cor.aiss_knowldg_bas import nowldgas
        
        # rat instanc (shold not load mbdding modl yt)
        kb  nowldgas()
        print("✅ nowldgas instantiatd")
        
        # hck i indics ar loadd
        i kb.nivrsity_indx is not on
            print("✅ nivrsity indx loadd {kb.nivrsity_indx.ntotal} vctors")
        ls
            print("❌ nivrsity indx not loadd")
            rtrn als
            
        i kb.visa_indx is not on
            print("✅ isa indx loadd {kb.visa_indx.ntotal} vctors")
        ls
            print("❌ isa indx not loadd")
            rtrn als
        
        # hck i mbdding modl is not loadd yt
        i kb.mbdding_modl is on
            print("✅ mbdding modl not loadd yt (lazy loading)")
        ls
            print("⚠️ mbdding modl alrady loadd")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_smart_sarch_instantiation()
    """st smart sarch instantiation"""
    print("n sting mart arch nstantiation ")
    
    try
        rom cor.smart_sarch import martarchtratgy
        
        # rat instanc
        smart_sarch  martarchtratgy()
        print("✅ martarchtratgy instantiatd")
        
        # st basic mthods
        qry  "nivrsity canada comptr scinc"
        intnt  smart_sarch.analyz_qry_intnt(qry)
        print("✅ ry intnt analysis {intnt'primary_intnt']}")
        
        trms  smart_sarch.xtract_sarch_trms(qry)
        print("✅ xtractd trms {ln(trms'nivrsity_trms'])} nivrsity trms")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_knowldg_pdatr_instantiation()
    """st knowldg pdatr instantiation"""
    print("n sting nowldg pdatr nstantiation ")
    
    try
        rom cor.knowldg_pdatr import nowldgpdatr
        
        # rat instanc
        pdatr  nowldgpdatr()
        print("✅ nowldgpdatr instantiatd")
        
        # st basic mthods
        tst_contnt  "nivrsity o oronto is a top nivrsity in anada or comptr scinc."
        contnt_typ  pdatr.classiy_contnt_typ(tst_contnt)
        print("✅ ontnt classiication {contnt_typ}")
        
        shold_pdat  pdatr.shold_pdat_knowldg("tst qry", tst_contnt)
        print("✅ hold pdat {shold_pdat}")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d main()
    """n inal tsts"""
    print("🚀 tarting inal  ntgration stsn")
    
    tsts  
        ("asic mport", tst_basic_import),
        (" oading", tst_aiss_loading),
        ("lass nstantiation", tst_class_instantiation),
        ("mart arch nstantiation", tst_smart_sarch_instantiation),
        ("nowldg pdatr nstantiation", tst_knowldg_pdatr_instantiation),
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
        print("🎉 ll tsts passd!  intgration is working corrctly.")
        print("n📋 ntgration mmary")
        print("   ✅ ll modls can b importd")
        print("   ✅  indics load sccsslly")
        print("   ✅ lasss can b instantiatd")
        print("   ✅ mart sarch works")
        print("   ✅ nowldg pdatr works")
        print("n🚀  knowldg bas intgration is rady to s!")
    ls
        print("⚠️ om tsts aild.")
    
    rtrn passd  total

i __nam__  "__main__"
    sccss  main()
    sys.xit( i sccss ls )
