from itertools import chain
import re
import emoji


class WordBreak_preprocess():
    def __init__(self):
        self.MY_SYLLABLE_PATTERN = re.compile(
            r'(?:(?<!္)([\U00010000-\U0010ffffက-ဪဿ၊-၏]|[၀-၉]+|[^က-၏\U00010000-\U0010ffff]+)(?![ှျ]?[့္်]))',
            re.UNICODE)
        self.ENG_MY_SPLIT_PATTERN = re.compile(
            r'[https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}]+|[\u2707-\u27B0]+|[\U00010000-\U0010ffff]+|[က-ဪဿ၊-၏^က-၏ ]+|[0-9a-zA-Z.@-]+|[“”!\"#$%&\'()*\+,-./:;<=>?@\[\\\]^_`{|}~]+'
        )
    #check whole sentence for english
        self.ENG_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')
    #check True if only a part of sentence contains english
        self.ENG_PATTERN_word = re.compile(r'[a-zA-Z0-9]+')

    def syllable_break(self, text):
        return self.MY_SYLLABLE_PATTERN.sub(r'𝕊\1', text).strip('𝕊').split('𝕊')

    def separate_eng_mm(self, text):
        return self.ENG_MY_SPLIT_PATTERN.findall(text)

    def syllable_break_both(self, text):

        return list(
            chain.from_iterable([
                self.syllable_break(i) for i in self.separate_eng_mm(text)
                if i != ' ' or i != ''
            ]))

    def syllable_break_eng_my_split(self, text):
        clean_data = " ".join(text.split())
        example_test = self.syllable_break_both(clean_data)
        temp_list = example_test
        for idx, data in enumerate(example_test):
            if self.ENG_PATTERN.match(data):
                if idx + 1 < len(example_test):
                    if self.MY_SYLLABLE_PATTERN.match(example_test[
                            idx +
                            1]) and example_test[idx + 1] != ' ' and not (
                                self.ENG_PATTERN.match(example_test[idx + 1])):
                        temp_list.insert(idx + 1, ' ')
        return temp_list

    def syllable_break_list(self, text):
        '''Parameters:
        input_value: list
        Returns: syllable values with no spaces
        e.g. [['09950367221', 'တစ်', 'SwanAung', 'car', 'တယ်', 'OK', '$', '😁', '😂'],
                    ['slkfjlskfj', 'car', 'စာ', 'အုပ်', 'sfsfd']]'''
        words = [self.syllable_break_both(data) for data in text]
        filtered_words = [
            list(filter(lambda word: word.strip(), msg)) for msg in words
        ]
        return filtered_words


