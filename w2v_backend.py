from time import gmtime, strftime

import logging, gensim, scipy
import pandas as pd
import numpy as np

# Load Model
print('[ ]', strftime('%H:%M:%S', gmtime()), ' Loading model...')
model = gensim.models.KeyedVectors.load_word2vec_format('src/w2v_model.wv')
print('[x]', strftime('%H:%M:%S', gmtime()),' Model loaded')

# Test the model
#print(model.similarity('black_metal', 'death_metal'))

query = []
query.append(input('Enter a query item (ENTER to stop): '))

while query[len(query)-1] != '':
    query.append(input('Enter a query item (ENTER to stop): '))

query.remove('')

print('[ ]', strftime('%H:%M:%S', gmtime()), ' Querying the model...')

arr =  np.array(())
l = []
for i in query:

    ls = []

    for j in query:
        try:
            ls.append(round(model.similarity(str(i), str(j)),8))
        except:
            ls.append('0')
    l.append(ls)
    c_arr = np.array(l)
    
df = pd.DataFrame(c_arr, index=query, columns=query)

print('[x]', strftime('%H:%M:%S', gmtime()), ' Cosines generated')

print('[ ]', strftime('%H:%M:%S', gmtime()), ' Saving cosines...')
csv_location = 'exports/' + strftime('%y%m%d_%H%M%S') + ' - W2V_Cosines.csv'
df.to_csv(csv_location)
print('[x]', strftime('%H:%M:%S', gmtime()), ' Cosines saved')

#print(df.head())

print("[x] Finished! Check the 'exports' folder to see the results")