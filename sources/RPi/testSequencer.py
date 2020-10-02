

def testread_csv():
	df_idents={}
	f = open("idents.csv", "r")
	s = f.read().split("\n")
	for line in s[1:-1]:
		_idents = line.split(",")
		
		key = _idents[1]
		if key in df_idents:
			df_idents[key].append(_idents[0])
		else:	
			df_idents[key] = [_idents[0]]
	print(df_idents["448861"])
	f.close()

if __name__ == "__main__":
	#testFunction()
	#testIdents()
	testread_csv()
	#idents_pour("438132")