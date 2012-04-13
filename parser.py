#!/usr/bin/python
import json
import re
import pickle
from os import path , mkdir

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

postFile = "sample_feed.txt"
stopWords = "stopWords.txt"
outputFile = "output.txt"
postHashFile = "hashFile.txt"
categoryFile = "categoryFile.dump"
MINLENGTH = 3
THRESHOLD = 1

if path.isfile(categoryFile):
	f5 = open(categoryFile,'r+')
	categories = pickle.load(f5)
else :
	categories = {
	'news' : {"cnn":1,"ibnlive":1,"news":1,"bbc":1,"fox":1,"newyork times":1,"washington posts":1,"wsj":1,"post":1,"breaking":1,"posts":1," news":1,"current":1,"affairs":1,"just now":1,"live":1,"tune in":1,"attack":1,"terror":1,"obama":1,"osama":1,"guardian":1,"hot":1,"wire":1,"revolt":1,"protest":1,"accuse":1,"times":1,"america":1,"india":1,"usa":1,"foreign":1,"minister":1,"open":1,"bowl":1,"minister":1,"scam":1,"plot":1,"science":1,"mathematician":1,"discovery":1,"research":1,"planet":1,"earth":1,"sun":1,"nature":1,"scientist":1,"death":1,"demise":1,"fire":1,"newspaper":1,"paper":1,"mashable":1,"tech":1,"history":1,"internet":1,"police":1,"econom":1,"business":1,"election":1,"democr":1,"republic":1,"govern":1,"govt":1,"career":1,"rape":1,"grammy":1,"academy":1,"sopa":1},
	'sports' : {"cricket":1,"nfl":1,"hockey":1,"roger federer":1,"andy murray":1,"djokovik":1,"nadal":1,"tennis":1,"football":1,"wpl":1,"nfl":1,"nba":1,"soccer":1,"ice hockey":1,"nole":1,"rafa":1,"rafael":1,"michael jordon":1,"league":1,"barcelona":1,"manchester":1,"viva":1,"vamos":1,"real madrid":1,"chelsea":1,"liverpool":1,"xavi":1,"iniesta":1,"argentina":1,"lance":1,"sachin tendulkar":1,"F1":1,"circuit":1,"polo":1,"golf":1,"stick":1,"sport":1,"coach":1,"athlete":1,"goal" : 1 ,"kick" : 1,"goalkeeper" : 1},
	'music' :{"music":1,"nirvana":1,"bob dylan":1,"the doors":1,"pink floyd":1,"eminem":1,"metallica":1,"coldplay":1,"enrique":1,"green day":1,"rahman":1,"linkin park":1,"michael jackson":1,"ozzy osbourne":1,"rock music":1,"u2":1," john mayer":1,"jay sean":1,"u2":1,"bruce springsteen":1,"slipknot":1,"robbie williams":1,"strings":1,"the beatles":1,"kesha":1,"david guetta":1,"justin beiber":1,"lady gaga":1,"pop":1,"rock":1,"jazz":1,"metal":1,"blues":1,"mix":1,"produced":1,"radio":1,"mashup":1,"dj":1,"classical":1,"band":1,"disco":1,"country":1,"guitar":1,"drum":1,"rap":1,"salsa":1,"folk":1,"rnb":1,"chachacha":1,"blues":1,"dance":1,"spotify":1,"turntable":1,"ipod":1,"itunes":1},
	'humor' : {"humor":1,"joke":1,"kidding":1,"haha":1,"lol":1,"jaja":1,"rofl":1,"lmfao":1,"funny":1,"lolmax":1,"hehe":1,"hihi":1,"laugh":1,"giggle":1,"wow":1,"bhak sala":1,"humour":1,"giggle":1,"giggle":1},
	'adventure' : {"trekking":1,"hiking":1,"sking":1,"skydiving":1,"hip hop":1,"maps":1,"places":1,"wow":1,"exciting":1,"bravo":1},
  'television' : {"that 70's show":1,"lost":1,"smallville":1,"prison break":1,"channel":1,"television":1,"bazinga":1,"the big bang theory how i met your mother":1," tbbt":1,"himym":1,"rome":1,"sparctus":1,"hollywood":1,"bollywood":1,"oscar":1,"awards":1,"golden":1,"grammy":1},
	'leisure' : {"sleeping":1,"coding":1,"novels":1,"novel":1,"book":1,"books":1,"cartoon":1,"painting":1,"hobby":1,"hobbies":1,"photography":1,"pics":1},
	'friends' : {"":1},
	'movies' : {"movie" : 1 , "movies" : 1, "titanic":1,"avatar":1,"imdb":1,"academy":1,"actor":1,"director":1,"brad pitt":1,"hugo":1,"moneyball":1,"angelina":1,"hollywood":1,"bollywood":1},
	'apps' : {"farmville":1,"poker":1,"angry birds":1,"smallville":1,"texas poker":1,"texas hold 'em":1,"zynga":1},
	'others' :{"":1}
	}

categoryList  = categories.keys()

numberCategories = len(categoryList)

checkWords = []

for category in categoryList:
	checkWords.append(categories[category].keys())

number_posts = 0

f1 = open(postFile,"r") 
f2 = open(stopWords,"r")
f3 = open(outputFile,"w")
f4 = open(postHashFile,"w")

combinedText = ""
#loading JSON from file and decoding it
text = str(f1.read())
JSON = json.loads(text)

JSON = eval(str(JSON['data']))

#reading stopwords
text2 = str(f2.read().split())
STOPWORDS = eval(text2)

if len(JSON) < 0 :
	print "JSON length < 0.. exiting"
	exit()

directory = str(JSON[0]['viewer_id'])
if not path.exists(directory):
	mkdir(directory, 0777)
fileHandler = []
for cat in categoryList:
	fileHandler.append(open(directory + '/' + str(cat)+".ssd","w"))

maintext =  ''
maintext2 = ''

for post in JSON:
	feed = ''

	if 'post_id' in post.keys():
		post_id = post['post_id']
	elif 'id' in post.keys():
		post_id = post['id']
	else :
		continue

	if 'description' in post.keys():
		if post['description'] is not None :
			feed = post['description'].lower()

	if 'message' in post.keys():
		if post['message'] is not None :
			feed = feed + ' ' + post['message'].lower()

	if 'link' in post.keys():
		if post['link'] is not None :
			feed = feed + ' ' + str(re.sub('[^a-zA-Z ]+',' ',post['link']))

	if 'attachment' in post.keys():
		if post['attachment'] is not None :
			print post['attachment']

	PlainText = re.sub('[^a-zA-Z ]+',' ',feed)
	PlainText = PlainText.split(' ')

	#cache implementation using dictionary to be done

	finalList = []
	for word in PlainText :
		if word not in STOPWORDS :
			finalList.append(word)
			if word not in finalList and word not in STOPWORDS and len(word) > 4:
				finalList.append(word)
	categoryScore = [0 for j in range(len(categoryList))]

	for word in finalList:
		for index in range(len(categoryList)):
			if word in checkWords[index] and is_ascii(word) and len(word) > 0:
				checkDict = categories[categoryList[index]]
				categoryScore[index] = categoryScore[index] + checkDict[word]

	if max(categoryScore) > THRESHOLD:
		maxValue = max(categoryScore)
		index = categoryScore.index(max(categoryScore))
		cat = categoryList[index]
		catDict = categories[cat]
		for word in finalList :
			if word in catDict.keys() and len(word) > MINLENGTH :
				catDict[word] = catDict[word] + 1
			else :
				catDict[word] = 1
		fileHandler[index].write(str(post_id) + '\n')
	else :
		fileHandler[categoryList.index('others')].write(str(post_id) + '\n')

#print categories
f5 = open("categoryFile",'w')
pickle.dump(categories,f5)
f5.close()
f1.close()
f2.close()
f3.close()
f4.close()
