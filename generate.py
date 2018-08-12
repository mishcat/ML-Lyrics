import argparse 


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type=str, required=True) 
	parser.add_argument('--model', type=str, default='LSTM')

	args = parser.parse_args()

	lyric_chars = open(args.file).read()
	lyrics_chars = lyric_chars.lower()

	chars = sorted(list(set(lyric_chars)))
	char_to_int = dict((c, i) for i, c in enumerate(chars))
	int_to_char = dict((i, c) for i, c in enumerate(chars))

	print(len(lyric_chars))
	print(lyric_chars)



if __name__ == '__main__':
    main()	
