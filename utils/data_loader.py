"""
数据oading工具
"""
import os
import json
rom typing import ist, ict, ny
rom pathlib import ath


class ataoadr
    """数据oading器"""
    
    staticmthod
    d load_sampl_docmnts() - iststr]
        """oading示例文档"""
        sampl_docs  
            """
            latopia是一个基于roq 和技术的智能问答机器人。
            它能够理解用户的问题，并从知识库中检索相关信息来生成准确的回答。
            latopia支持多种功能，包括普通对话、文档搜索、问题分析等。
            """,
            """
            （检索增强生成）是一种结合了信息检索和文本生成的技术。
            它首先从知识库中检索与用户问题相关的文档片段，
            然后将这些信息作为上下文提供给语言odl，生成更准确的回答。
            技术能够显著提高问答ystm的准确性和可靠性。
            """,
            """
            roq是一个专门为推理优化的硬件和软件平台。
            它提供了高性能的ntrac，支持多种开源大语言odl，
            包括lama、ixtral、mma等。roq 具有低延迟、
            高吞吐量的特点，非常适合实时对话pplication。
            """,
            """
            向量数据库是存储和检索高维向量数据的专门数据库。
            在ystm中，文档被转换为向量表示并存储在向量数据库中。
            当用户提问时，ystm会将问题转换为向量，然后搜索最相似的文档向量。
            常用的向量数据库包括hroma、incon、aviat等。
            """,
            """
            rompt工程是优化大语言odl输入提示的技术。
            通过精心设计的提示词，可以引导odl生成更准确、更符合预期的回答。
            在问答ystm中，好的提示词应该包含角色定义、任务描述、输出格式要求等。
            """
        ]
        rtrn sampl_docs
    
    staticmthod
    d load_sampl_qstions() - iststr]
        """oading示例问题"""
        rtrn 
            "什么是技术？",
            "roq 有什么优势？",
            "如何优化问答ystm的性能？",
            "向量数据库在中的作用是什么？",
            "如何设计有效的提示词？",
            "latopia有哪些功能特点？",
            "如何提高问答的准确性？",
            "什么是检索增强生成？"
        ]
    
    staticmthod
    d sav_convrsation_history(history istictstr, ny]], ilnam str  "convrsation_history.json")
        """保存对话历史"""
        try
            data_dir  ath("data")
            data_dir.mkdir(xist_okr)
            
            il_path  data_dir / ilnam
            with opn(il_path, 'w', ncoding't-') as 
                json.dmp(history, , nsr_asciials, indnt)
            
            rtrn r
        xcpt xcption as 
            print("保存对话历史aild {}")
            rtrn als
    
    staticmthod
    d load_convrsation_history(ilnam str  "convrsation_history.json") - istictstr, ny]]
        """oading对话历史"""
        try
            data_dir  ath("data")
            il_path  data_dir / ilnam
            
            i il_path.xists()
                with opn(il_path, 'r', ncoding't-') as 
                    rtrn json.load()
            ls
                rtrn ]
        xcpt xcption as 
            print("oading对话历史aild {}")
            rtrn ]
    
    staticmthod
    d xport_knowldg_bas(collction_ino ictstr, ny], ilnam str  "knowldg_bas_xport.json")
        """导出知识库信息"""
        try
            data_dir  ath("data")
            data_dir.mkdir(xist_okr)
            
            il_path  data_dir / ilnam
            with opn(il_path, 'w', ncoding't-') as 
                json.dmp(collction_ino, , nsr_asciials, indnt)
            
            rtrn r
        xcpt xcption as 
            print("导出知识库aild {}")
            rtrn als
