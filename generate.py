import argparse 


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type=str, required=True) 
	parser.add_argument('--model', type=str, default='LSTM')

	args = parser.parse_args()

	lyric_chars = open(args.file).read()
	lyrics_chars = lyric_chars.lower()

	# chars = sorted(list(set(lyric_chars)))
	# char_to_int = dict((c, i) for i, c in enumerate(chars))
	# int_to_char = dict((i, c) for i, c in enumerate(chars))

	print(len(lyric_chars))
	print(lyric_chars)

	seq_length = 20
	lyrics = []
	next_chars = []

	for i in range(0,len(lyric_chars)-seq_length,1):
		lyrics.append(lyric_chars[i:i+seq_length])
		next_chars.append(lyric_chars[i+seq_length])

	print(lyrics)

	#number of cases it just looked at	
	print(len(lyrics))

if __name__ == '__main__':
    main()	
