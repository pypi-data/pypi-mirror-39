from itertools import product
from itertools import islice
word='ശാസന'
letters = 'ശഷസശഷസ'

for replacement, pos in product(letters, range(len(word)) ):
    s = list(word)
    original = s[pos]
    if original in letters:
        s[pos] = replacement
        print(''.join(s))