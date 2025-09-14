"""
st ll sr intraction low
"""

import asyncio
rom cor.latopia_chat_managr import latopia_chat_managr

async d tst_ll_intraction()
    """st th complt sr intraction low"""
    
    print("🧪 sting ll sr ntraction low")
    print("" * )
    
    # imlat th sr's xprinc
    tst_inpts  
        "hi！my nam is yogri",
        "'m  yars old",
        "'m rom ndia",
        " want to stdy abroad"
    ]
    
    or i, tst_inpt in nmrat(tst_inpts, )
        print("n📱 tp {i} sr says '{tst_inpt}'")
        
        try
            # rocss th inpt
            rspons  await latopia_chat_managr.chat(tst_inpt)
            
            print("🤖 ot rsponds {rspons'answr']}")
            print("📊 sr proil {latopia_chat_managr.sr_proil}")
            print("📋 ollctd ino {latopia_chat_managr.collctd_ino}")
            print("🔄 onvrsation stag {latopia_chat_managr.convrsation_stag}")
            
        xcpt xcption as 
            print("❌ rror {}")
        
        print("-" * )

i __nam__  "__main__"
    asyncio.rn(tst_ll_intraction())
