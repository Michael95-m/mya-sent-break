import numpy as np 
import pandas as pd

DICT_STRING = ' ၀၁၂၃၄၅၆၇၈၉၊။'

class Normalization(object):
    """
    This function normalizes common errors for Burmese Language.
    Eg: ၇ > ရ , ၀ > ဝ , င့် > င့် (i.e, sequence order error)
    Usage : 
     For all normalization >> 
     n = Normalization()
     n.normalize_data('ယဥ််')
     For sequence validation only >> 
     n = Normalization()
     n.validate_sequence('ဖြင့်') ... etc. xD
     pre_rule_fix function is only for fixing ရ & ၀ case. 
     ## will be updated after found sth
    """
    def __init__(self):
        pass
    
    def validate_sequence(self, sent):
        
#         sent = sent.replace('င့်','င့်').replace('ည့်','ည့်').replace('မ့်','မ့်').replace('န့်','န့်').replace('ဉ့်','ဉ့်').replace('ယ့်','ယ့်').replace('စျ','ဈ').replace('ဥ့်','ဉ့်').replace('ဥ်','ဉ်').replace('််',်').
        sent = sent.replace('ပာ', 'ပါ') ## wrong with ဟ
        sent = sent.replace('့်','့်').replace('််','်').replace('ိိ','ိ').replace('ီီ','ီ').replace('ံံ', 'ံ').replace('ဲဲ', 'ဲ')
        sent = sent.replace('စျ','ဈ').replace('ဥ့်','ဉ့်').replace('ဥ်','ဉ်')
        sent = sent.replace('ဩော်','ဪ').replace('သြော်','ဪ').replace('သြ','ဩ')
        sent = sent.replace('ဉီ','ဦ').replace('ဦ','ဦ')
        return sent
    
    def remove_whitespace(self, sent):
        sent = sent.replace('\u200a', '')
        sent = sent.replace('\u200b', '')
        sent = sent.replace('\u200c', '')
        sent = sent.replace('\u200d', '')
        sent = sent.replace('\u200e', '')
        sent = sent.replace('\u200f', '')
        sent = sent.replace('\xa0', '')
        sent = sent.replace('•', '')
        sent = sent.replace('\u202d', '')
        return sent
    
    def zero2walone(self, y):
        y = list(f' {y} ')
        for i in np.where(np.asarray(y) == '၀')[0]:
            if y[i+1] not in DICT_STRING and y[i-1] not in DICT_STRING:
                y[i] = 'ဝ'

        return ''.join(y[1:-1])

    def walone2zero(self, y):
        y = list(f' {y} ')
        for i in np.where(np.asarray(y) == 'ဝ')[0]:
            if y[i+1] in DICT_STRING and y[i-1]  in DICT_STRING:
                y[i] = '၀'

        return ''.join(y[1:-1])

    def seventoyagouk(self, y):
        y = np.asarray(list(y))
        for i in np.where(y == '၇')[0]:
            if i<len(y)-1:
                if y[i+1] not in list('၀၁၂၃၄၅၆၇၈၉၊။'):
                    y[i] = 'ရ'
        return ''.join(y)

    def pre_rule_fix(self,text):
        # text = [str(y) for y in text]
        text = self.zero2walone(text)
        text = self.walone2zero(text)
        # text = self.seventoyagouk(text)
        return text

    def normalize_sent(self, sent):
        # sent = sent_level_norm(sent)
        word_ls = []
        for word in sent.strip().split():
            new_word = self.normalize_data(word)
            word_ls.append(new_word)
        new_sent = ' '.join(word_ls)
        return new_sent 
    
    def normalize_data(self, text, chk_prerule_fix=True):
        # try:
            
        text = self.remove_whitespace(text)
        text = self.validate_sequence(text)
        if chk_prerule_fix:
            text = self.pre_rule_fix(text)
        return text
    
def del_miss_char(corpus_main_ls):
    fine_sent = []
    fau_sent = []
    for sent in corpus_main_ls:
        if '�' in sent:
            fau_sent.append(sent)
        else:
            fine_sent.append(sent)
            
    return fine_sent, fau_sent
    