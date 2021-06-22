import inquirer
import json
import os
import urllib.request as uget
import random
import requests

global CONFIG
global data
global alphabet
global word

alphabet = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def ask(name, p, cL, s):
    if s == "True":
        setup = [
            inquirer.List(name, message=p, choices=cL),
        ]
        response = inquirer.prompt(setup)
        return response["letter"]
    else:
        return input(p + ": ")


# The CONFIG variable is where the configuration is hosted. The Variable "URL" is for the predefined json word URL, the "LIMIT" variable is a custom play controlled feature that cuts out words longer than the value ("":No Limit,Real Limit can go up to 100), the feature DEV is used to display information about the game's internal values which was used during bugtesting.

if os.path.isfile("config.json"):
    with open("config.json") as f:
        CONFIG = json.load(f)
    if type(CONFIG) == type({}):
        print("|--> CONFIG FILE INVALID - SWITCHING TO DEFAULT <--|") if len([
            x for x in ["FANCY", "LIMIT", "DEV", "SCRABBLE-LIMIT"]
            if x not in CONFIG.keys()
        ], ) else print('Using Configuration File "config.json"')
        if "URL" not in CONFIG.keys():
            CONFIG["URL"] = ""
else:
    CONFIG = {
        "URL": "https://api.npoint.io/3e986e81d537efcb2863",
        "LIMIT": "",
        "DEV": "False",
        "FANCY": "False",
        "SCRABBLE-LIMIT": "",
    }


def urlget(p):
    return str(input(str(p)))

if CONFIG["URL"] == "":
	url = urlget("URL: ")
else:
	url = CONFIG["URL"]
	print(f"URL: {url}")


def scrabble(wordlist):
    scrabbledict = {
        "a": 1,
        "b": 3,
        "c": 3,
        "d": 2,
        "e": 1,
        "f": 4,
        "g": 2,
        "h": 4,
        "i": 1,
        "j": 8,
        "k": 5,
        "l": 1,
        "m": 3,
        "n": 1,
        "o": 1,
        "p": 3,
        "q": 10,
        "r": 1,
        "s": 1,
        "t": 1,
        "u": 1,
        "v": 4,
        "w": 4,
        "x": 8,
        "y": 4,
        "z": 10,
    }
    lst = []
				if CONFIG["SCRABBLE-LIMIT"] == "":
					lim = 1000
				else:
					lim = int(CONFIG["SCRABBLE-LIMIT"])
    
    for wrd in wordlist:
        totalval = 0
								lettervalues = []
								for x in [wrd[c] for c in [i for i in range(len(wrd))]]:
									if x in scrabbledict.keys():
										lettervalues.append(scrabbledict[x])
										
        for points in lettervalues:
            totalval += int(points)
        if totalval <= lim:
            lst.append(wrd)
    return lst


# Retrieve JSON and store it in variable "data"
with (uget.urlopen(str(url))) as response:
    data = json.loads(response.read())


# Generate List of Words That Are Less than Length "LIMIT" in CONFIG
def wordlistgen(lst):
    return [
        x for x in [
            lst[c] for c in [
                i for i in range(len(lst)) if len(lst[i]) <= [
                    1000 if CONFIG["LIMIT"] not in
                    range(100) else CONFIG["LIMIT"]
                ][0]
            ]
        ] if len(x) >= [int(CONFIG["MIN"]) if (CONFIG["MIN"] != "") else 0][0]
    ]


# Pick Random Word From the List
def wordgen(lst):
    return lst[random.randrange(0, len(lst))]


# Store Random Word
wordlist = wordlistgen(list(data["words"]))
wordlist = scrabble(wordlist)
word = wordgen(wordlist)


# Parse Word Into Hangman Characters
def parseLetters(string):
    return [string[c] for c in [i for i in range(len(string))]]


# Add to Dictionary
def addDict(lst, dct):
    dct = {}
    for x in range(len(lst)):
        dct.update({int(x): str(lst[x])})
    return dct


wordletterlist = parseLetters(word)

# If In Dev Mode Paste Useful Info
if CONFIG["DEV"] == "True":
    print(f"Word: {word}\nLetters: {wordletterlist}")
dct = addDict(parseLetters(word), {})


# Verify that letter "ltr" is in dictionary "d"
def verifyLetter(d, ltr):
    return [
        x[0] for x in [[x if d[x].lower() == ltr.lower() else None]
                       for x in range(len(d))] if x[0] != "_"
    ]


# Return the Amount of times that letter "ltr" appeared in dictionary "d"
def returnInstances(d, ltr):
    print(
        f"There were exactly {len(verifyLetter(d,ltr))} Instances of the letter {ltr}",
    )


def bold(txt):
    return f"\033[1m{txt}\033[0m"


# Main Function. Generates An Underscore for every single space, then replaces the underscores with the previous played letters (stored in ltrlist), however will only do so if the letter is not already played. It will then determine if the letter is incorrect, and will subtract a life from the player if that's the case. Then It will return the "din" directory (The Correct Inputs), the "dout" directory (The Inputs You have Submitted), the list "ltrlist" (A list of letters you have played) and the number "lives" (the number of lives you have left.)
def generateSpaces(din, dout, ltr, ltrlist, lives, charlist):
    print("\n")
    if lives == 0:
        print("You are Dead!!")
        return [dout, din, ltrlist, lives]
    if ltr.lower() not in ltrlist:
        ltrlist.append(ltr.lower())
        for x in din.keys():
            if din[x] == ltr.lower():
                dout[x] = din[x]
            elif din[x] in ltrlist:
                dout[x] = din[x]
            else:
                dout[x] = "_"
        if ltrlist[-1] not in din.values():
            lives -= 1

    else:
        print("Letter Already Submitted")
    print(f"WORD: {combine(dout.values())}")
    if ltrlist != []:
        for x in range(len(ltrlist)):
            if ltrlist[x] in charlist:
                del charlist[charlist.index(ltrlist[x])]
    return [dout, din, ltrlist, lives, charlist]


# This is a function that will combine a given list "lst" into a string of it's combined individual components ([a,b,c,_,_] -> [a b c _ _])
def combine(lst):
    return " ".join([str(x) for x in lst])


def getdefinition(wrd):
    definitionlist = []
    [
        definitionlist.append(possible)
        for possible in (requests.get(
            f"http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_{wrd[0].lower()}.html",
        ).text).split("\n")
        if f"<P><B>{wrd.lower()[0].upper()}{wrd.lower()[1:len(wrd)]}</B>" in
        possible
    ]
    if len(definitionlist) == 0:
        return "(No Valid Definition Found)"
    else:
        return f"\n{bold(((((definitionlist[0].replace('<P><B>','')).replace('</B> ',' ')).replace('<I>','')).replace('</I>','')).replace('</P>','').split(')')[0])}{bold(')')}{((((definitionlist[0].replace('<P><B>','')).replace('</B> ',' ')).replace('<I>','')).replace('</I>','')).replace('</P>','').split(')')[1]}"


# The function that loops over itself until the user is either out of lives or has completed the word.
def guessLetter():
    ONGOING = True
    print(combine([("_") for x in range(len(word))]) + "\n")
    d_out, d_in, ltrlist, lives, charlist = generateSpaces(
        dct,
        {},
        ask("letter", "Letter", alphabet, CONFIG["FANCY"]),
        [],
        9,
        alphabet,
    )
    print(f"Lives Left: {lives}")

    while ONGOING == True:
        d_out, d_in, ltrlist, lives, charlist = generateSpaces(
            dct,
            d_out,
            ask("letter", "Letter", charlist, CONFIG["FANCY"]),
            ltrlist,
            lives,
            charlist,
        )
        print(f"Lives Left: {lives}")
        if lives <= 0:
            print("You Lost!!")
            break
        elif d_out == d_in:
            print("You Won!")
            print(getdefinition(word))
            break


guessLetter()
