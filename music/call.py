import requests


for i in range(51,100):
	url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=.' + str(i)+ '&tl=en&total=1&idx=0&textlen=9'
	r = requests.get(url, allow_redirects=True)

	open( 'p'+str(i)+'.mp3', 'wb').write(r.content)
	print(i)

print ("end")