from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import pysrt
import io
import nltk
import itertools
from operator import itemgetter
import networkx as nx
import numpy as np
from nltk.tokenize.punkt import PunktSentenceTokenizer
#from sklearn.feature_extraction.text import TfidfTrachecklistformer, CountVectorizer
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer
from pydub import AudioSegment
import operator
import sys
import argparse
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
class SrtObject:
	def __init__(self,filename):
		subs = pysrt.open(filename)
		number = 0	
		self.finalList = []	
		#get start time of the trachecklistcript
		start=str(subs[0].start.hours)+':'+str(subs[0].start.minutes)+":"+str(subs[0].start.seconds)
		print (start)
		print (len(subs))
		subsentence = open('textrank_detections/subsentence.txt','w')
		timestamp=open("textrank_detections/timestamp.txt",'w')
		
		
		temptext = ''
		for i in range(0,len(subs)):
			temptext+=' '+subs[i].text.replace('\n',' ')
			if((temptext.endswith('.') or temptext.endswith('!') or temptext.endswith('?')) and i<len(subs)-1):
				number+=1
				sentenceList=[]
				end=str(subs[i+1].start.hours)+':'+str(subs[i+1].start.minutes)+":"+str(subs[i+1].start.seconds)
				sentenceList.append(temptext)
				sentenceList.append(start)
				sentenceList.append(end)
				subsentence.write(temptext)
				subsentence.write('\n')
				timestamp.write(str(number))
				timestamp.write('\t'+temptext)
				timestamp.write('\t'+start+'\t'+end)
				timestamp.write('\n')
				self.finalList.append(sentenceList)
				start=end
				temptext=''
			elif i==len(subs)-1:
				number+=1
				sentenceList=[]
				end=str(subs[i].end.hours)+':'+str(subs[i].end.minutes)+":"+str(subs[i].end.seconds)
				sentenceList.append(temptext)
				sentenceList.append(start)
				sentenceList.append(end)
				subsentence.write(temptext)
				subsentence.write('\n')
				timestamp.write(str(number))
				timestamp.write('\t'+temptext)
				timestamp.write('\t'+start+'\t'+end)
				timestamp.write('\n')
				self.finalList.append(sentenceList)
		subsentence.close()
		timestamp.close()
	def compressSentences(self,checklist):
		samt = 250
		ranks=open("textrank_detections/RankedSentences.txt",'w')
		sentence=open("textrank_detections/sentenceList.txt","w")

		start=self.finalList[0][1].split(':')
		end=self.finalList[len(self.finalList)-1][2].split(':')
		tstart=((int(start[0]*60)+int(start[1]))*60+int(start[2]))*1000
		tend=((int(end[0]*60)+int(end[1]))*60+int(end[2]))*1000
		totalDuration=tend-tstart
		elapsedTime=0
		outword=''
		ultimateList=[]
		parser = PlaintextParser.from_file('textrank_detections/subsentence.txt', Tokenizer('english'))
		summarizer=TextRankSummarizer()
		#silence=AudioSegment.silent(duration=samt)
		#audio = AudioSegment.from_wav(filename)
		scoreList=[]

		summary=summarizer.rate_sentences(parser.document)
		templist=[]
		for k in summary.items():
    			templist.append(k[0])
    			templist.append(k[1])
    			scoreList.append(templist)
    			templist=[]
		scoreList=sorted(scoreList,key=lambda l:l[1], reverse=True)
		for s in scoreList:
    			for x in self.finalList:
        			if(s[0]._text in x[0]):
            				start=x[1].split(':')
            				end=x[2].split(':')
            				starttime=((int(start[0]*60)+int(start[1]))*60+int(start[2]))*1000
            				endtime=((int(end[0]*60)+int(end[1]))*60+int(end[2]))*1000
            				elapsedTime+=(endtime-starttime)
            				ranks.write("num: "+str(self.finalList.index(x)+1)+"\tscore: "+str(s[1])+"\telapsedTime: "+str(elapsedTime))
            				ranks.write("\n")
            				break
		ranks.close()

		#out5=open("textrank_detections/segment_file_"+str(checklist)+".txt",'w')
		#out7=open("textrank_detections/segment_file_notext_"+str(checklist)+".txt",'w')
		ultimateList=[]
		timeSortedUltimateList=[]
		audiolist=[]
		previousEnd=-999
		duration=totalDuration*checklist
		for s in scoreList:
			for x in self.finalList:
				if(s[0]._text in x[0] and duration>0):
					templist=[]
					start=x[1].split(':')
					end=x[2].split(':')
					starttime=((int(start[0]*60)+int(start[1]))*60+int(start[2]))*1000
					endtime=((int(end[0]*60)+int(end[1]))*60+int(end[2]))*1000
					duration = duration - (endtime-starttime)						
					templist.append(x[0])
					templist.append(starttime)
					templist.append(endtime)
					templist.append(s[1])
					ultimateList.append(templist)
		timeSortedUltimateList=sorted(ultimateList,key=lambda l:l[1], reverse=False)
		if(checklist==0.7):
			print("true")
			for k in timeSortedUltimateList:
				for x in finalList:
					if(k[0] in x[0]):
						sentence.write(str(finalList.index(x)+1)+"\t"+str(k[3])+"\n")
		sentence.close()


		print("r: "+str(checklist)+"\tTextRank no. of sentences: "+str(len(timeSortedUltimateList)))
		num=1
		info=''
		st=timeSortedUltimateList[0][1]
		en=0
		self.starts = list()
		self.ends = list()
		for k in timeSortedUltimateList:
			if(not(k[1]==previousEnd) and previousEnd!=-999):
				#audiolist.append(silence)
				#audiolist.append(audio[k[1]:k[2]])
				en=previousEnd
				#out5.write("seg "+str(num)+":"+info+"\t"+str(st)+"\t"+str(en))
				self.starts.append(st)
				self.ends.append(en)
				#out5.write("\n\n")
				#out7.write("seg "+str(num)+":\t"+str(st)+"\t"+str(en))
				#out7.write("\n\n")
				st=k[1]
				num+=1
				info=''
				info+=k[0]

			else:
				#audiolist.append(audio[k[1]:k[2]])
				info+=k[0]
			previousEnd=k[2]
		#finalaudio = audiolist[0]
		#for a in range(1,len(audiolist)):
			#finalaudio = finalaudio + audiolist[a]
		#finalaudio.export("textrank_detections/cutoff"+filename, format="wav")


		#out5.close()
		#out7.close()

	def makeFinalVideo(self,filename):
		starts = [i/1000 for i in self.starts]
		ends = [i/1000 for i in self.ends]
		frame = ""
		inter = ""
		concat_str = "concat:"
		for i in range(len(starts)):
			frame = "video_detections/"+str(i)+"final.mp4"
			inter = "video_detections/"+str(i)+"inter.ts"
			ffmpeg_extract_subclip(filename, starts[i], ends[i], targetname=frame)
			os.system("ffmpeg -i "+frame+" -c copy -bsf:v h264_mp4toannexb -f mpegts "+inter)
			concat_str = concat_str + inter + "|"
		concat = concat_str[:-1]
		concat = '"'+concat+'"'
		os.system("ffmpeg -i "+concat+" -c copy -bsf:a aac_adtstoasc dragon.mp4")
		
	
		


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Text Rank optiochecklist")
	parser.add_argument('--i', type=str, default='input.srt', help="Input trachecklistcript file for textrank")
	parser.add_argument('--v', type=str, default='input.mp4', help="Input video file")

	parser.add_argument('--scale', type=float, default=0.5, help="Rate of the new audio after textrank")        
	args = parser.parse_args()
	lecture1 = SrtObject(args.i)
	lecture1.compressSentences(args.scale)
	lecture1.makeFinalVideo(args.v)
	
        
	

