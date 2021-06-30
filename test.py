import os
import numpy as np
from bm25 import BM25Okapi
# import pkuseg
import jieba

# seg = pkuseg.pkuseg()

# sp_char = ['（', '(', '/' , '·']
def doc_init():

    path = 'docs'
    files = os.listdir(path)
    title = {}
    corpus = {}

    for file in files:
        file_path = path + '/' + file
        kewen_id = file.split('.')[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            res = ''

            # ------------------------ 题目处理 ---------------------------

            raw_timu = ''.join(lines[0].strip().split())
            if raw_timu not in title:
                title[raw_timu] = []
                title[raw_timu].append(kewen_id)
            else:
                title[raw_timu].append(kewen_id)


            if '·' in raw_timu:
                part = raw_timu.split('·')
                for timu in part:
                    if timu not in title:
                        title[timu] = []
                        title[timu].append(kewen_id)
                    else:
                        title[timu].append(kewen_id)
            if '/' in raw_timu:
                part = raw_timu.split('/')
                for timu in part:
                    if timu not in title:
                        title[timu] = []
                        title[timu].append(kewen_id)
                    else:
                        title[timu].append(kewen_id)

            if '（' in raw_timu:
                timu = raw_timu.split('（')[0]
                if timu not in title:
                    title[timu] = []
                    title[timu].append(kewen_id)
                else:
                    title[timu].append(kewen_id)
            if '(' in raw_timu:
                part = raw_timu.split('(')[0]
                if timu not in title:
                    title[timu] = []
                    title[timu].append(kewen_id)
                else:
                    title[timu].append(kewen_id)

            # ------------------- 作者处理 ------------------------------

            raw_zz = lines[1].strip()
            if len(raw_zz) != 0:
                raw_zz_split = raw_zz.split()
                if len(raw_zz_split) == 2:
                    zz = raw_zz_split[1]
                    if zz not in title:
                        title[zz] = []
                        title[zz].append(kewen_id)
                    else:
                        title[zz].append(kewen_id)
                else:  # len(raw_zz_split)==1
                    zz = raw_zz_split[0]
                    if zz not in title:
                        title[zz] = []
                        title[zz].append(kewen_id)
                    else:
                        title[zz].append(kewen_id)

            # ----------------- 随机内容处理 ---------------------------
            for line in lines:
                text1 = [w for w in line.strip()]
                text2 = jieba.lcut(line.strip())
                # text3 = seg.cut(line.strip())
                line = ' '.join(text1) + ' ' + ' '.join(text2) + ' '
                res += line
            corpus[res[:-1]] = kewen_id

    tokenized_corpus = [doc.split(' ') for doc in corpus.keys()]
    bm25 = BM25Okapi(tokenized_corpus)
    return title, corpus, bm25


def search(bm25, query, n):
    text1 = [w for w in query]
    text2 = jieba.lcut(query)
    # text3 = seg.cut(query)
    text = text1 + text2
    # print('query分词: ', text)

    doc_scores = bm25.get_scores(text)
    #     topn_scores = doc_scores[np.argsort(doc_scores)[::-1][:n]]
    #     print(topn_scores)
    #     print('文档最高得分：', max(doc_scores), '\n')

    if max(doc_scores) > 0:
        results = bm25.get_top_n(text, list(corpus.keys()), n)
        return results
    else:
        print('无匹配文档')
        return


if __name__ == '__main__':
    # 文档预处理与预加载
    title, corpus, bm25 = doc_init()

    # query搜索匹配
    query = "历史朝代"
    if query in title:
        print('【文档匹配id】：%s' % title[query])
    else:
        results = search(bm25, query, n=3)
        # print('【文档匹配id】：%s' % ([corpus[res] for res in results]))

        for res in results:
            print('【文档匹配id】：%s,  【文档】：%s' % (corpus[res], ''.join(res.split(' '))), '\n')