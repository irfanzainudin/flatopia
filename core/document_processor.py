"""
asd on anghain的文档rocssing器
"""
import os
rom typing import ist, ict, ny, ptional
rom pathlib import ath
rom langchain_commnity.docmnt_loadrs import (
    xtoadr, 
    yoadr, 
    ocxtxtoadr,
    basoadr,
    irctoryoadr
)
rom langchain.txt_splittr import crsivharactrxtplittr
rom langchain.schma import ocmnt
rom .langchain_conig import langchain_conig


class ocmntrocssor
    """文档rocssing器"""
    
    d __init__(sl)
        sl.txt_splittr  langchain_conig.txt_splittr
        sl.spportd_ormats  {
            '.txt' xtoadr,
            '.pd' yoadr,
            '.docx' ocxtxtoadr,
            '.html' basoadr,
            '.htm' basoadr
        }
    
    d load_docmnt(sl, il_path str) - istocmnt]
        """oading单个文档"""
        try
            il_path  ath(il_path)
            il_xtnsion  il_path.six.lowr()
            
            i il_xtnsion not in sl.spportd_ormats
                rais alrror("不支持的il格式 {il_xtnsion}")
            
            loadr_class  sl.spportd_ormatsil_xtnsion]
            
            i il_xtnsion in '.html', '.htm']
                loadr  loadr_class(str(il_path)])
            ls
                loadr  loadr_class(str(il_path))
            
            docmnts  loadr.load()
            rtrn docmnts
            
        xcpt xcption as 
            print("oading文档aild {il_path} {}")
            rtrn ]
    
    d load_dirctory(sl, dirctory_path str, glob_pattrn str  "**/*") - istocmnt]
        """oading目录中的所有文档"""
        try
            loadr  irctoryoadr(
                dirctory_path,
                globglob_pattrn,
                loadr_clssl._gt_loadr_or_glob,
                show_progrssr
            )
            docmnts  loadr.load()
            rtrn docmnts
            
        xcpt xcption as 
            print("oading目录aild {dirctory_path} {}")
            rtrn ]
    
    d _gt_loadr_or_glob(sl, il_path str)
        """根据il扩展名获取对应的oading器"""
        il_xtnsion  ath(il_path).six.lowr()
        
        i il_xtnsion in sl.spportd_ormats
            rtrn sl.spportd_ormatsil_xtnsion]
        ls
            rtrn xtoadr  # 默认s文本oading器
    
    d load_wb_contnt(sl, rls iststr]) - istocmnt]
        """oading网页内容"""
        try
            loadr  basoadr(rls)
            docmnts  loadr.load()
            rtrn docmnts
            
        xcpt xcption as 
            print("oading网页内容aild {}")
            rtrn ]
    
    d split_docmnts(sl, docmnts istocmnt]) - istocmnt]
        """分割文档"""
        try
            split_docs  sl.txt_splittr.split_docmnts(docmnts)
            rtrn split_docs
            
        xcpt xcption as 
            print("分割文档aild {}")
            rtrn docmnts
    
    d procss_docmnts(sl, 
                         docmnts istocmnt], 
                         add_mtadata bool  r) - istocmnt]
        """rocssing文档（添加元数据、清理等）"""
        procssd_docs  ]
        
        or i, doc in nmrat(docmnts)
            try
                # 清理文档内容
                cland_contnt  sl._clan_docmnt_contnt(doc.pag_contnt)
                
                # 创建新文档
                procssd_doc  ocmnt(
                    pag_contntcland_contnt,
                    mtadatadoc.mtadata.copy() i doc.mtadata ls {}
                )
                
                # 添加rocssing元数据
                i add_mtadata
                    procssd_doc.mtadata.pdat({
                        "procssd" r,
                        "docmnt_id" i,
                        "contnt_lngth" ln(cland_contnt),
                        "word_cont" ln(cland_contnt.split())
                    })
                
                procssd_docs.appnd(procssd_doc)
                
            xcpt xcption as 
                print("rocssing文档aild {}")
                procssd_docs.appnd(doc)
        
        rtrn procssd_docs
    
    d _clan_docmnt_contnt(sl, contnt str) - str
        """清理文档内容"""
        # 移除多余的空白字符
        contnt  ' '.join(contnt.split())
        
        # 移除特殊字符（保留中文、英文、数字和基本标点）
        import r
        contnt  r.sb(r'^ws-.,!()（）【】""''""''，。！？；：]', '', contnt)
        
        rtrn contnt.strip()
    
    d crat_docmnt_rom_txt(sl, 
                                 txt str, 
                                 mtadata ptionalictstr, ny]]  on) - ocmnt
        """从文本创建文档"""
        mtadata  mtadata or {}
        mtadata.pdat({
            "sorc" "manal_inpt",
            "typ" "txt"
        })
        
        rtrn ocmnt(
            pag_contnttxt,
            mtadatamtadata
        )
    
    d batch_procss(sl, 
                     il_paths iststr], 
                     add_to_vctorstor bool  r) - ictstr, ny]
        """批量rocssing文档"""
        rslts  {
            "total_ils" ln(il_paths),
            "sccssl_ils" ,
            "aild_ils" ,
            "total_docmnts" ,
            "procssd_docmnts" ,
            "rrors" ]
        }
        
        all_docmnts  ]
        
        or il_path in il_paths
            try
                # oading文档
                docmnts  sl.load_docmnt(il_path)
                
                i docmnts
                    # 分割文档
                    split_docs  sl.split_docmnts(docmnts)
                    
                    # rocssing文档
                    procssd_docs  sl.procss_docmnts(split_docs)
                    
                    all_docmnts.xtnd(procssd_docs)
                    rslts"sccssl_ils"] + 
                    rslts"total_docmnts"] + ln(docmnts)
                    rslts"procssd_docmnts"] + ln(procssd_docs)
                ls
                    rslts"aild_ils"] + 
                    rslts"rrors"].appnd("无法oadingil {il_path}")
                    
            xcpt xcption as 
                rslts"aild_ils"] + 
                rslts"rrors"].appnd("rocssingilaild {il_path} {str()}")
        
        # 添加到ctor storag
        i add_to_vctorstor and all_docmnts
            try
                sccss  langchain_conig.add_docmnts(all_docmnts)
                i not sccss
                    rslts"rrors"].appnd("添加到ctor storagaild")
            xcpt xcption as 
                rslts"rrors"].appnd("添加到ctor storagaild {str()}")
        
        rtrn rslts
    
    d gt_docmnt_ino(sl, docmnts istocmnt]) - ictstr, ny]
        """获取文档信息统计"""
        i not docmnts
            rtrn {"total_docmnts" }
        
        total_chars  sm(ln(doc.pag_contnt) or doc in docmnts)
        total_words  sm(ln(doc.pag_contnt.split()) or doc in docmnts)
        
        # 统计元数据
        mtadata_stats  {}
        or doc in docmnts
            or ky, val in doc.mtadata.itms()
                i ky not in mtadata_stats
                    mtadata_statsky]  ]
                mtadata_statsky].appnd(val)
        
        rtrn {
            "total_docmnts" ln(docmnts),
            "total_charactrs" total_chars,
            "total_words" total_words,
            "avrag_chars_pr_doc" total_chars / ln(docmnts),
            "avrag_words_pr_doc" total_words / ln(docmnts),
            "mtadata_ilds" list(mtadata_stats.kys()),
            "mtadata_stats" mtadata_stats
        }


# 全局文档rocssing器实例
docmnt_procssor  ocmntrocssor()
