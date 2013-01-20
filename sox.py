
from os 	import system
from sys 	import argv
from string import replace

audio_filter = ['reverse','short_echo','long_echo','fast','slow','glacial']

def do_all(random_id):
	audio_name = str(random_id)

	reverse(audio_name)
	short_echo(audio_name)
	long_echo(audio_name)		
	fast(audio_name)	
	slow(audio_name)		
	glacial(audio_name)	
	
	for effect in audio_filter:
		effect = '/tmp/' + audio_name + '_' + effect + '.wav'
	return audio_filter

# 'sox {}.wav /tmp/{}_{} {}'

def reverse(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_reverse.wav '
	command += 'reverse'
	#command = 'sox {}.wav /tmp/{}_{} {}'.format(audio_name,audio_name,)
	print command
	system(command)

def short_echo(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_short_echo.wav '
	command += 'echo .8 .9 100 .8'
	system(command)

def long_echo(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_long_echo.wav '
	command += 'echo .8 .9 500 .8'
	system(command)

def fast(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_fast.wav '
	command += 'speed 1.2'
	system(command)

def slow(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_slow.wav '
	command += 'speed .8'
	system(command)

def glacial(audio_name):
	command = 'sox /tmp/'+audio_name+'_original.wav /tmp/'+audio_name+'_glacial.wav '
	command += 'speed .5'
	system(command)
