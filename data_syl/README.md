Syllable Segmentation data
------------------

1. end_syl.txt 

This is the file containing the syllables which can be the end of the sentence.

2. break_one_gram_prev.json

The sentence can be ended if the previous syl and the sentence ending syl matches. Example.

```json
"တယ်": [
        "ကောင်း",
        "ချင်",
        "လာ",
        "ပါ",
        "ကြ",
        "သွား",
        "ကြိုက်"
]
```

The word "တယ်" can be the end of the sentence when its previous syllable is "ပါ". eg. ပါ တယ် ။ 

3. break_two_gram_prev.json

Same concept with break_one_gram_prev.json except it checks between two previous ngram syl and the sentence ending syl matches. 

4. break_three_gram_prev.json

Same concept with break_one_gram_prev.json except it checks between three previous ngram syl and the sentence ending syl matches.

5. no_break_one_gram_next.json

The sentence can't be ended if this syllable exists next to the sentence ending syllable. Example.

```json
"တယ်": [
        "တဲ့",
        "ဆို",
        "နော်",
        "လေ",
        "အစ်",
        "ပေါ့",
        "မ",
        "လို့",
        "ရှင့်"
    ]
```
The word "တယ်" can not be the end of the sentence if its next syllable is "ဆို", "ရှင့်", "နော်" and "လို့". 
 eg. တယ် ဆို, တယ် ရှင့်, တယ် နော်, တယ် လို့. 

6. no_break_two_gram_next.json

Same concept with no_break_one_gram_next.json except it checks between two next ngram syl and the sentence ending syl matches. 

7. no_break_three_gram_next.json

Same concept with no_break_one_gram_next.json except it checks between three next ngram syl and the sentence ending syl matches. s
