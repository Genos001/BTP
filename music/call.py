import requests


for i in range(1,2):
	url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=.' +'cyan'+ '&tl=en&total=1&idx=0&textlen=9'
	r = requests.get(url, allow_redirects=True)

	open( 'cyan.mp3', 'wb').write(r.content)
	print(i)

print ("end")