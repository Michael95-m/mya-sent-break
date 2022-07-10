import pandas as pd
from tqdm import tqdm
import pyidaungsu as pds
import json

class sent_break_syl:

    def __init__(self, fld_path):
        
        with open(f'{fld_path}/end_syl.txt') as f:
            self.end_syl_ls = [line.strip() for line in f]
        self.break_one_gram_prev = self.__load_data(f'{fld_path}/break_one_gram_prev.json')
        self.break_two_gram_prev = self.__load_data(f'{fld_path}/break_two_gram_prev.json')
        self.break_three_gram_prev = self.__load_data(f'{fld_path}/break_three_gram_prev.json')
        self.no_break_one_gram_next = self.__load_data(f'{fld_path}/no_break_one_gram_next.json')
        self.no_break_two_gram_next = self.__load_data(f'{fld_path}/no_break_two_gram_next.json')
        self.no_break_three_gram_next = self.__load_data(f'{fld_path}/no_break_three_gram_next.json')

    def __load_data(self, json_loc):

        with open(json_loc) as f:
            json_data = json.load(f)

        return json_data 

    def find_end_syl(self, syl_sent_ls):

        return [ i for i, syl in enumerate(syl_sent_ls) if syl in set(self.end_syl_ls) ]

    def find_break_index(self, syl_sent_ls, end_index_ls, show_log=False):
        break_index_ls = []

        for index in end_index_ls:

            if index == 0:
                continue
            if index == len(syl_sent_ls)-1:
                continue
            end_syl = syl_sent_ls[index]

            prev_syl = syl_sent_ls[index-1]
            if index-1 >= 0:
                prev_two_gram_syl = ' '.join(syl_sent_ls[index-1: index+1])
            if index-2 >= 0:
                prev_two_gram_syl = ' '.join(syl_sent_ls[index-2: index+1])

            if show_log:
                print(f'end_syl is {end_syl}')

            one_gram_break_ok = False 
            two_gram_break_ok = False 
            three_gram_break_ok = False 

            if len(self.break_one_gram_prev[end_syl].keys()) == 0 or \
                prev_syl in self.break_one_gram_prev[end_syl].keys():
                one_gram_break_ok = True 
            if len(self.break_two_gram_prev[end_syl].keys()) == 0 or \
                prev_syl in self.break_two_gram_prev[end_syl].keys():
                two_gram_break_ok = True 
            if len(self.break_three_gram_prev[end_syl].keys()) == 0  or \
                prev_syl in self.break_three_gram_prev[end_syl].keys():
                three_gram_break_ok = True 

            prev_break_or_not = one_gram_break_ok or two_gram_break_ok or three_gram_break_ok
            if show_log:
                    print(f'one gram break ok : {one_gram_break_ok}')
                    print(f'two gram break ok : {two_gram_break_ok}')
                    print(f'three gram break ok : {three_gram_break_ok}')
                    print(f'prev break or not: {prev_break_or_not}')    
                    
            if not prev_break_or_not:
                if show_log:
                    print(f'break failed for {end_syl}')
                continue
            
            if show_log:
                print('-'*10)
                       
            next_syl, next_two_gram_syl, next_three_gram_syl = None, None, None 

            next_syl = syl_sent_ls[index+1]
            if index+2 <= len(syl_sent_ls)-1:
                next_two_gram_syl = ' '.join(syl_sent_ls[index+1: index+3])
            if index+3 <= len(syl_sent_ls)-1:
                next_three_gram_syl = ' '.join(syl_sent_ls[index+1: index+4])

            one_gram_ok = True
            two_gram_ok = True
            three_gram_ok = True

            if next_syl is not None:
                if len(self.no_break_one_gram_next[end_syl].keys()) != 0 \
                    and next_syl in self.no_break_one_gram_next[end_syl].keys():
                    one_gram_ok = False
            if next_two_gram_syl is not None:
                if len(self.no_break_two_gram_next[end_syl].keys()) != 0 \
                    and next_two_gram_syl in self.no_break_two_gram_next[end_syl].keys():
                    two_gram_ok = False
            if next_three_gram_syl is not None:
                if len(self.no_break_three_gram_next[end_syl].keys()) != 0 \
                    and next_three_gram_syl in self.no_break_three_gram_next[end_syl].keys():
                    three_gram_ok = False

            break_or_not =   one_gram_ok and two_gram_ok and three_gram_ok
            if show_log:
                    print(f'one gram next break : {one_gram_ok}')
                    print(f'two gram next break : {two_gram_ok}')
                    print(f'three gram next break : {three_gram_ok}')
                    print(f'next break or not: {break_or_not}') 
                    print('-'* 10)
            if break_or_not:
                break_index_ls.append(index)

        return break_index_ls 

    def chg_into_dummy(self, syl_sent_ls, break_index_ls):
        acc = 1
        for i in range(len(break_index_ls)):
            syl_sent_ls.insert(break_index_ls[i]+acc, '//')
            acc += 1

        return ' '.join(syl_sent_ls)

    def break_sent(self, sent, show_log=False):

        syl_sent_ls = pds.tokenize(sent)
        end_index_ls = self.find_end_syl(syl_sent_ls)
        break_index_ls = self.find_break_index(syl_sent_ls, end_index_ls, show_log)
        syl_sent_break = self.chg_into_dummy(syl_sent_ls, break_index_ls)

        return syl_sent_break       