# encoding=utf-8
"""
@author : ZhongQing
"""
from feature import Feature ,FeatureType

import logging
import  pandas as pd
import numpy as np

Numerical = 'Numerical'
Categorical = 'Categorical'
Mix = 'Mix'


def init_feature_list():
    logging.info("init_feature_list")


    df = pd.read_csv('colmap.csv',header=0)
    df['table_id'] = df['table_id'].astype(str)

    buf = []





    for row in df.itertuples():
        if row.type == Numerical:
            ft = FeatureType.VAL
        elif row.type == Categorical:
            ft = FeatureType.BIN
        elif row.type == Mix:
            ft = FeatureType.MIX
        else:
            raise NotImplementedError("Check your TYPE")

        f = Feature(name=row.table_id, prefix=row.table_id, startid=1, type=ft)
        buf.append(f)


    return  buf

def fill_feature_dict(fealist , X):
    logging.info('fill feature dict')
    map = {}

    bincols = []
    for f in fealist:
        map[f.prefix] = f
        if f.type == FeatureType.BIN or f.type == FeatureType.MIX:
            bincols.append(f.prefix)

    """
    000330ad1f424114719b7525f400660b "0119=膀胱 0119=充盈 0119=良好 0119=壁 0119=光滑 0119=延续性 0119=好 0119=其内 0119=透声性 0119=良好 0119=未见 0119=明显 0119=占位性 0119=病变 0120=前列腺 0120=稍大 0120=： 0120=46mm 0120=× 0120=40mm 0120=× 0120=30mm 0120=内 0120=回声 0120=尚 0120=均匀 0120=未见明显异常 0120=回声 0124=输尿管 0124=上 0124=段 0124=膀胱 0124=壁间 0124=段 0124=无 0124=扩张 2302=健康 1301=正常 1302=正常 1303=正常 1304=正常 1305=正常 1308=裸眼 1308=视力 1308=右 1308=: 1308=07 1308=裸眼 1308=视力 1308=左 1308=: 1308=07 1313=正常 1314=正常 1315=正常 1316=正常 1319=nan 1320=nan 1321=0.7 1322=0.7 1325=nan 1326=nan 1328=正常 1402=大致正常脑血流图 1102=颈椎骨质未见明显异常 1103=颈椎 1103=正常 1103=生理 1103=曲度 1103=正常 1103=颈椎 1103=体及 1103=附件 1103=未见 1103=明显 1103=骨质 1103=性 1103=改变 1103=椎间隙 1103=均匀 1103=周围 1103=软组织 1103=未见异常 1104=nan 0101=双侧 0101=甲状腺 0101=大小 0101=形态 0101=正常 0101=包膜 0101=光整 0101=实质 0101=回声 0101=均匀 0101=光点 0101=稍 0101=粗 0101=未见明显异常 0101=回声 0101=CDFI 0101=： 0101=血流 0101=显示 0101=未见异常 0102=甲状腺 0102=彩超 0102=含 0102=颈部 0102=淋巴细胞 0102=未发现明显异常 A201=详见纸质报告 0979=无 0980=无 0985=无 0201=正常 0202=正常 0203=正常 0206=正常 0207=正常 0208=正常 0209=正常 0210=正常 0212=无 0215=正常 0216=正常 0217=正常 0222=耳鼻咽喉科检查未见异常 0225=nan 1001=窦性心律肢体导联低电压 0405=未见异常 0406=未见异常 0407=未见异常 0409=病史 0409=: 0409=甲状腺 0409=功能 0409=亢进 0409=治疗 0409=中 0413=未见异常 0420=未见异常 0421=整齐 0423=未见异常 0424=90--100次/分 0425=正常 0426=未见异常 0430=未见异常 0431=未见异常 0432=未见异常 0433=未见异常 0434=甲状腺功能亢进（治疗中） 0435=未见异常 A202=详见纸质报告 0102=前列腺 0102=: 0102=前列腺 0102=稍大 0102=膀胱 0102=双侧 0102=输尿管 0102=未发现明显异常 2406=63.9 2403=71.3 2404=171.0 2405=24.4 0102=肝胆胰 0102=脾 0102=左 0102=肾 0102=右肾 0102=未发现明显异常 0113=肝脏 0113=大小 0113=形态 0113=正常 0113=包膜 0113=光整 0113=肝内 0113=血管 0113=走行 0113=较 0113=清晰 0113=回声 0113=均匀 0114=胆囊 0114=大小 0114=形态 0114=正常 0114=囊壁光 0114=整囊腔 0114=内 0114=透声 0114=好 0114=胆总管 0114=无 0114=扩张 0115=胰腺 0115=大小 0115=形态 0115=正常 0115=边缘 0115=规整 0115=内部 0115=回声 0115=均匀 0115=胰管 0115=未见 0115=扩张 0116=脾脏 0116=大小 0116=形态 0116=正常 0116=包膜 0116=光整 0116=回声 0116=均匀 0117=左 0117=肾
    """
    for row in X.itertuples():
        feature_str = row.X
        us = feature_str.split(" ")

        for unit in us:
            try:
                k, v  = unit.split("=",1)
                if k in bincols:
                    f = map[k]  # type:Feature
                    f.tryAdd(k, unit)  #特征ID编码！！ 0119=膀胱  编码ID是多少?
            except:
                print( 'ERROR=', unit)


    start = 1

    for f in fealist:  # type:Feature
        start = f.alignFeatureID(start)
        logging.info(f.coverRange())

    return start
def transform_feature(fealist, X):
    map = {}

    bincols = []
    for f in fealist:
        map[f.prefix] = f
        if f.type == FeatureType.BIN:
            bincols.append(f.prefix)

    """
        000330ad1f424114719b7525f400660b "0119=膀胱 0119=充盈 0119=良好 0119=壁 0119=光滑 0119=延续性 0119=好 0119=其内 0119=透声性 0119=良好 0119=未见 0119=明显 0119=占位性 0119=病变 0120=前列腺 0120=稍大 0120=： 0120=46mm 0120=× 0120=40mm 0120=× 0120=30mm 0120=内 0120=回声 0120=尚 0120=均匀 0120=未见明显异常 0120=回声 0124=输尿管 0124=上 0124=段 0124=膀胱 0124=壁间 0124=段 0124=无 0124=扩张 2302=健康 1301=正常 1302=正常 1303=正常 1304=正常 1305=正常 1308=裸眼 1308=视力 1308=右 1308=: 1308=07 1308=裸眼 1308=视力 1308=左 1308=: 1308=07 1313=正常 1314=正常 1315=正常 1316=正常 1319=nan 1320=nan 1321=0.7 1322=0.7 1325=nan 1326=nan 1328=正常 1402=大致正常脑血流图 1102=颈椎骨质未见明显异常 1103=颈椎 1103=正常 1103=生理 1103=曲度 1103=正常 1103=颈椎 1103=体及 1103=附件 1103=未见 1103=明显 1103=骨质 1103=性 1103=改变 1103=椎间隙 1103=均匀 1103=周围 1103=软组织 1103=未见异常 1104=nan 0101=双侧 0101=甲状腺 0101=大小 0101=形态 0101=正常 0101=包膜 0101=光整 0101=实质 0101=回声 0101=均匀 0101=光点 0101=稍 0101=粗 0101=未见明显异常 0101=回声 0101=CDFI 0101=： 0101=血流 0101=显示 0101=未见异常 0102=甲状腺 0102=彩超 0102=含 0102=颈部 0102=淋巴细胞 0102=未发现明显异常 A201=详见纸质报告 0979=无 0980=无 0985=无 0201=正常 0202=正常 0203=正常 0206=正常 0207=正常 0208=正常 0209=正常 0210=正常 0212=无 0215=正常 0216=正常 0217=正常 0222=耳鼻咽喉科检查未见异常 0225=nan 1001=窦性心律肢体导联低电压 0405=未见异常 0406=未见异常 0407=未见异常 0409=病史 0409=: 0409=甲状腺 0409=功能 0409=亢进 0409=治疗 0409=中 0413=未见异常 0420=未见异常 0421=整齐 0423=未见异常 0424=90--100次/分 0425=正常 0426=未见异常 0430=未见异常 0431=未见异常 0432=未见异常 0433=未见异常 0434=甲状腺功能亢进（治疗中） 0435=未见异常 A202=详见纸质报告 0102=前列腺 0102=: 0102=前列腺 0102=稍大 0102=膀胱 0102=双侧 0102=输尿管 0102=未发现明显异常 2406=63.9 2403=71.3 2404=171.0 2405=24.4 0102=肝胆胰 0102=脾 0102=左 0102=肾 0102=右肾 0102=未发现明显异常 0113=肝脏 0113=大小 0113=形态 0113=正常 0113=包膜 0113=光整 0113=肝内 0113=血管 0113=走行 0113=较 0113=清晰 0113=回声 0113=均匀 0114=胆囊 0114=大小 0114=形态 0114=正常 0114=囊壁光 0114=整囊腔 0114=内 0114=透声 0114=好 0114=胆总管 0114=无 0114=扩张 0115=胰腺 0115=大小 0115=形态 0115=正常 0115=边缘 0115=规整 0115=内部 0115=回声 0115=均匀 0115=胰管 0115=未见 0115=扩张 0116=脾脏 0116=大小 0116=形态 0116=正常 0116=包膜 0116=光整 0116=回声 0116=均匀 0117=左 0117=肾
        
        0119=膀胱:  1:1
        0119=充盈:  2:1 
        0119=良好:  3:1
    """
    buf = []
    for row in X.itertuples():
        lbuf = []
        feature_str = row.X
        us = feature_str.split(" ")

        fidset = set()
        for unit in us:
            try:
                k, v = unit.split("=", 1 )
                if k in map:
                    f = map[k] #type:Feature
                    sparse_f = f.transform(k , unit)  #0119=膀胱:  1:1
                    if sparse_f != -1:
                        fid , _  = sparse_f.split(':')

                        if sparse_f != -1 and fid not in fidset:
                            lbuf.append(sparse_f)
                            fidset.add(fid)
            except Exception as e:
                logging.warn(e)
                logging.warn(unit)
        # sort by feature_id
        lbuf.sort(key=lambda x: int(x.split(":")[0]))

        buf.append(' '.join(lbuf))

    X['sparse'] = buf

    # computer visiable.!
    X[['vid','sparse']].to_csv('X_libsvm.csv',index=False)


