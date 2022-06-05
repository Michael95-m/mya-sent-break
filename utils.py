import pandas as pd
from tqdm import tqdm
import pyidaungsu as pds
import json

class sent_break_syl:

    def __init__(self):

        self.end_syl_ls = self.__load_data('data_syl/break_one_gram_prev.json')
        self.break_one_gram_prev = self.__load_data('data_syl/break_one_gram_prev.json')
        self.no_break_one_gram_next = self.__load_data('data_syl/no_break_one_gram_next.json')
        self.no_break_two_gram_next = self.__load_data('data_syl/no_break_two_gram_next.json')
        self.no_break_three_gram_next = self.__load_data('data_syl/no_break_three_gram_next.json')

    def __load_data(self, json_loc):

        with open(json_loc) as f:
            json_data = json.load(f)

        return json_data 

    def __find_end_syl(self, syl_sent_ls):

        return [ i for i, syl in enumerate(syl_sent_ls) if syl in set(self.end_syl_ls) ]

    def __find_break_index(self, syl_sent_ls, end_index_ls):
        break_index_ls = []

        for index in end_index_ls:

            if index == 0:
                continue
            if index == len(syl_sent_ls)-1:
                continue
            end_syl = syl_sent_ls[index]

            prev_syl = syl_sent_ls[index-1]
            next_syl = syl_sent_ls[index+1]
            if index+3 <= len(syl_sent_ls)-1:
                next_two_gram_syl = ' '.join(syl_sent_ls[index+1: index+3])
            if index+4 <= len(syl_sent_ls)-1:
                next_three_gram_syl = ' '.join(syl_sent_ls[index+1: index+4])

            print(f'end_syl is {end_syl}')
            if prev_syl not in self.break_one_gram_prev[end_syl].keys():
                print(prev_syl)
                print('prev syl failed')
                continue

            one_gram_ok = True
            two_gram_ok = True
            three_gram_ok = True

            # if next_syl in self.no_break_one_gram_next[end_syl].keys():
            #     print('next syl failed')
            #     one_gram_ok = False
            if next_two_gram_syl in self.no_break_two_gram_next[end_syl].keys():
                print('next two gram syl failed')
                two_gram_ok = False
            elif next_three_gram_syl in self.no_break_three_gram_next[end_syl].keys():
                print('next three gram syl failed')
                three_gram_ok = False

            break_or_not =   two_gram_ok and three_gram_ok
            if break_or_not:
                break_index_ls.append(index)

        return break_index_ls 

    def chg_into_dummy(self, syl_sent_ls, break_index_ls):
        acc = 1
        for i in range(len(break_index_ls)):
            syl_sent_ls.insert(break_index_ls[i]+acc, '//')
            acc += 1

        return ' '.join(syl_sent_ls)

    def break_sent(self, sent):

        syl_sent_ls = pds.tokenize(sent)
        end_index_ls = self.__find_end_syl(syl_sent_ls)
        break_index_ls = self.__find_break_index(syl_sent_ls, end_index_ls)
        syl_sent_break = self.chg_into_dummy(syl_sent_ls, break_index_ls)

        return syl_sent_break       