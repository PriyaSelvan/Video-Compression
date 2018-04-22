import argparse
from ambience import Videobject
from textrank import SrtObject
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Video Compression")
	parser.add_argument('--vi', type=str, default='input.mp4', help="Video required for compression in mp4 format")
	parser.add_argument('--ti', type=str, default='input.srt', help="SRT file of lecture video in srt format")
	parser.add_argument('--c', type=float, default='0.5', help="Rate of Compression")
	args = parser.parse_args()
	video_file = args.vi
	srt_file = args.ti
	compression_rate = args.c

	lecture = Videobject()
	audio_file = lecture.return_wave_from_video(video_file)
	lecture_srt = SrtObject(srt_file)
	lecture_srt.compressSentences(audio_file,compression_rate)
	op1_audio_name = 'textrank_detections/cutoff'+audio_file
	print (op1_audio_name)
	lecture.detect_ambience(50,op1_audio_name)
	lecture.compress_audio()
	print ("Finished!")

