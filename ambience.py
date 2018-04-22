#Ambience detection and Removal for audio
import os
import subprocess

class Videobject:
	#class for a video
	def __init__(self):
		print ("init")
		
	def return_wave_from_video(self,filename):
		self.filename = filename.split('.')[0]
		self.wav_filename = "%s%s" % (self.filename,".wav")
		exe_str = ['./ffmpeg','-i',filename,self.wav_filename]
		result = subprocess.check_output(exe_str)

		return (self.wav_filename)

	def detect_ambience(self,e,filename):
		exe_str =['auditok','-i',str(filename),'-e',str(e),'-o','detections/det_{N}.wav','--printf','{id}']
		print (exe_str)
		result = subprocess.check_output(exe_str)
		self.number_of_detections = int(result.split()[-1].decode())
	
	def compress_audio(self):
		#self.com_filename = "%s%s" % (self.filename,"compressed.wav")
		list_of_files = 'list_of_files'
		f = open(list_of_files,"w")
		for i in range(1,self.number_of_detections+1):
			f.write("file detections/det_"+str(i)+".wav"+"\n")	
		f.close()
		os.system('./ffmpeg -f concat -i list_of_files '+self.filename+'_final.wav')
		'''
		try:
			exe_str = ['./ffmpeg','-f','concat','-i',list_of_files,self.com_filename]
		except subprocess.CalledProcessError as e:
			raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
		result = subprocess.check_output(exe_str)
		'''

