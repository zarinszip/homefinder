import sys

def main():
	dict = {}
	args = sys.argv[1:]

	if len(args) == 0:
		return

	end_of_args = False
	for arg in args:
		if not end_of_args:
			match arg:
				case '--filter' | '-f':
						...
				case '--module':
					i = args.index('--module')
					module = args[i+1]
				case '--':
					end_of_args = True
		else:
			kv = arg.split('=')
			kv[1] = tuple(kv[1].split(':'))
			dict.update({kv[0] : kv[1]})

	print(dict)

if __name__ == '__main__':
	main()
