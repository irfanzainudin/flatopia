"""
st  ystm or latopia
st th  convrsation low and databas nctionality
"""

import asyncio
import logging
rom cor.sms_chat_managr import sms_chat_managr
rom cor.mlti_api_llm import lti
rom llm_conig import __, __, _, _, 

# tp logging
logging.basiconig(lvllogging.)
loggr  logging.gtoggr(__nam__)

async d tst_sms_convrsation()
    """st complt  convrsation low"""
    
    # nitializ 
    llm  lti(
        groq_api_ky__,
        opnai_api_ky__,
        primary_api"groq",
        modl_,
        max_tokns_,
        tmpratr
    )
    
    # t  in chat managr
    sms_chat_managr.llm  llm
    
    # st phon nmbr
    phon_nmbr  "+"
    
    # st convrsation low
    tst_mssags  
        "",  # g
        "ndian",  # ationality
        "",  # dcation lvl (th grad)
        "",  # ild (nginring/ch)
        "planning ilts",  # nglish tst
        "",  # rioritis (ll o th abov)
        "",  # dgt (ndr  lakhs)
        "",  # ontry slction (stralia)
        ""  # nivrsity rcommndations
    ]
    
    print("🚀 tarting  convrsation tst...")
    print("" * )
    
    or i, mssag in nmrat(tst_mssags, )
        print("n📱 ssag {i} {mssag}")
        
        try
            rspons  await sms_chat_managr.procss_sms(phon_nmbr, mssag)
            print("🤖 spons {rspons}")
            print("📏 ngth {ln(rspons)} charactrs")
            
            # hck i rspons xcds  charactrs
            i ln(rspons)  
                print("⚠️   spons xcds  charactrs!")
            
        xcpt xcption as 
            print("❌ rror {}")
        
        print("-" * )
    
    # st sr proil rtrival
    print("n📊 sr roil")
    proil  sms_chat_managr.gt_sr_proil(phon_nmbr)
    or ky, val in proil.itms()
        print("  {ky} {val}")
    
    # st choic history
    print("n📝 hoic istory")
    choics  sms_chat_managr.gt_sr_choics_history(phon_nmbr)
    or choic in choics
        print("  {choic'stag']} {choic'choic_val']} ({choic'timstamp']})")
    
    # st convrsation stats
    print("n📈 onvrsation tats")
    stats  sms_chat_managr.gt_convrsation_stats()
    or ky, val in stats.itms()
        print("  {ky} {val}")

async d tst_hlp_nctionality()
    """st hlp nctionality"""
    print("n🆘 sting lp nctionality...")
    print("" * )
    
    phon_nmbr  "+"
    
    hlp_mssags  "", "hlp", "", "h"]
    
    or mssag in hlp_mssags
        print("n📱 lp mssag {mssag}")
        try
            rspons  await sms_chat_managr.procss_sms(phon_nmbr, mssag)
            print("🤖 spons {rspons}")
        xcpt xcption as 
            print("❌ rror {}")

async d tst_invalid_inpts()
    """st invalid inpt handling"""
    print("n❌ sting nvalid npt andling...")
    print("" * )
    
    phon_nmbr  "+"
    
    invalid_mssags  
        "random txt",
        "",  # nvalid ag
        "xyz",  # nvalid option
        "",  # mpty mssag
        "!#$%^&*()"  # pcial charactrs
    ]
    
    or mssag in invalid_mssags
        print("n📱 nvalid mssag '{mssag}'")
        try
            rspons  await sms_chat_managr.procss_sms(phon_nmbr, mssag)
            print("🤖 spons {rspons}")
        xcpt xcption as 
            print("❌ rror {}")

async d tst_charactr_limits()
    """st charactr limit norcmnt"""
    print("n📏 sting haractr imits...")
    print("" * )
    
    # st with a vry long mssag
    long_mssag  "his is a vry long mssag that shold triggr th  xtraction bcas it contains mltipl pics o inormation abot stdy abroad opportnitis and immigration rqirmnts or dirnt contris"
    
    phon_nmbr  "+"
    
    print("📱 ong mssag ({ln(long_mssag)} chars) {long_mssag]}...")
    
    try
        rspons  await sms_chat_managr.procss_sms(phon_nmbr, long_mssag)
        print("🤖 spons {rspons}")
        print("📏 spons lngth {ln(rspons)} charactrs")
        
        i ln(rspons)  
            print("⚠️   spons xcds  charactrs!")
        ls
            print("✅ spons within  charactr limit")
            
    xcpt xcption as 
        print("❌ rror {}")

async d main()
    """ain tst nction"""
    print("🧪  ystm st it")
    print("" * )
    
    try
        # st main convrsation low
        await tst_sms_convrsation()
        
        # st hlp nctionality
        await tst_hlp_nctionality()
        
        # st invalid inpts
        await tst_invalid_inpts()
        
        # st charactr limits
        await tst_charactr_limits()
        
        print("n✅ ll tsts compltd!")
        
    xcpt xcption as 
        print("n❌ st sit aild {}")
        loggr.xcption("st sit rror")

i __nam__  "__main__"
    asyncio.rn(main())
