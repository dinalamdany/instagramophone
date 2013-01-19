
from os 	import system
from sys 	import argv
from string import replace
import soundcloud

audio_change = ['reverse','short_echo','long_echo','fast','slow','glacial']


def do_all(audio_name):
	reverse(audio_name)
	short_echo(audio_name)
	long_echo(audio_name)
	fast(audio_name)
	slow(audio_name)
	glacial(audio_name)
	for effect in audio_change:
		effect = '/tmp/' + audio_name + '_' + effect + '.wav'
	return audio_change

def reverse(audio_name):
	command = './sox '+audio_name+'.wav '+audio_name+'_reverse.wav '
	command += 'reverse'
	system(command)

def short_echo(audio_name):
	command = './sox '+audio_name+'.wav '+audio_name+'_short_echo.wav '
	command += 'echo .8 .9 100 .8'
	system(command)

def long_echo(audio_name):
	command = './sox '+audio_name+'.wav '+audio_name+'_long_echo.wav '
	command += 'echo .8 .9 500 .8'
	system(command)

def fast(audio_name):
	command = './sox'+audio_name+'.wav '+audio_name+'_fast.wav '
	command += 'rate 1.2'
	system(command)

def slow(audio_name):
	command = './sox'+audio_name+'.wav '+audio_name+'_slow.wav '
	command += 'rate .8'
	system(command)

def glacial(audio_name):
	command = './sox'+audio_name+'.wav '+audio_name+'_glacial.wav '
	command += 'rate .5'
	system(command)
