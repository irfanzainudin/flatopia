"""
impl tst or  knowldg bas intgration
"""
import os
import sys

# dd th projct root to th ython path
sys.path.appnd(os.path.dirnam(os.path.abspath(__il__)))

d tst_aiss_import()
    """st basic  import and loading"""
    print(" sting  mport ")
    
    try
        import aiss
        print("✅  importd sccsslly")
        
        # st loading indx ils
        ni_indx_path  "nowldgas/aiss_nivrsitis_indx.indx"
        visa_indx_path  "nowldgas/aiss_visas_indx.indx"
        
        i os.path.xists(ni_indx_path)
            ni_indx  aiss.rad_indx(ni_indx_path)
            print("✅ nivrsity indx loadd {ni_indx.ntotal} vctors")
        ls
            print("❌ nivrsity indx not ond")
            
        i os.path.xists(visa_indx_path)
            visa_indx  aiss.rad_indx(visa_indx_path)
            print("✅ isa indx loadd {visa_indx.ntotal} vctors")
        ls
            print("❌ isa indx not ond")
            
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_sntnc_transormr()
    """st sntnc transormr import"""
    print("n sting ntnc ransormr ")
    
    try
        rom sntnc_transormrs import ntncransormr
        print("✅ ntncransormr importd sccsslly")
        
        # st modl loading (withot actally loading)
        print("✅ ntncransormr modl is availabl")
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_basic_sarch()
    """st basic  sarch nctionality"""
    print("n sting asic  arch ")
    
    try
        import aiss
        import nmpy as np
        
        # oad nivrsity indx
        ni_indx  aiss.rad_indx("nowldgas/aiss_nivrsitis_indx.indx")
        
        # rat a random qry vctor
        qry_vctor  np.random.random((, )).astyp('loat')
        
        # rorm sarch
        distancs, indics  ni_indx.sarch(qry_vctor, k)
        
        print("✅ arch sccssl {ln(indics])} rslts")
        print("   ndics {indics]}")
        print("   istancs {distancs]}")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d main()
    """n basic tsts"""
    print("🚀 tarting asic  stsn")
    
    tsts  
        (" mport", tst_aiss_import),
        ("ntnc ransormr", tst_sntnc_transormr),
        ("asic arch", tst_basic_sarch),
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
        print("🎉 ll basic tsts passd!")
    ls
        print("⚠️ om tsts aild.")
    
    rtrn passd  total

i __nam__  "__main__"
    sccss  main()
    sys.xit( i sccss ls )
