import argparse 
import numpy as np
import random 
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Dropout
from keras.optimizers import RMSprop
import sys



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type=str, required=True) 
	parser.add_argument('--model', type=str, default='LSTM')

	args = parser.parse_args()

	lyric_chars = open(args.file).read()
	lyrics_chars = lyric_chars.lower()

	chars = sorted(list(set(lyric_chars)))
	chars_len = len(chars)

	char_to_int = dict((c, i) for i, c in enumerate(chars))
	int_to_char = dict((i, c) for i, c in enumerate(chars))

	#print(len(lyric_chars))
	#print(lyric_chars)

	seq_length = 20
	lyrics = []
	next_chars = []

	for i in range(0,len(lyric_chars)-seq_length,1):
		lyrics.append(lyric_chars[i:i+seq_length])
		next_chars.append(lyric_chars[i+seq_length])

	#print(lyrics)

	#number of cases it just looked at	
	print(len(lyrics))

	X = np.zeros((len(lyrics), seq_length, chars_len), dtype=np.int)
	y = np.zeros((len(lyrics), chars_len), dtype=np.int)
	for i, substring in enumerate(lyrics):
	    for j, char in enumerate(substring):
	    	# print(sentence)
	    	# print(char)
	    	#i is the specific case of all possibilities when looking at the whole text in substrings of len seq_length
	    	#t is 0->seq_length
	    	#for each case, 1 assigned to the chars that appear in the substring with length seq_length
	    	X[i, j, char_to_int[char]] = 1
	    #next char that follows substring in lyrics file
	    y[i, char_to_int[next_chars[i]]] = 1


	# print(X[1600][19][1])
	# print(y)

	#sequence classficiation with lstm 
	model = Sequential()
	model.add(LSTM(128, input_shape=(seq_length, chars_len)))
	model.add(Dropout(0.5))
	model.add(Dense(chars_len, activation='softmax'))

	optimizer = RMSprop(lr=0.01)
	model.compile(loss='categorical_crossentropy', optimizer=optimizer)


	#train model 
	for iteration in range(1, 5):
	    model.fit(x=X, y=y, batch_size=100, nb_epoch=10)


	    start = random.randint(0, len(lyrics_chars) - seq_length- 1)

	    sentence = lyric_chars[start: start + seq_length]

	    #get next char using model.predict
	    for i in range(1000):
	        x = np.zeros((1, seq_length, chars_len))
	        for t, char in enumerate(sentence):
	            x[0, t, char_to_int[char]] = 1.

	        pred = model.predict(x, verbose=0)[0]
	        next_index = sample(pred, 0.5)
	        next_char = int_to_char[next_index]

	        sentence = sentence[1:] + next_char

	        sys.stdout.write(next_char)
	        sys.stdout.flush()

	    print("next epoch")


def sample(preds, temperature):
	# https://github.com/llSourcell/keras_explained/blob/master/gentext.py
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)




if __name__ == '__main__':
    main()	
