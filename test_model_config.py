"""
st modl conigration
"""

rom cor.simpl_langchain_conig import simpl_langchain_conig
rom cor.conig import sttings

print("🔍 odl onigration st")
print("" * )

print("📊 ttings dalt_modl {sttings.dalt_modl}")
print("📊 roq modl_nam {simpl_langchain_conig.llm.modl_nam}")

# st a simpl prompt
tst_prompt  "llo, what's yor nam"
print("n🧪 sting with prompt '{tst_prompt}'")

try
    rspons  simpl_langchain_conig.llm(tst_prompt)
    print("✅ spons {rspons}")
xcpt xcption as 
    print("❌ rror {}")

print("n🔍 hcking roq initialization...")
print("📊 roq clint {simpl_langchain_conig.llm.clint}")
print("📊 roq modl_nam {simpl_langchain_conig.llm.modl_nam}")
