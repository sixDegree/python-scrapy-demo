import re
import os
import json

# f=open('./getMocTermDto.js','r',encoding='utf-8')
# result=f.read()
# f.close()
#print(result)

# 贪婪匹配 -- 默认
# ls=re.findall(r's\d+\.\w+=.*;',result)
# for i in ls:
# 	item=i.encode('utf-8').decode('unicode_escape')
# 	#print(item)
# 	props=re.split(r's\d+.',item)
# 	print(props)

# 最小匹配
# 最小匹配操作符：`*?`,`+?`,`??`,`{m,n}?`
# ls=re.findall(r's\d+\.\w+=.*?;',result)
# for i in ls:
# 	item=i.encode('utf-8').decode('unicode_escape')
# 	props=re.split(r'\.|=|;',item)
# 	print(props)


def parse_lesson():
	f=open('./getMocTermDto.js','r',encoding='utf-8')
	result=f.read()
	f.close()

	ls=re.findall(r's\d+\.\w+=.*;',result)
	lsMap={}
	my_type=""
	for index,i in enumerate(ls):
		if index>=3:
			break;

		item=i.encode('utf-8').decode('unicode_escape')

		if item.find("lessons")!=-1 or item.find("units")!=-1:
			my_type="lesson"
		else:
			my_type="material"

		props=re.split(r's\d+.',item)
		#props=re.findall(r's\d+\.\w+=.*?;',item)
		#props=re.split(r';s\d+.',item)
		record={"my_type":my_type}
		#print(props)
		for p in props:
			if not p:
				continue
			results=re.split(r'=|;',p)
			#print('results',results)
			if results[1]!='null' and results[1]!='':
				record[results[0]]=results[1]
				# print(results[0],results[1])
		print(my_type,record)
		key=record.get('id')
		if key:
			lsMap[key]=record	#lsMap[key].update(record)

	#print(lsMap)
	i=1
	for k,v in lsMap.items():
		if v.get('chapterId'):
			chapter=lsMap.get(v['chapterId'])
			v['chapter_name']=chapter['name']
		if v.get('lessonId'):
			lesson=lsMap.get(v['lessonId'])
			v['lesson_name']=lesson['name']
		if v.get('contentType')=='2' and v.get('contentId'):
			exam_record=lsMap.get(v['contentId'])
			exam_record['chapterId']=v.get('chapterId')
			exam_record['lessonId']=v.get('lessonId')
			lsMap[exam_record['id']].update(exam_record)
		print(i,k,v)
		i+=1

	# s39.id=1212471890;
	# s39.chapterId=1209097098;
	# s39.contentType=1;
	# s39.contentId=1005857411;	*
	# s39.lessonId=1210422476;	*

	# s39.name="5.\u4F8B\u9898\uFF1A\u7184\u706F\u95EE\u9898(2)";
	# s39.position=4;
	# s39.termId=1205957211;

	# s39.durationInSeconds=1317;
	# s39.freePreview=0;
	# s39.gmtCreate=1548990674642;
	# s39.gmtModified=1548990674642;
	
	# ---- 

	# s27.id=1210422476;
	# s27.chapterId=1209097098;
	# s27.contentType=1;

	# s27.name="5. \u4F8B\u9898\uFF1A\u7184\u706F\u95EE\u9898(2)";
	# s27.position=4;
	# s27.termId=1205957211;

	# s27.gmtCreate=1548990674634;
	# s27.gmtModified=1548990674634;
	# s27.isTestChecked=false;
	# s27.releaseTime=1550444400000;
	# s27.testDraftStatus=0;
	# s27.units=s38;

def parse_doc():
	f=open('./getLessonUnitLearnVo(doc).js','r',encoding='utf-8')
	result=f.read()
	f.close()

	record={}
	ls=re.findall(r'(textOrigUrl|textUrl):"(http.*?)"',result)
	for item in ls:
		print(item)
		record[item[0]]=item[1]
	print(record)

def parse_video():
	f=open('./getLessonUnitLearnVo(video).js','r',encoding='utf-8')
	result=f.read()
	f.close()

	record={}
	ls=re.findall(r's\d+\.\w+=.*?;',result)
	for item in ls:
		prop=re.split(r's\d+\.|;',item,maxsplit=2)[1]
		#pairs=prop.split('=',1)
		pairs=re.split(r'=|\?',prop)
		print(pairs)
		if len(pairs)>=2 and pairs[1]!='null' and pairs[1]!='':
			record[pairs[0]]=pairs[1].replace('"','')

	print(record)
		
def parse_attachment():
	content='"{\"nosKey\":\"E10AD03432E2BE51B2640F88BA83C191-1515898079229\",\"fileName\":\"week9.zip\"}"'
	content=content.strip('"')
	record=json.loads(content)
	print(record)
	url="https://www.icourse163.org/course/attachment.htm?fileName="+record['fileName']+"&nosKey="+record['nosKey']
	print(url)

	props=re.split(r'\?|\&',url)
	print(props)

if __name__=='__main__':
	# parse_lesson()
	parse_doc()
	# parse_video()
	# parse_attachment()



# dict: http://www.cnblogs.com/whatisfantasy/p/5956761.html
# unicode: https://www.cnblogs.com/technologylife/p/6071787.html

