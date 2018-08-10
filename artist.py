import argparse 


def main():
	print("hi")
	parser = argparse.ArgumentParser()
	parser.add_argument('--artist', type=str, required=True)
	args = parser.parse_args()
	print(args.artist)

if __name__ == '__main__':
    main()