# This is Hangman - Coded By Derp

> # How To Install
The Easiest Way to Install Is By Using the Start Script, Which Can Be Installed Like This:
```console
curl -O "https://raw.githubusercontent.com/derpferpmerp/HangMan-Attempt-2021/master/start.sh";./start.sh
```
You Could Also Clone The Repository and Import The Packages Yourself (Although this is just what the start script does):
```console
git clone "https://github.com/derpferpmerp/HangMan-Attempt-2021.git";mv main.py ./HANGMAN.py;sudo pip3 install inquirer
```

Although You Can Do the Second Option, I highly reccomend the first option, as I have coded in some safety measures (IE not having packages,
not having curl or wget, etc. etc.)

Upon Installation You will have the option to create a config.json file. If you do not create the json file, you can always create it later
with this command (make sure you are in the directory of the project):
```sh
curl -O "https://raw.githubusercontent.com/derpferpmerp/HangMan-Attempt-2021/master/config.json"||wget -o config.json "https://raw.githubusercontent.com/derpferpmerp/HangMan-Attempt-2021/master/config.json"||touch config.json;echo "There Was An Error, Please Look at the Github to Manually Create the Json File"
```
If the command fails, it will automatically create the file and print an error. If so, and also for potential bugfixing, The Config.Json should have this structure:
```json
{
	"URL": "https://api.npoint.io/3e986e81d537efcb2863",
	"LIMIT": "",
	"DEV": "True",
	"FANCY": "True"
}
```
```yaml
:EXPLANATION:
:URL : "The URL For the Json Word List",
:LIMIT : "The Maximum Character Limit (No words more than x characters long)",
:DEV : "Shows Troubleshooting Info (Pretty Much Cheating)",
:FANCY : "Turns on the Inquirer Library, which creates a scrollable options list, if set to "False", you will type in inputs manually, but be warned that although you cannot type the same character twice, you will get docked for typing more than one character."
```
The Moment you launch the program it should tell you whether or not your configuration is valid (and will be used), invalid (Will switch over to default config), or not there at all (Will Switch Over to default config).

# Have Fun!
