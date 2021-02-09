import requests


for i in range(0,221):
	for j in range(0,10):
		for k in range (0,10):
			url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=' +str(i)+'.'+str(j)+str(k)+ '&tl=en&total=1&idx=0&textlen=9'
			r = requests.get(url, allow_redirects=True)

			open( str(i)+'.'+str(j)+str(k)+'.mp3', 'wb').write(r.content)
	print(i)

print ("end")