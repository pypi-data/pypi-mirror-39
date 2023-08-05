import argparse

clap = u"\U0001F44F"
parser = argparse.ArgumentParser(description='CLAP BACK')
parser.add_argument('words', type=str, nargs='+') 
parser.add_argument('--louder', '-l', action="store_true")

def clapBack(input):
	wordlist = []
	for word in input:
		wordlist.append((clap, word))
	wordlist = [x for t in wordlist for x in t]
	print( ' '.join(word for word in wordlist))

def louder(input):
	args.words = [x.upper() for x in args.words]
	clapBack(args.words)

args = parser.parse_args()

if args.louder:
	louder(args.words)

else:
	clapBack(args.words)
