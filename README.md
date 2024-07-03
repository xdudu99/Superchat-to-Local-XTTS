# Superchat-to-Local-XTTS
A simple integration between Streamelements and daswer123 xtts-api-server (coqui TTS) so it reads superchats on stream

You need to install xtts api server from https://github.com/daswer123/xtts-api-server

Using custom tts voices is possible, just need to load one (or finetune one easily with https://github.com/daswer123/xtts-finetune-webui) and replace the speaker.wav in the ttshandling.py

Highly recommend to install DeepSpeed, takes 1/3 of the time to process a tts request. Leave --lowvram on if your gpu has less than 8gb. (Not terribly necessary if you won't be running any other gpu intensive application, but if you want to run a not too demanding game at the same time, in my case CS2, you need spare VRAM)

I'll add a function to automatically change the used voice randomly or to check for a tag in the superchat msg so the sender can select the voice.
