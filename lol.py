x   import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool
import subprocess
os.chdir('E://Projects/slac')
#with open("api-key.json") as f:
 #   GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
for filess in os.listdir("./data"):#for seeing all files in data
    if filess.endswith(".wav"):
        fname = filess#getting files from data
        completeName = 'E://Projects/slac/text/' + fname + ".txt"
        os.chdir('E://Projects/slac')
        pool = Pool(8)  # Number of concurrent threads
        subprocess.call(['ffmpeg', '-i', 'data/' + fname , '-f', 'segment' ,'-segment_time', '10' ,'-c' ,'copy' ,'parts/out%09d.wav'])
        r = sr.Recognizer()
        files = sorted(os.listdir('parts/'))

        def transcribe(data):#speech rec module
            idx, file = data
            name = "parts/" + file
            print(name + " started")
            # Load audio file
            with sr.AudioFile(name) as source:
                audio = r.record(source)
            # Transcribe audio file
            text = r.recognize_google(audio)
            print(name + " done")
            return {
                "idx": idx,
                "text": text
            }

        all_text = pool.map(transcribe, enumerate(files))
        pool.close()
        pool.join()

        transcript = ""#creating transcript
        for t in sorted(all_text, key=lambda x: x['idx']):
            total_seconds = t['idx'] * 30
            m, s = divmod(total_seconds, 60)
            h, m = divmod(m, 60)

            # Format time as h:m:s - 30 seconds of text
            transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t['text'])

        print(transcript)

        with open(completeName, "w") as f:#writing individual files
            f.write(transcript)

        os.chdir('E://Projects/slac/parts')
        for filename in os.listdir():#deleting from parts
            if filename.endswith('.wav'):
                os.unlink(filename)