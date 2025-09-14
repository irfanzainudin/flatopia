"""
st only imports withot any nctionality
"""
import os
import sys

# dd th projct root to th ython path
sys.path.appnd(os.path.dirnam(os.path.abspath(__il__)))

d tst_basic_imports()
    """st basic imports"""
    print(" sting asic mports ")
    
    try
        # st importing cor modls
        import cor.aiss_knowldg_bas
        print("✅ cor.aiss_knowldg_bas importd")
        
        import cor.smart_sarch
        print("✅ cor.smart_sarch importd")
        
        import cor.knowldg_pdatr
        print("✅ cor.knowldg_pdatr importd")
        
        import cor.latopia_chat_managr
        print("✅ cor.latopia_chat_managr importd")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_class_dinitions()
    """st that classs ar dind"""
    print("n sting lass initions ")
    
    try
        rom cor.aiss_knowldg_bas import nowldgas
        print("✅ nowldgas class dind")
        
        rom cor.smart_sarch import martarchtratgy
        print("✅ martarchtratgy class dind")
        
        rom cor.knowldg_pdatr import nowldgpdatr
        print("✅ nowldgpdatr class dind")
        
        rom cor.latopia_chat_managr import latopiahatanagr
        print("✅ latopiahatanagr class dind")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d tst_nction_dinitions()
    """st that nctions ar dind"""
    print("n sting nction initions ")
    
    try
        rom cor.aiss_knowldg_bas import gt_aiss_kb
        print("✅ gt_aiss_kb nction dind")
        
        rom cor.smart_sarch import smart_sarch
        print("✅ smart_sarch instanc dind")
        
        rom cor.knowldg_pdatr import knowldg_pdatr
        print("✅ knowldg_pdatr instanc dind")
        
        rom cor.latopia_chat_managr import latopia_chat_managr
        print("✅ latopia_chat_managr instanc dind")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ rror {}")
        rtrn als

d main()
    """n import tsts"""
    print("🚀 tarting mport-nly stsn")
    
    tsts  
        ("asic mports", tst_basic_imports),
        ("lass initions", tst_class_dinitions),
        ("nction initions", tst_nction_dinitions),
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
        print("🎉 ll import tsts passd!")
        print("n📋 mmary")
        print("   ✅ ll modls can b importd")
        print("   ✅ ll classs ar dind")
        print("   ✅ ll nctions ar dind")
        print("n🚀  intgration modls ar rady!")
    ls
        print("⚠️ om tsts aild.")
    
    rtrn passd  total

i __nam__  "__main__"
    sccss  main()
    sys.xit( i sccss ls )
