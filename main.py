global CONFIG,data,alphabet
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def ask(name,p,cL,s):
	if s=="True":
		setup = [__import__("inquirer").List(name,message=p,choices=cL),]
		response = __import__("inquirer").prompt(setup)
		return response["letter"]
	else:
		return input(p+": ")
# The CONFIG variable is where the configuration is hosted. The Variable "URL" is for the predefined json word URL, the "LIMIT" variable is a custom play controlled feature that cuts out words longer than the value ("":No Limit,Real Limit can go up to 100), the feature DEV is used to display information about the game's internal values which was used during bugtesting.


if __import__("os").path.isfile('config.json'):
	with open('config.json') as f:CONFIG=__import__("json").load(f)
	if type(CONFIG)==type({}):
		print("|--> CONFIG FILE INVALID - SWITCHING TO DEFAULT <--|") if len(list([x for x in ["FANCY","LIMIT","DEV"] if x not in CONFIG.keys()])) else print("Using Configuration File \"config.json\"")
		if "URL" not in CONFIG.keys():CONFIG["URL"]=""
else:CONFIG={"URL":"https://api.npoint.io/3e986e81d537efcb2863","LIMIT":"","DEV":"False","FANCY":"False"}

def urlget(p):return str(input(str(p)))
url = CONFIG["URL"] if CONFIG["URL"]!="" else urlget("URL: ")
if(url==CONFIG["URL"]):print(f"URL: {url}")





# Retrieve JSON and store it in variable "data"
with (__import__('urllib.request',fromlist=['request']).urlopen(str(url))) as response:data=(__import__("json").loads(response.read()))





# Generate List of Words That Are Less than Length "LIMIT" in CONFIG
def wordlistgen(lst):
	return(list([lst[c] for c in [i for i in range(len(lst)) if len(lst[i])<=[1000 if CONFIG["LIMIT"] not in range(100) else CONFIG["LIMIT"]][0]]]))





# Pick Random Word From the List
def wordgen(lst):
	return lst[__import__("random").randrange(0,len(lst))]





# Store Random Word
wordlist=wordlistgen(list(data["words"]))
global word
word=wordgen(wordlist)




# Parse Word Into Hangman Characters
def parseLetters(string):
	return list([string[c] for c in [i for i in range(len(string))]])





# Add to Dictionary
def addDict(lst,dct):
	dct={}
	for x in range(len(lst)):
		dct.update({int(x):str(lst[x])})
	return dct
wordletterlist=parseLetters(word)




# If In Dev Mode Paste Useful Info
if CONFIG["DEV"]=="True":
	print(f"Word: {word}\nLetters: {wordletterlist}")
dct=addDict(parseLetters(word),{})




# Verify that letter "ltr" is in dictionary "d"
def verifyLetter(d,ltr):
	return [x[0] for x in list([x if d[x].lower()==ltr.lower() else None] for x in range(len(d))) if x[0]!="_"]




# Return the Amount of times that letter "ltr" appeared in dictionary "d"
def returnInstances(d,ltr):
	print(f"There were exactly {len(verifyLetter(d,ltr))} Instances of the letter {ltr}")




# Main Function. Generates An Underscore for every single space, then replaces the underscores with the previous played letters (stored in ltrlist), however will only do so if the letter is not already played. It will then determine if the letter is incorrect, and will subtract a life from the player if that's the case. Then It will return the "din" directory (The Correct Inputs), the "dout" directory (The Inputs You have Submitted), the list "ltrlist" (A list of letters you have played) and the number "lives" (the number of lives you have left.)
def generateSpaces(din,dout,ltr,ltrlist,lives,charlist):
	print("\n")
	if lives==0:
		print("You are Dead!!")
		return [dout,din,ltrlist,lives]
	if ltr.lower() not in ltrlist:
		ltrlist.append(ltr.lower())
		for x in din.keys():
			if din[x]==ltr.lower():dout[x]=din[x]
			elif din[x] in ltrlist:dout[x]=din[x]
			else:dout[x]="_"
		if ltrlist[-1] not in din.values():lives-=1

	else:print("Letter Already Submitted")
	print(f"WORD: {combine(dout.values())}")
	if ltrlist != []:
		for x in range(len(ltrlist)):
			if ltrlist[x] in charlist:
				del(charlist[charlist.index(ltrlist[x])])
	return [dout,din,ltrlist,lives,charlist]




# This is a function that will combine a given list "lst" into a string of it's combined individual components ([a,b,c,_,_] -> [a b c _ _])
def combine(lst):return " ".join([str(x) for x in lst])




# The function that loops over itself until the user is either out of lives or has completed the word.
def guessLetter():
	ONGOING=True
	print(combine(list([("_") for x in range(len(word))]))+"\n")
	d_out,d_in,ltrlist,lives,charlist=generateSpaces(dct,{},ask("letter","Letter",alphabet,CONFIG["FANCY"]),[],9,alphabet)
	print(f"Lives Left: {lives}")
	
	while ONGOING==True:
		d_out,d_in,ltrlist,lives,charlist=generateSpaces(dct,d_out,ask("letter","Letter",charlist,CONFIG["FANCY"]),ltrlist,lives,charlist)
		print(f"Lives Left: {lives}")
		if lives<=0:
			print("You Lost!!")
			break
		elif d_out==d_in:
			print("You Won!")
			break

guessLetter()