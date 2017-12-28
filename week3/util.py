import re
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
GOOD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
def text_prepare(text):
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = GOOD_SYMBOLS_RE.sub('', text)
    text = ' '.join([x for x in text.split() if x and x not in STOPWORDS])
    return text.strip()

def array_to_string(arr):
    return '\n'.join(str(num) for num in arr)

def matrix_to_string(matrix):
    return '\n'.join('\t'.join(str(num) for num in line) for line in matrix)