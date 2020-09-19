import json
import re
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, TimeDistributed, Dense, Dropout
from tf2crf import CRF
from tensorflow.keras.preprocessing.sequence import pad_sequences
import csv

def split_sentence(s, character):
    s1 = []
    for s2 in s:
        if (s2 != ""):
            s3 = s2.split(character)
            for s4 in s3:
                if (s4 != ""):
                    s1.append(s4)
    return s1

with open('data.json', encoding="utf8") as json_file:
    data = json.load(json_file)
text=[]
for book in data:
    text.append(book['description'])
    for review in book['review']:
        text.append(review['content'])
        for cmt in review['list_cmt']:
            text.append(cmt['cmt'])

sentences_1=[]
for s in text:
    s1 = s.split("\n")
    s3 = split_sentence(s1, '.')
    s3 = split_sentence(s3, '-')
    s3 = split_sentence(s3, "'")
    s4 = []
    for s2 in s3:
        s4.append(re.findall(r"[\w']+", s2))
    if (len(s4)>0):
        sentences_1+=s4

sentences=[]
for s in sentences_1:
    sentence=[]
    for w in s:
        sentence.append(w.lower())
    sentences.append((sentence))

with open('w2i.json', encoding="utf8") as json_file:
    word2idx = json.load(json_file)
with open('i2w.json', encoding="utf8") as json_file:
    idx2word = json.load(json_file)

max_len=223

model=Sequential()
model.add(Embedding(input_dim=len(word2idx), output_dim=40, input_length=max_len, mask_zero=False))
model.add(Bidirectional(LSTM(units=64, return_sequences=True, recurrent_dropout=0.2, dropout=0.2)))
model.add(TimeDistributed(Dense(64, activation="relu")))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(64, activation="relu")))
model.add(Dropout(0.2))
crf = CRF(4)  # CRF layer
model.add(crf)
model.load_weights('model.h5')

name=[]
for s in sentences:
    s_ids=[]
    for w in s:
        if (w in word2idx):
            s_ids.append(word2idx[w])
        else:
            s_ids.append(word2idx['UNK'])
    X = pad_sequences(maxlen=max_len, sequences=[s_ids], padding="post", value=word2idx["PAD"])
    predict = model.predict(X)
    for i in range(max_len):
        if predict[0][i] == 1:
            a = s[i]
            k = i + 1
            while (k < len(s) and predict[0][k] == 2):
                a += ' ' + s[k]
                k += 1
            name.append(a)
            print(a)
print(name)

with open('name.csv', 'w', newline='', encoding="utf8") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(name)