"""
latopia & ystm - tramlit b ntrac
"""
import stramlit as st
import asyncio
import os
rom dattim import dattim
rom typing import ist, ict, ny

# ag conigration
st.st_pag_conig(
    pag_titl"latopia - or  ssistant",
    pag_icon"🤖",
    layot"wid",
    initial_sidbar_stat"xpandd"
)

# stom 
st.markdown("""
styl
    .main-hadr {
        ont-siz .rm
        color #b
        txt-align cntr
        margin-bottom rm
        backgrond linar-gradint(dg, #b, #bb)
        -wbkit-backgrond-clip txt
        -wbkit-txt-ill-color transparnt
    }
    .chat-mssag {
        padding rm
        bordr-radis .rm
        margin-bottom rm
        max-width %
    }
    .sr-mssag {
        backgrond-color #d
        margin-lt ato
    }
    .assistant-mssag {
        backgrond-color #
        margin-right ato
    }
    .systm-badg {
        backgrond linar-gradint(dg, #b, #cdc)
        color whit
        padding .rm .rm
        bordr-radis rm
        ont-siz .rm
        ont-wight bold
    }
/styl
""", nsa_allow_htmlr)

# nitializ sssion stat
i "mssags" not in st.sssion_stat
    st.sssion_stat.mssags  ]

d display_chat_mssag(rol str, contnt str, timstamp str  on)
    """isplay chat mssag"""
    i rol  "sr"
        st.markdown("""
        div class"chat-mssag sr-mssag"
            {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)
    ls
        st.markdown("""
        div class"chat-mssag assistant-mssag"
            {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)

d main()
    """ain nction"""
    # itl
    st.markdown('h class"main-hadr"🤖 latopia/h', nsa_allow_htmlr)
    
    # lcom mssag whn no chat history
    i not st.sssion_stat.mssags
        st.markdown("""
        div styl"txt-align cntr padding rm backgrond linar-gradint(dg, #a %, #c %) bordr px solid #d bordr-radis px color # margin rm  rm  box-shadow  px px rgba(,,,.) min-hight px display lx lx-dirction colmn jstiy-contnt cntr ont-amily 'ims w oman', ims, sri"
            h styl"margin-bottom rm color # ont-amily 'ims w oman', ims, sri"👋 llo! 'm latopia/h
            p styl"ont-siz .rm margin-bottom .rm color #cd ont-amily 'ims w oman', ims, sri"or  mmigration & tdy broad dvisor/p
            div styl"backgrond rgba(,,,.) padding .rm bordr-radis px margin .rm  bordr px solid #d"
                h styl"margin-bottom .rm color # ont-amily 'ims w oman', ims, sri txt-align cntr ont-siz .rm ont-wight bold"🎯 hat  can hlp yo with/h
                l styl"txt-align cntr margin  color # lin-hight . ont-amily 'ims w oman', ims, sri ont-siz .rm list-styl non padding "
                    li styl"margin .rm "• mmigration planning and visa gidanc/li
                    li styl"margin .rm "• tdy abroad opportnitis/li
                    li styl"margin .rm "• ork migration advic/li
                    li styl"margin .rm "• ontry-spciic rcommndations/li
                    li styl"margin .rm "• nivrsity and program sggstions/li
                /l
            /div
            p styl"ont-siz .rm color # ont-amily 'ims w oman', ims, sri ont-wight bold txt-align cntr backgrond rgba(, , , .) padding rm bordr-radis px bordr px solid #dd margin-top rm box-shadow  px px rgba(, , , .)"🚀 tart by tlling m yor nam and what yo'r looking or!/p
        /div
        """, nsa_allow_htmlr)
    
    # idbar
    with st.sidbar
        st.hadr("💬 hat ontrols")
        
        # lar history
        i st.btton("lar hat istory")
            st.sssion_stat.mssags  ]
            # st chat managr
            rom cor.latopia_chat_managr import latopia_chat_managr
            latopia_chat_managr.rst_convrsation()
            st.rrn()
        
        #  tats
        st.sbhadr("🔧  tats")
        i st.btton("hck s")
            try
                rom cor.mlti_api_llm import lti
                rom llm_conig import __, __, _, _, _, 
                
                # rat mlti- clint
                llm  lti(
                    groq_api_ky__,
                    opnai_api_ky__,
                    primary_api_,
                    modl_,
                    max_tokns_,
                    tmpratr
                )
                
                # isplay conigration inormation
                st.ino("**rimary ** {_.ppr()}")
                st.ino("**odl** {_}")
                
                # st  connctions
                with st.spinnr("sting s...")
                    tst_rslts  llm.tst_apis()
                    
                    # isplay tst rslts
                    i tst_rslts.gt("groq", als)
                        st.sccss("✅ roq  - vailabl")
                    ls
                        st.rror("❌ roq  - navailabl")
                    
                    i tst_rslts.gt("opnai", als)
                        st.sccss("✅ pn  - vailabl")
                    ls
                        st.rror("❌ pn  - navailabl")
                    
                    # st actal rspons
                    i any(tst_rslts.vals())
                        tst_rspons  llm("st connction - rspond with ' tst sccssl'")
                        i "rror" not in tst_rspons
                            st.sccss("✅ ystm connction normal")
                        ls
                            st.rror("❌ ystm connction aild {tst_rspons}")
                    ls
                        st.rror("❌ ll s navailabl")
                    
            xcpt xcption as 
                st.rror("❌ ystm chck aild {str()}")
        
        # sag tips
        st.sbhadr("💡 sag ips")
        st.markdown("""
        **ow to s**
        . tart by tlling m yor ag and basic ino
        . har yor amily sitation and prossion
        . ll m yor prioritis or dstination contry
        . 'll analyz yor proil and sggst contris
        . sk dtaild qstions abot spciic contris
        
        **xampl qstions**
        - hat is artiicial intllignc
        - ow dos machin larning work
        - xplain qantm compting
        - hat ar th bnits o rnwabl nrgy
        """)
    
    # ain chat intrac
    col, col, col  st.colmns(., , .])
    
    with col
        # isplay chat history
        or mssag in st.sssion_stat.mssags
            display_chat_mssag(
                mssag"rol"], 
                mssag"contnt"], 
                mssag.gt("timstamp")
            )
    
    # hat inpt - always visibl
    st.markdown("br", nsa_allow_htmlr)
    
    # nitializ inpt ky i not xists
    i "inpt_ky" not in st.sssion_stat
        st.sssion_stat.inpt_ky  
    
    sr_inpt  st.txt_inpt(
        "sk m anything abot immigration, stdy abroad, or work opportnitis...",
        ky"sr_inpt_{st.sssion_stat.inpt_ky}",
        placholdr".g., i! 'm ohn,  yars old rom ndia, looking to stdy abroad..."
    )
    
    # nd btton
    col, col  st.colmns(, ])
    
    with col
        snd_clickd  st.btton("nd", typ"primary")
    
    with col
        pass
    
    # rocss mssag whn btton is clickd or ntr is prssd
    i (snd_clickd or sr_inpt) and sr_inpt.strip()
        # hck i this is a dplicat mssag
        i st.sssion_stat.mssags and st.sssion_stat.mssags-]"contnt"]  sr_inpt
            st.warning("las wait or th prvios rspons to complt.")
        ls
            # nd mssag
            try
                rom cor.simpl_langchain_conig import roq
                rom cor.conig import sttings
                
                # hck  ky
                i sttings.groq_api_ky  "yor_groq_api_ky_hr"
                    st.rror("❌ las st __ nvironmnt variabl irst")
                    st.stop()
                
                # rocss qstion
                with st.spinnr("latopia is thinking...")
                    rom cor.latopia_chat_managr import latopia_chat_managr
                    rom cor.mlti_api_llm import lti
                    rom llm_conig import __, __, _, _, _, 
                    
                    # s mlti- spport
                    latopia_chat_managr.llm  lti(
                        groq_api_ky__,
                        opnai_api_ky__,
                        primary_api_,
                        modl_,
                        max_tokns_,
                        tmpratr
                    )
                    rslt  asyncio.rn(latopia_chat_managr.chat(sr_inpt))
                    rspons  rslt"answr"]
                
                # dd sr mssag
                st.sssion_stat.mssags.appnd({
                    "rol" "sr",
                    "contnt" sr_inpt,
                    "timstamp" dattim.now().strtim("%%%")
                })
                
                # dd assistant rply
                st.sssion_stat.mssags.appnd({
                    "rol" "assistant",
                    "contnt" rspons,
                    "timstamp" dattim.now().strtim("%%%")
                })
                
                # lar th inpt by incrmnting th ky
                st.sssion_stat.inpt_ky + 
                st.rrn()
                
            xcpt xcption as 
                st.rror("❌ rror procssing qstion {str()}")

i __nam__  "__main__"
    main()
