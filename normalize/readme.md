<h2> Normalization Usage </h2>

--------------

**normalize_data.py** is used for normalizing different character order but visually similar.(eg. **သင့်** and **သင့်**). **sent_level_order.py** can fix  wrong character order like **တေွ** to **တွေ** and can fix wrong spelling like **မျိူး** to **မျိုး**.

```python
from normalize.normalize_data import Normalization
from sent_level_order import sent_level_norm 

sent = 'အိပ်ယာနိုးရင်ခြေဖဝါးတွေနာလာလို့ စစ်ကြည့်တာ'
norm_obj = Normalization()

sent = sent_level_norm(sent) ##  first step
sent = norm_obj.normalize_data(sent) ## second step 
```
