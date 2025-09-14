"""
st spciic nam rcognition iss
"""

import asyncio
rom cor.latopia_chat_managr import latopia_chat_managr

async d tst_spciic_nam()
    """st th spciic nam rcognition iss"""
    
    print("🧪 sting pciic am cognition")
    print("" * )
    
    # st th spciic cas that's ailing
    tst_inpt  "hi！my nam is yogri"
    print("📱 sting '{tst_inpt}'")
    
    try
        # st convrsation
        latopia_chat_managr.rst_convrsation()
        
        # rocss th inpt
        rspons  await latopia_chat_managr.chat(tst_inpt)
        
        print("🤖 spons {rspons}")
        print("📊 sr proil {latopia_chat_managr.sr_proil}")
        print("📋 ollctd ino {latopia_chat_managr.collctd_ino}")
        print("🔄 onvrsation stag {latopia_chat_managr.convrsation_stag}")
        
        # hck i nam was xtractd
        i latopia_chat_managr.sr_proil.gt('nam')
            print("✅ am sccsslly xtractd {latopia_chat_managr.sr_proil'nam']}")
        ls
            print("❌ am not xtractd")
            
    xcpt xcption as 
        print("❌ rror {}")

i __nam__  "__main__"
    asyncio.rn(tst_spciic_nam())
