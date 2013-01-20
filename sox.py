
from os 	import system
from sys 	import argv
from string import replace

audio_filter = ['reverse','short_echo','long_echo','fast','slow','glacial','satanic']

def do_all(random_id):
	audio_name = str(random_id)

	reverse(audio_name)
	short_echo(audio_name)
	long_echo(audio_name)		
	fast(audio_name)	
	slow(audio_name)		
	glacial(audio_name)
	satanic(audio_name)
	
	for effect in audio_filter:
		effect = '/tmp/' + audio_name + '_' + effect + '.wav'
	return audio_filter

def reverse(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'reverse','reverse')
	print command
	system(command)

def short_echo(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'short_echo','echo .8 .9 100 .8')
	print command
	system(command)

def long_echo(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'long_echo','echo .8 .9 500 .8')
	print command
	system(command)

def fast(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'fast','speed 1.2')
	print command
	system(command)

def slow(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'slow','speed .8')
	print command
	system(command)

def glacial(audio_name):
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'glacial','speed .5')
	print command
	print command
	system(command)

def satanic(audio_name):	# Just for Chris
	command = 'sox /tmp/{0}_original.wav /tmp/{0}_{1}.wav {2}'.format(audio_name,'satanic','reverse : speed .5')
	print command
	system(command)





