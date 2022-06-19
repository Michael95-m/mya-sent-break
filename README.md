Burmese Sentence Segmentation by checking ngram
------------
This is the repository about how to segment the sentence written in burmese by rule-based ngram checking method.

----------------------
### Requirements

1. Install python and create python virtual environment
```
python3 -m venv .venv
```

2. Activate Python virtual environment
```
source .venv/bin/activate
```

3. Install python denpendencies
```
pip install -r requirements.txt
```

---------------------------
### How to run sentence segmentation

```python
from utils import sent_break_syl
from normalize.normalize_data import Normalization

norm_obj = Normalization() ## create normalization object 
sent_break_obj = sent_break_syl() ## create sentence break syllabel segmentation object

sent = 'အဆင်မပြေပါဘူး အထူသား၀ယ်တာ အပါးသားရောက်လာပါတယ် ပြထားတဲ့ပုံနဲ့ တခြားဆီပဲ...အပါးတွေက လွယ်၂ ၀ယ်လို့ရတယ် ၃ထောင်အများဆုံပဲ အခုကအထူသားလိုချင်လို မှာတာ အပါးလေးရောက်လာတယ် ၅ထောင်ပေး၀ယ်ရပြိးတေ့ စိတ်ပျက်တယ်'

print(sent_break_obj.break_sent(sent, False))

# output result --> အ ဆင် မ ပြေ ပါ ဘူး // အ ထူ သား ဝယ် တာ အ ပါး သား ရောက် လာ ပါ တယ် // ပြ ထား တဲ့ ပုံ နဲ့ တ ခြား ဆီ ပဲ // . . . အ ပါး တွေ က လွယ် ၂၀ ယ် လို့ ရ တယ် // ၃ ထောင် အ များ ဆုံ ပဲ // အ ခု က အ ထူ သား လို ချင် လို မှာ တာ အ ပါး လေး ရောက် လာ တယ် ၅ ထောင် ပေး ဝယ် ရ ပြိး တေ့ စိတ် ပျက် တယ်

```



