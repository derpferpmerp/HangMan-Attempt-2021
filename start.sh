read -p "Do You Want A Config File? (Y|N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git clone "https://github.com/derpferpmerp/HangMan-Attempt-2021.git"&&cd "HangMan-Attempt-2021";sudo chmod 777 *;mv main.py ./HANGMAN.py;sudo pip3 install inquirer;echo "Run 'python3 ./HANGMAN.py' to Start";exit 1
fi
mkdir HANGMAN;cd HANGMAN;curl -o HANGMAN.py "https://raw.githubusercontent.com/derpferpmerp/HangMan-Attempt-2021/master/main.py"||wget -O HANGMAN.py "https://raw.githubusercontent.com/derpferpmerp/HangMan-Attempt-2021/master/main.py"||echo "Download Unsuccessful. Please Install wget or curl";exit 1
sudo pip3 install inquirer;echo "Run 'python3 HANGMAN.py' to Start or run 'viconf' to edit the config.json file";alias viconf "vi config.json"
