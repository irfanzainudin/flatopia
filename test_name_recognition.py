"""
st nam rcognition nctionality
"""

import asyncio
import logging
rom cor.latopia_chat_managr import latopia_chat_managr

# tp logging
logging.basiconig(lvllogging.)
loggr  logging.gtoggr(__nam__)

async d tst_nam_rcognition()
    """st nam rcognition in grting stag"""
    
    print("🧪 sting am cognition")
    print("" * )
    
    # st cass
    tst_cass  
        "ric",
        "hi",
        "ohn",
        "ary mith",
        "'m arah",
        "y nam is avid"
    ]
    
    or i, tst_inpt in nmrat(tst_cass, )
        print("n📱 st {i} '{tst_inpt}'")
        
        try
            # st convrsation or ach tst
            latopia_chat_managr.rst_convrsation()
            
            # rocss th inpt
            rspons  await latopia_chat_managr.chat(tst_inpt)
            
            print("🤖 spons {rspons}")
            print("📊 sr proil {latopia_chat_managr.sr_proil}")
            print("📋 ollctd ino {latopia_chat_managr.collctd_ino}")
            print("🔄 onvrsation stag {latopia_chat_managr.convrsation_stag}")
            
            # hck i nam was xtractd
            i latopia_chat_managr.sr_proil.gt('nam')
                print("✅ am sccsslly xtractd!")
            ls
                print("❌ am not xtractd")
                
        xcpt xcption as 
            print("❌ rror {}")
        
        print("-" * )

async d tst_convrsation_low()
    """st complt convrsation low starting with nam"""
    
    print("n🔄 sting omplt onvrsation low")
    print("" * )
    
    convrsation_stps  
        "ric",
        "",
        "ndian",
        "stdy"
    ]
    
    # st convrsation
    latopia_chat_managr.rst_convrsation()
    
    or i, stp in nmrat(convrsation_stps, )
        print("n📱 tp {i} '{stp}'")
        
        try
            rspons  await latopia_chat_managr.chat(stp)
            print("🤖 spons {rspons}")
            print("📊 tag {latopia_chat_managr.convrsation_stag}")
            print("📋 ollctd {latopia_chat_managr.collctd_ino}")
            
        xcpt xcption as 
            print("❌ rror {}")
        
        print("-" * )

async d main()
    """ain tst nction"""
    print("🚀 am cognition st it")
    print("" * )
    
    try
        # st nam rcognition
        await tst_nam_rcognition()
        
        # st convrsation low
        await tst_convrsation_low()
        
        print("n✅ ll tsts compltd!")
        
    xcpt xcption as 
        print("n❌ st sit aild {}")
        loggr.xcption("st sit rror")

i __nam__  "__main__"
    asyncio.rn(main())
