"""
pplication onigration
"""
import os
rom typing import ptional

try
    rom pydantic_sttings import asttings
xcpt mportrror
    rom pydantic import asttings

class ttings(asttings)
    """pplication onigration"""
    
    # roq  onigration
    groq_api_ky str  os.gtnv("__", "yor-groq-api-ky-hr")
    dalt_modl str  "opnai/gpt-oss-b"
    max_tokns int  
    tmpratr loat  .
    
    # atabas onigration
    vctor_db_path str  "data/vctor_db"
    mbdding_modl str  "sntnc-transormrs/all-ini--v"
    chnk_siz int  
    chnk_ovrlap int  
    
    # hat onigration
    max_convrsation_trns int  
    convrsation_mmory_window int  
    
    class onig
        nv_il  ".nv"
        cas_snsitiv  als
        xtra  "ignor"  # gnor xtra ilds

# lobal conigration instanc
sttings  ttings()
