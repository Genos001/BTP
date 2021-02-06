# import requests


# for i in range(51,100):
# 	url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=.' + str(i)+ '&tl=en&total=1&idx=0&textlen=9'
# 	r = requests.get(url, allow_redirects=True)

# 	open( 'p'+str(i)+'.mp3', 'wb').write(r.content)
# 	print(i)

# print ("end")

import librosa  # just to demo, not necessary, as you already have the data
import soundfile

# read some wave file, so that y is the date and sr the sample rate
y, sr = librosa.load('red.wav')

# write to a new wave file with sample rate sr and format 'unsigned 8bit'
soundfile.write('your.wav', y, sr, subtype='PCM_U8')