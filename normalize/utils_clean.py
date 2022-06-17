from normalize.normalize_data import Normalization, del_miss_char
import os 
import pandas as pd
from tqdm import tqdm 
import json
import re
from g2p.g2p_gen import g2p_tag 

tqdm.pandas()

def w2ph_create(lexicon_ls):
    w2ph_dict = {}
    for lexicon in lexicon_ls:
        ls = lexicon.split()
        word = ls[0]
        phone = ls[1:]
        phone = ' '.join(phone)
        if word not in w2ph_dict.keys():
            w2ph_dict[word] = [] 
        if phone not in w2ph_dict[word]:
            w2ph_dict[word].append(phone)
    return w2ph_dict 

def ph2w_create(lexicon_ls):
    ph2w_dict = {}
    for lexicon in lexicon_ls:
        ls = lexicon.split()
        word = ls[0]
        phone = ls[1:] 
        phone = ' '.join(phone)
        if phone not in ph2w_dict.keys():
            ph2w_dict[phone] = []
        if word not in ph2w_dict[phone]:
            ph2w_dict[phone].append(word) 
    return ph2w_dict

def f_write_ls(file_loc, line_ls):
    with open(file_loc, 'w') as file:
        for line in line_ls:
            file.write('%s\n'%line)

class corpus_clean:

    def __init__(self, dir_loc, g2p_loc = 'g2p/s2p4k1.csv'):
        self.n = Normalization()
        if not os.path.exists(dir_loc):
            os.makedirs(dir_loc)

        self.dir_loc = dir_loc 
        self.g2p_obj = g2p_tag(g2p_loc)

    def normalize_line(self, row):
        word_ls = []
        for word in row.line.split():
            new_word = self.n.normalize_data(word)
            word_ls.append(new_word)
        row['line'] = ' '.join(word_ls)
        return row 

    def sent_to_word(self, sent_ls):
        word_ls = set()
        for sent in sent_ls:
            for word in sent.split():
                word_ls.add(word)
        word_ls = list(set(word_ls)) 
        return word_ls

    def corpus_clean(self, sent_ls, use_norm=True):
          
        df = pd.DataFrame({'line': sent_ls})
        print('[INFO] Count of original sentence is ', len(df))
        
        df = df.dropna()
        print('[INFO] Count of sentence after dropping na is ', len(df))
        
        dup_df = df[df.duplicated()]
        df = df.drop_duplicates()
        print('[INFO] Count of sentence after dropping duplicate is ', len(df))
        dup_df.to_csv('{}/dup_df.csv'.format(self.dir_loc), index=False)
        
        if use_norm:
            print('[INFO] Normalization')
            df = df.progress_apply(self.normalize_line, axis=1)
            
            dup_df2 = df[df.duplicated()]
            df = df.drop_duplicates()
            print('[INFO] Count of Sentence after normalization and dropping duplicate is ', len(df))
            dup_df2.to_csv('{}/dup_norm_df.csv'.format(self.dir_loc), index=False)
        
        df['no_sp'] = df.line.apply(lambda x: re.sub("\s+", "", x))
        dup_wb_df = df[df.duplicated(subset=['no_sp'], keep=False)]
        dup_wb_df = dup_wb_df.sort_values(by=['line'])
        dup_wb_df = dup_wb_df[['line']]
        dup_wb_df.to_csv('{}/dup_wb_df.csv'.format(self.dir_loc), index=False)
        print('[INFO] Count of same Sentence with different word break is ', len(dup_wb_df))
        
        df = df.drop_duplicates(subset=['no_sp'], keep=False)
        df = df[['line']]
        print('[INFO] Count of Sentence after dropping same sentence with different word break is ', len(df))

        sent_ls = df.line.tolist()
        good_ln, bad_ln = del_miss_char(sent_ls)
        good_ln = sorted(good_ln)
        bad_ln = sorted(bad_ln)
        print('[INFO] Count of Sentence after removing missing character is ', len(good_ln))    
        f_write_ls('{}/clean.txt'.format(self.dir_loc), good_ln)
        f_write_ls('{}/miss_char.txt'.format(self.dir_loc), bad_ln)

        # if tag_g2p:
        #     print('[INFO] Tagging G2P')
        #     g2p_df = self.g2p_obj.tag(good_ln)
        #     g2p_df.to_csv('{}/gp2_corpus_only.csv'.format(self.dir_loc), index=False)
        #     print('[INFO] Tagging G2P finished')

    def gen_spell_chk(self, lexicon_ls):
    
        ph2w_dict = ph2w_create(lexicon_ls)
        mis_spell_dict = {key: word for key, word in ph2w_dict.items() if len(word) > 1}
        print('[INFO] There are {} scipious words to check '.format(len(mis_spell_dict)))

        ph_neme_ls = list(mis_spell_dict.keys())
        word_ls = list(mis_spell_dict.values())
        
        spell_chk_df = pd.DataFrame()
        spell_chk_df['phneme'] = ph_neme_ls
        spell_chk_df['chk_words'] = word_ls
        
        spell_chk_df = spell_chk_df.sort_values(by=['chk_words']) ## sort with check words 
        spell_chk_df.to_csv('{}/spell_chk.csv'.format(self.dir_loc), index=False)

    def gen_only_words(self, lexicon_ls, corpus_ls, tag_g2p=False):

        lexi_ls = list(set(lexicon_ls))
        w2ph_dict = w2ph_create(lexi_ls)
        lexi_word_ls = [lexi.strip().split()[0] for lexi in lexi_ls]
        cor_word_ls = self.sent_to_word(corpus_ls) 

        print('[INFO] There are {} unique words in lexicon'.format(len(lexi_word_ls)))
        print('[INFO] There are {} unique words in corpus'.format(len(cor_word_ls)))

        cor_worddf = pd.DataFrame({'word': cor_word_ls})
        lexi_worddf = pd.DataFrame({'word': lexi_word_ls})

        union_df = pd.merge(cor_worddf, lexi_worddf, how='outer', indicator=True, on='word')

        corpus_only_df = union_df[union_df['_merge'] == 'left_only']
        lexi_only_df = union_df[union_df['_merge'] == 'right_only']
        print('[INFO] There are {} and {} words in corpus and lexicon only words'.format(len(corpus_only_df), len(lexi_only_df)))

        corpus_only_df = corpus_only_df.sort_values(by=['word'])
        lexi_only_df = lexi_only_df.sort_values(by=['word'])
        lexi_only_df = lexi_only_df.drop_duplicates()
        lexi_only_df['phneme'] = lexi_only_df.word.apply(lambda x: w2ph_dict[x])
        lexi_only_df = lexi_only_df[['word', 'phneme']]
        
        corpus_words = corpus_only_df.word.tolist()

        if tag_g2p: 
            print('[INFO] Tagging G2P')
            g2p_df = self.g2p_obj.tag(corpus_words)
            
            print('[INFO] Tagging G2P finished')

        if tag_g2p:
            g2p_df.to_csv('{}/gp2_corpus_only.csv'.format(self.dir_loc), index=False)
        else:
            f_write_ls('{}/corpus_only.txt'.format(self.dir_loc), corpus_words)
        lexi_only_df.to_csv('{}/lexi_only.csv'.format(self.dir_loc), index=False)



