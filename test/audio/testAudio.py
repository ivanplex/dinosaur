"""
Unit Test for Audio Module


"""

from audio.audioHandler import AudioHandler

def test_Object_Creation():
	audioHandler = AudioHandler()
	assert audioHandler != None

def test_stream_creation():
	audioHandler = AudioHandler()
	assert audioHandler.getStream() != None


