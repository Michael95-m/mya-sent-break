import pyidaungsu as pds
import json

class sent_break_syl:

    def __init__(self, fld_path):
        
        with open(f'{fld_path}/end_syl.txt') as f:
            self.end_syl_ls = [line.strip() for line in f]

        with open(f'{fld_path}/look_prev.txt') as f:
            self.look_prev_ls = [line.strip() for line in f]

        with open(f'{fld_path}/skip_list.txt') as f:
            self.skip_ls = [line.strip() for line in f]

        self.break_one_gram_prev = self.load_data(f'{fld_path}/break_one_gram_prev.json')
        self.break_two_gram_prev = self.load_data(f'{fld_path}/break_two_gram_prev.json')
        self.break_three_gram_prev = self.load_data(f'{fld_path}/break_three_gram_prev.json')
        self.no_break_one_gram_next = self.load_data(f'{fld_path}/no_break_one_gram_next.json')
        self.no_break_two_gram_next = self.load_data(f'{fld_path}/no_break_two_gram_next.json')
        self.no_break_three_gram_next = self.load_data(f'{fld_path}/no_break_three_gram_next.json')

    def load_data(self, json_loc):

        with open(json_loc) as f:
            json_data = json.load(f)

        return json_data 

    def find_end_syl(self, syl_sent_ls):

        return [ i for i, syl in enumerate(syl_sent_ls) if syl in set(self.end_syl_ls) ]


    def not_break_gram_check(self, end_syl, next_syl, gram):
        gram_break = True
        look_prev = False

        if next_syl is not None:
            if gram == 1:
                if len(self.no_break_one_gram_next[end_syl]) == 0:
                    if end_syl in self.look_prev_ls:
                        look_prev = True
                    else:
                        look_prev = False
                else:
                    if next_syl in self.no_break_one_gram_next[end_syl]:
                        gram_break = False
                    else:
                        gram_break = True 

            if gram == 2:
                if len(self.no_break_two_gram_next[end_syl]) == 0:
                    if end_syl in self.look_prev_ls:
                        look_prev = True
                    else:
                        look_prev = False
                else:
                    if next_syl in self.no_break_two_gram_next[end_syl]:
                        gram_break = False
                    else:
                        gram_break = True 

            if gram == 3:
                if len(self.no_break_three_gram_next[end_syl]) == 0:
                    if end_syl in self.look_prev_ls:
                        look_prev = True
                    else:
                        look_prev = False
                else:
                    if next_syl in self.no_break_three_gram_next[end_syl]:
                        gram_break = False
                    else:
                        gram_break = True 

        return gram_break, look_prev


    def find_break_index(self, syl_sent_ls, end_index_ls, show_log=False):
        break_index_ls = []
        first_index = 0
        last_index = len(syl_sent_ls)-1

        for index in end_index_ls:

            if index != first_index and index != last_index: ## check if the first syl or the last syl

                end_syl = syl_sent_ls[index]

                if end_syl in self.skip_ls:
                    continue 

                next_syl, next_two_gram_syl, next_three_gram_syl = None, None, None

                next_syl_index = index+1
                next_two_gram_index = index+2
                next_three_gram_index = index+3
                next_four_gram_index = index+4

                next_syl = syl_sent_ls[next_syl_index] ## already check in first condition
                if next_two_gram_index <= last_index:
                    next_two_gram_syl = ' '.join(syl_sent_ls[next_syl_index: next_three_gram_index])
                if next_three_gram_index <= last_index:
                    next_three_gram_syl = ' '.join(syl_sent_ls[next_syl_index: next_four_gram_index])

                one_gram_next_break, one_gram_look_prev = self.not_break_gram_check(end_syl, next_syl, 1)
                two_gram_next_break, two_gram_look_prev = self.not_break_gram_check(end_syl, next_two_gram_syl, 2)
                three_gram_next_break, three_gram_look_prev = self.not_break_gram_check(end_syl, next_three_gram_syl, 3)

                if show_log:
                    print(f"current syl is {end_syl}")
                    print(f"one_gram_next_break is {one_gram_next_break}")
                    print(f"two_gram_next_break is {two_gram_next_break}")
                    print(f"three_gram_next_break is {three_gram_next_break}")

                ## use next cases 
                is_break_next = one_gram_next_break and two_gram_next_break and three_gram_next_break
                look_prev = one_gram_look_prev or two_gram_look_prev or three_gram_look_prev

                if show_log:
                    print(f"break or not based on next syl is {is_break_next}")
                    print(f"look prev based on current syl is {look_prev}")

                if is_break_next:
                    break_index_ls.append(index)
                    print()
                    continue 

                if look_prev and is_break_next:

                ## if looking prev is needed
                    prev_syl, prev_two_gram_syl, prev_three_gram_syl = None, None, None

                    prev_syl_index = index-1
                    prev_two_gram_index = index-2
                    prev_three_gram_index = index-3
                    prev_four_gram_index = index-4

                    prev_syl = syl_sent_ls[prev_syl_index] ## already check in first condition
                    if prev_two_gram_index <= last_index:
                        prev_two_gram_syl = ' '.join(syl_sent_ls[prev_syl_index: prev_three_gram_index])
                    if prev_three_gram_index <= last_index:
                        prev_three_gram_syl = ' '.join(syl_sent_ls[prev_syl_index: prev_four_gram_index])

                    one_gram_prev_break = False 
                    two_gram_prev_break = False 
                    three_gram_prev_break = False 

                    if len(self.break_one_gram_prev[end_syl]) == 0 or \
                        prev_syl in self.break_one_gram_prev[end_syl]:
                        one_gram_prev_break = True 
                    if len(self.break_two_gram_prev[end_syl]) == 0 or \
                        prev_two_gram_syl in self.break_two_gram_prev[end_syl]:
                        two_gram_prev_break = True 
                    if len(self.break_three_gram_prev[end_syl]) == 0  or \
                        prev_three_gram_syl in self.break_three_gram_prev[end_syl]:
                        three_gram_prev_break = True 

                    if show_log:
                        print(f"one_gram_prev_break is {one_gram_prev_break}")
                        print(f"two_gram_prev_break is {two_gram_prev_break}")
                        print(f"three_gram_prev_break is {three_gram_prev_break}")

                    ## use "or"  operator unlike next cases
                    ## because if one matches, it's ok to break
                    is_break_prev = one_gram_prev_break or two_gram_prev_break or three_gram_prev_break 

                    if show_log:
                        print(f"break or not based on prev syl is {is_break_prev}")
                        print()

                    if is_break_prev:
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
