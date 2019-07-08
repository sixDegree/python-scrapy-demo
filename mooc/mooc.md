mooc

1. Course List:

db.course.find({"category_name":"计算机"}).count()
db.course.find({"category_name":"计算机",name:/分析/}).count()

db.course.find({"category_name":"计算机",name:/分析/}
,{'name':1,'school.name':1,'school.short_name':1,'lector':{$slice:1},'term.id':1
})

db.course.find({"category_name":"计算机",name:/分析/}
,{'name':1,'school.name':1,'school.short_name':1,'lector':{$slice:1},'lector.realName':1,'lector.lectorTitle':1,'term.id':1
})

db.course.aggregate([
	{$match:{
		"category_name":"计算机",name:/分析/
	}}
	,{$project:{
		'name':1
		,'school':"$school.name"
		,'code':"$school.short_name"
		,'lector':{ $arrayElemAt: [ "$lector.realName", 0 ] }
		,'title':{ $arrayElemAt: [ "$lector.lectorTitle", 0 ] }
		,'termId':"$term.id"
	}}
])

,'lector':"$lector.realName"


db.course.aggregate([
	{$match:{
		"category_name":"计算机",name:/分析/
	}}
	,{$project:{
		'name':1
		,'school':{ $concat:[ "$school.name"," ","$school.short_name"] }
		,'lector':{ $concat:[
			{ $arrayElemAt: [ "$lector.realName", 0 ] }
			," "
			,{ $arrayElemAt: [ "$lector.lectorTitle", 0 ] }
		]}
		,'termId':"$term.id"
	}}
])

db.course.aggregate([
	{$match:{
		name:/大数据/
	}}
	,{$project:{
		'name':1
		,'school':{ $concat:[ "$school.name"," ","$school.short_name"] }
		,'lector':{ $concat:[
			{ $arrayElemAt: [ "$lector.realName", 0 ] }
			," "
			,{ $arrayElemAt: [ "$lector.lectorTitle", 0 ] }
		]}
		,'termId':"$term.id"
		,'tag':{$arrayElemAt:["$tag.name",0]}
		,'enroll':"$term.enroll_count"
		,'crawl':"$lesson_crawl"
		,'uri':{ $concat:[
			"/learn/"
			,"$school.short_name"
			,"-"
			,{$toString:"$_id"}
			,"?tid="
			,{$toString:"$term.id"}
			,"#/learn/content"
		]}
	}}
])


1205806833 商务数据分析 FUDAN 复旦大学 赵卫东 副教授	1206096296

https://www.icourse163.org/learn/FUDAN-{_id}?tid={term.id}#/learn/content
https://www.icourse163.org/learn/FUDAN-1205806833?tid=1206096296#/learn/content


2. Lesson crawl by course:

db.course.find({'lesson_crawl':'Done'}).count()
db.course.find({'lesson_crawl':{$ne:'Done'}}).count()

db.course.updateMany({},{$set:{'lesson_crawl':''}})

db.course.updateMany({
	_id:1001894005
},{
	$set:{'lesson_crawl':''}
})



3. Material:

contentType:
	1-video
	2-exam(db.lesson)
	3-doc
	4-attachment
	5-test
	6-chat

db.material.find({course_id:1205806833,contentId:{$exists:true}}).pretty()

db.material.aggregate([
	{$match:{
		course_id:1205806833
		,contentId:{$exists:true}
	}}
	,{$group:{
		_id:"$contentType"
		,count:{$sum:1}
		,done:{$sum:{
			$cond:[{$eq:["$material_crawl","Done"]},1,0]
		}}
		,fail:{$sum:{
			$cond:[{$eq:["$material_crawl","Fail"]},1,0]
		}}
	}}
])

db.material.find({
	contentId:{$exists:true}
	,course_id:1001894005
},{
	'_id':1,'contentId':1
	,'contentType':1
	,'chapter_name':1
	,'name':1
	,'position':1
}).sort({'chapterId':1,'position':1})


-- find:

db.material.find({
	contentId:{$exists:true}
	,course_id:1001894005
}).sort({'chapterId':1,'position':1}).pretty()

db.material.find({
	contentId:{$exists:false}
	,course_id:1001894005
}).sort({'chapterId':1,'position':1})


db.material.find({
	course_id:1001894005
	,contentId:{$exists:true}
	,'material_crawl':{$ne:'Done'}
}).pretty()

db.material.find({
	contentId:{$exists:true}
	,course_id:1001755117
	,contentType:4
}).sort({'chapterId':1,'position':1}).pretty()

-- update:

db.material.updateMany({
	'material_crawl':'Done'
},{
	$set:{'material_crawl':''}
})

db.material.updateMany({
	'material_crawl':'Done'
	,'contentType':1
},{
	$set:{'material_crawl':''}
})

db.material.updateMany({
	'material_crawl':'Done'
	,'course_id':1002335004
},{
	$set:{'material_crawl':''}
})

db.material.updateMany({
	contentId:{$exists:true}
	,course_id:1001894005
	,contentType:4
},{
	$unset:{resource_url:true}
})


==================================

Search

POST https://www.icourse163.org/web/j/mocSearchBean.searchMocCourse.rpc

csrfKey: e8c25a05689c41ceae46266ee393e68c

formData:
query:{"keyword":"python","pageIndex":1,"highlight":true,"orderBy":0,"stats":30,"pageSize":20,"courseTagType":1}

query: {"keyword":"python","pageIndex":1,"highlight":true,"orderBy":0,"stats":10,"pageSize":20,"courseTagType":1}

stats: 
	30 -- All
	10 -- going
	20 -- next
	0 -- finished


Response:
{
	code: 0
	message: ""
	result: {
		categories: [
			{
				children: null
				courseCout: 20
				iconUrl: "http://img2.ph.126.net/t82u8eaQzZfmAXrKUrNUiQ==/2435884448472057908.png"
				id: -1
				linkName: null
				mobCoverIcon: null
				mobIcon: null
				name: "全部课程"
				parentId: null
				type: null
				webIcon: null
				weight: null
			}
			{
				children: null
				courseCout: 168
				iconUrl: "http://img2.ph.126.net/FtS9B4h7fszp1ogQY57Qrw==/6630414655791978284.png"
				id: 7001
				linkName: null
				mobCoverIcon: null
				mobIcon: null
				name: "文学艺术"
				parentId: null
				type: 1
				webIcon: null
				weight: null
			}
			3: {id: 8002, name: "经管法学", type: 1, courseCout: 1,…}
			4: {id: 8003, name: "基础科学", type: 1, courseCout: 642,…}
			5: {id: 2001, name: "工程技术", type: 1, courseCout: 12,…}
			6: {id: 8004, name: "农林医药", type: 1, courseCout: 56,…}
		]
		pagination: {
			DEFAULT_OFFSET: 0
			DEFAULT_PAGE_INDEX: 1
			DEFAULT_PAGE_SIZE: 10
			DEFAULT_TOTLE_COUNT: 0
			DEFAULT_TOTLE_PAGE_COUNT: 1
			limit: 20
			offset: 0
			pageIndex: 1
			pageSize: 20
			sortCriterial: null
			totleCount: 13
			totlePageCount: 1
		}
		result: [
			{
				cid: 268001
				highlightBgKnowledge: null
				highlightContent: "spContent=计算机是运算工具，更是创新平台，高效有趣地利用计算机需要更简洁实用的编程语言。{##Python##}简洁却强大、简单却专业，它是当今世界最受欢迎的编程语言，学好它终身受用。请跟随我们，学习并掌握{##Python##}语言，一起动起来，站在风口、享受创新！"
				highlightDescription: null
				highlightFaq: null
				highlightName: "{##Python##}语言程序设计"
				highlightOutline: null
				highlightRecommendRead: null
				highlightRequirements: null
				highlightSpContent: null
				highlightTeacherNames: "嵩天;礼欣;黄天羽;"
				highlightUniversity: "北京理工大学"
				mocCourseCardDto: {
					VideoUrl: "nos/mp4/2015/08/28/2065044_sd.mp4"
					allTerms: null
					applyConvertChannelStatus: 0
					applyMoocStatus: 0
					channel: 1
					classroomSupport: null
					courseType: 1
					currentTermChargeable: 0
					currentTermId: 1206073223
					firstPublishTime: 0
					fromCourseId: null
					fromCourseMode: -1
					fromCourseName: null
					fromCourseSchoolName: null
					gmtCreate: 1430802567336
					id: 268001
					imgUrl: "http://edu-image.nosdn.127.net/5B8826377EE623C7B6328E8F8B8D2871.png?imageView&thumbnail=510y288&quality=100"
					lastLearningTime: null
					learnedCount: null
					learnerCount: 1086554
					mocTagDtos: [,…]
					mode: 0
					name: "Python语言程序设计"
					ordinaryEditors: [,…]
					originalCourseChannel: 0
					productType: 1
					schoolId: 8007
					schoolImgUrl: "http://nos.netease.com/edu-image/C3257A57EE18C9695E8CEEFC957F373E.png?imageView&thumbnail=220y80&quality=100"
					schoolPanel: {id: 8007, name: "北京理工大学", shortName: "BIT",…}
					shortName: "0809BIT008"
					spocToOocStatus: 0
					status: 2
					termPanel: {id: 1206073223, courseId: 268001, courseName: null, startTime: 1552269600000, endTime: 1559575800000,…}
					universalCoupon: null
					videoId: 2065044
					webVisible: 1
					weight: 0
				}
				
			}
			1: {mocCourseCardDto: {id: 1003368009, shortName: "0806BJTU033", name: "Python语言程序设计",…}, cid: 1003368009,…}
			2: {mocCourseCardDto: {id: 1002058035, shortName: "0908BIT001CAP", name: "零基础学Python语言CAP",…},…}
			3: {mocCourseCardDto: {id: 1001870001, shortName: "0809BIT021A", name: "Python网络爬虫与信息提取",…},…}
			4: {mocCourseCardDto: {id: 1003479006, shortName: "0809PKU036", name: "Python语言基础与应用",…}, cid: 1003479006,…}
			5: {mocCourseCardDto: {id: 1001870002, shortName: "0809BIT021B", name: "Python数据分析与展示",…},…}
			6: {mocCourseCardDto: {id: 1001871001, shortName: "0809BIT021D", name: "Python科学计算三维可视化",…},…}
		]
		totalHit: 13

	}


}







https://www.icourse163.org/

https://www.icourse163.org/home.htm?userId=1022948033#/home/course

https://www.icourse163.org/member/login.htm?returnUrl=null&_trace_c_p_k2_=b1229a7156e743d7a24b6ef9827c8298#/webLoginIndex

https://open.weixin.qq.com/connect/qrconnect?appid=wx9a0045ed373f90e3&response_type=code&scope=snsapi_login&redirect_uri=https%3A%2F%2Fwww.icourse163.org%2Fsns%2Fwx%2FoAuthCallback.htm%3FoauthType%3Dlogin%26returnUrl%3DaHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvP2Zyb209c3R1ZHk%3D%26nrsstcw%3Dfalse%26nc%3Dfalse

https://open.weixin.qq.com/connect/qrconnect?appid=wx9a0045ed373f90e3&response_type=code&scope=snsapi_login&redirect_uri=https%3A%2F%2Fwww.icourse163.org%2Fsns%2Fwx%2FoAuthCallback.htm%3FoauthType%3Dlogin%26returnUrl%3DaHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaW5kZXguaHRtP2Zyb209c3R1ZHk%3D%26nrsstcw%3Dfalse%26nc%3Dfalse

Step0: 

https://www.icourse163.org/category/all
https://www.icourse163.org/category/guojiajingpin
categoryId: 1001093001
type: 30
orderBy: 0
pageIndex: 1
pageSize: 20

https://www.icourse163.org/category/computer

https://www.icourse163.org/category/all#?type=30&orderBy=0&pageIndex=2
https://www.icourse163.org/category/all#?type=30&orderBy=0&pageIndex=3
https://www.icourse163.org/category/guojiajingpin#?type=30&orderBy=0&pageIndex=2

md5+urandom
https://www.cnblogs.com/shanys/p/5890265.html
import os
from hashlib import md5
md5(os.urandom(24)).hexdigest()

cookie: EDUWEBDEVICE=167dbf5fa5d94e2081dff26ff08e2bdc; hb_MA-A976-948FFA05E931_source=www.baidu.com; bpmns=1; videoResolutionType=2; hasVolume=true; videoVolume=0.97; videoRate=1.5; __utmz=63145271.1556536170.24.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; UM_distinctid=16a6cb5b1f3f7-05cf382fdb4837-37657f06-fa000-16a6cb5b1f4a36; CNZZDATA1277354711=1349629894-1556598061-%7C1556598061; NTESSTUDYSI=8e1ea9f0aadd4d7db006d3eb78115738; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1556536168,1556536693,1556594681,1556697784; __utma=63145271.1316171326.1535256523.1556626984.1556697784.29; __utmc=63145271; WM_NI=H9NCcBbG4xp4ovYJ%2FPmPSdUbt3fwF2c1OM4pHoAmEnY2yVWQ9T3BmbZapEA7h5HbuhP3XBkQwg1Z%2BsINaphPy07FSxgcGTD8XCmZOUeFBszmcBWCoFQiwUESafcuDiKqOXE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89d96192bff793c934f18a8ba7c55b839b9e84b76798eb9682d0408abd9ca9b32af0fea7c3b92a8ce782a4e24aa299fc99f340adaa97abae5caf909d85d86ab8edaa98c53aa1ef81aeb77c8cb18f8ec8669beeb7b7d65bfb8cfda3f06a9abfc0a6c43daceb8883f86494ed98a3ea5bb5b9ffbbaa798b92af91eb5cbbf0f9a7d274a5bd89b5c7349c9da3bbce5fa79a8e94f967a19e99a4ee4e93b7b9b6c859a3baad96c76389af81b9c837e2a3; WM_TID=I86onYxK69JAUEFUBVIohysvkn0CW4mh; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1556698929; __utmb=63145271.11.9.1556698929679
edu-script-token: 8e1ea9f0aadd4d7db006d3eb78115738
origin: https://www.icourse163.org
referer: https://www.icourse163.org/category/guojiajingpin


POST https://www.icourse163.org/web/j/mocCourseCategoryBean.getCategByType.rpc?csrfKey=8e1ea9f0aadd4d7db006d3eb78115738
FormData:
	type: 4
Response:
{
	code: 0
	message: ""
	result: [
		{
			checked: true
			children: null
			id: 1001093001
			linkName: "guojiajingpin"
			mobCoverIcon: "http://edu-image.nosdn.127.net/d1e1279b0dd047f4b23848ae70687c96.png?imageView&quality=100&thumbnail=216y150"
			mobIcon: "http://edu-image.nosdn.127.net/d056aa4b-3a19-42ea-b88f-253b78c91b4a.png?imageView&quality=100"
			name: "国家精品"
			parentId: -1
			type: 4
			webIcon: "u-icon-elite"
			weight: 135
		}
		0: {id: 1001093001, name: "国家精品", type: 4, parentId: -1, linkName: "guojiajingpin",…}
		1: {id: 1001043131, name: "计算机", type: 4, parentId: -1, linkName: "computer", webIcon: "u-icon-computer",…}
		2: {id: 1001044005, name: "外语", type: 4, parentId: -1, linkName: "foreign-language",…}
		3: {id: 1001043135, name: "心理学", type: 4, parentId: -1, linkName: "psychology",…}
		4: {id: 1001043119, name: "经济学", type: 4, parentId: -1, linkName: "ECO", webIcon: "u-icon-economics",…}
		5: {id: 1202344001, name: "管理学", type: 4, parentId: -1, linkName: "management theory",…}
		6: {id: 1001043032, name: "法学", type: 4, parentId: -1, linkName: "law", webIcon: "u-icon-law",…}
		7: {id: 1001044001, name: "文学文化", type: 4, parentId: -1, linkName: "literature",…}
		8: {id: 1202344002, name: "历史", type: 4, parentId: -1, linkName: "historiography",…}
		9: {id: 1001043026, name: "哲学", type: 4, parentId: -1, linkName: "philosophy",…}
		10: {id: 1001043044, name: "工学", type: 4, parentId: -1, linkName: "engineering",…}
		11: {id: 1001043056, name: "理学", type: 4, parentId: -1, linkName: "science", webIcon: "u-icon-science",…}
		12: {id: 1001043130, name: "医药卫生", type: 4, parentId: -1, linkName: "biomedicine",…}
		13: {id: 1001111001, name: "农林园艺", type: 4, parentId: -1, linkName: "agriculture",…}
		14: {id: 1001043036, name: "艺术设计", type: 4, parentId: -1, linkName: "art-design", webIcon: "u-icon-art",…}
		15: {id: 1001043033, name: "教育教学", type: 4, parentId: -1, linkName: "teaching-method",…}
	]
}

POST https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=8e1ea9f0aadd4d7db006d3eb78115738
FormData:
	categoryId: -1
	type: 30
	orderBy: 0
	pageIndex: 1
	pageSize: 20

POST https://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc?csrfKey=8e1ea9f0aadd4d7db006d3eb78115738
FormData:
	categoryId: -1
	type: 30
	orderBy: 0
	pageIndex: 2
	pageSize: 20

Response:
{
	code: 0
	message: ""
	result: {
		courseCount: 0
		pagination: {
			DEFAULT_OFFSET: 0
			DEFAULT_PAGE_INDEX: 1
			DEFAULT_PAGE_SIZE: 10
			DEFAULT_TOTLE_COUNT: 0
			DEFAULT_TOTLE_PAGE_COUNT: 1
			limit: 20
			offset: 20
			pageIndex: 2
			pageSize: 20
			sortCriterial: null
			totleCount: 3007
			totlePageCount: 151
		}
		result: [
			{
				VideoUrl: null
				allTerms: null
				applyConvertChannelStatus: null
				applyMoocStatus: 0
				channel: 1
				classroomSupport: null
				courseType: 1
				currentTermChargeable: 0
				currentTermId: 1206288204
				firstPublishTime: 1543821112803
				fromCourseId: null
				fromCourseMode: -1
				fromCourseName: null
				fromCourseSchoolName: null
				gmtCreate: 1545888565615
				id: 1003606001
				imgUrl: "http://edu-image.nosdn.127.net/BA6E8A0C3E0F01524CA935791C1C9823.jpg?imageView&thumbnail=510y288&quality=100"
				lastLearningTime: null
				learnedCount: null
				learnerCount: 2432
				mocTagDtos: []
				mode: 0
				name: "International Relation and International Law"
				ordinaryEditors: [{member: {id: 11954098, nickName: "爱课程编辑FLY", userName: null, studentNumber: "",…}},…]
				originalCourseChannel: null
				productType: 1
				schoolId: 8008
				schoolImgUrl: "http://img2.ph.126.net/fehABjVTEaEhheiJK-f2Fw==/2963087079933355988.jpg"
				schoolPanel: {
					bgPhoto: "http://img2.ph.126.net/bvk96gI7cGQ4S-oCmV2QOw==/861031953858205055.jpg"
					classroomSupport: 1
					id: 8008
					imgUrl: "http://img2.ph.126.net/fehABjVTEaEhheiJK-f2Fw==/2963087079933355988.jpg"
					name: "吉林大学"
					shortName: "JLU"
					smallLogo: "http://img2.ph.126.net/z6uzXbT0n3AzqFazA3NCkg==/2217741341603701481.jpg"
					supportCommonMooc: 1
					supportMooc: 1
					supportPostgradexam: 0
					supportSpoc: 1
				}
				shortName: "0301JLU023"
				spocToOocStatus: 0
				status: 2
				termPanel: {
					achievementStatus: 0
					applyConvertChannelStatus: null
					applyMoocStatus: 0
					applyPassedTermId: null
					asynPrice: null
					bigPhotoUrl: "http://edu-image.nosdn.127.net/BA6E8A0C3E0F01524CA935791C1C9823.jpg?imageView&thumbnail=510y288&quality=100"
					certApplyEndTime: null
					certApplyStartTime: null
					certNo: null
					certStatus: 10
					chargeCertStatus: 10
					chargeableCert: null
					closeVisableStatus: 1
					copied: 1
					copyRight: null
					copyTime: null
					courseId: 1003606001			-- *
					courseName: null
					duration: ""
					endTime: 1563193800000
					enrollCount: 286
					fromTermId: 1003844001
					fromTermMode: 0
					hasEnroll: true
					id: 1206288204					-- *
					jsonContent: "国际法是什么，它为何存在，又能提供怎样的答案？在中国日渐融入国际社会，国际环境纷繁复杂的背景下，对国际法的研究，成为解决全球性问题“中国方案”的重要来源途径，也成为中国争取国家利益，增进人民福祉的重要方法。吉林大学何志鹏教授通过简明的解构与清晰的逻辑，为大家解读国际法的方方面面。"
					lectorPanels: [,…]
					lessonsCount: 0
					mode: 0
					orderPrice: null
					ordinaryEditors: null
					originMocTermCopyRight: null
					originalCourseChannel: null
					originalPrice: 0
					price: 0
					productType: 1
					publishStatus: 2
					schoolId: 8008
					schoolPanel: null
					scoreCardDto: null
					selfMocTermCopyright: null
					specialChargeableTerm: false
					spocToOocStatus: 0
					startTime: 1556762400000
					syncPrice: null
				}
				universalCoupon: null
				videoId: null
				webVisible: 1
				weight: 0
			}
			 {id: 1003782003, shortName: "0301JLU024", name: "国际法",…}
			 {id: 1003544002, shortName: "1202JXUFE016", name: "审计学",…}
			 {id: 1003518003, shortName: "1202CSU036", name: "会计管理信息系统",…}
			 {id: 1003632007, shortName: "1305TWHUT024", name: "设计概论",…}
			 {id: 1003469015, shortName: "0809XTU001", name: "计算思维—神秘的算法（算法设计与分析）",…}
			 {id: 1003503004, shortName: "0808CUT088", name: "自动控制原理及案例分析",…}
			 {id: 1003741002, shortName: "1002XJTU096", name: "内科学（呼吸系统疾病）",…}
			 {id: 1003476011, shortName: "0807ECNU015", name: "半导体器件原理与仿真设计",…}
			 {id: 1002918013, shortName: "0825SXU001", name: "环境毒理学",…}
			 {id: 1003628001, shortName: "0701NJU040", name: "数学分析（一）：一元微积分",…}
			 {id: 1003729002, shortName: "0809NWSUAF018", name: "程序设计基础（VB）",…}
			 {id: 1003759008, shortName: "0701BJFU020", name: "空间解析几何",…}
			 {id: 1003781003, shortName: "0809HIT074B", name: "集合论与图论（下）",…}
			 {id: 1003779006, shortName: "0809HIT074A", name: "集合论与图论（上）",…}
			 {id: 1002602073, shortName: "0809DLUT035", name: "系统分析与设计",…}
			 {id: 56001, shortName: "0809HIT004A", name: "程序设计基础",…}
			 {id: 1205964802, shortName: "0701NUDT022", name: "线性代数",…}
			 {id: 1003471004, shortName: "0701SJTU017", name: "世界文化史",…}
			 {id: 1002155003, shortName: "0701HIT052", name: "数学竞赛选讲",…}
		]
	}	
}

<ul class="u-nav-v1 f-cb">
<li><a href="/category/all"><span class="u-nav-name ga-click"><span class="u-icon-all"></span>全部</span></a></li>
<!--Regular list-->
<li><a href="/category/guojiajingpin"><span class="u-nav-name f-thide ga-click"><span class="u-icon-elite"></span>国家精品</span></a></li>

<li><a href="/category/computer"><span class="u-nav-name f-thide ga-click current"><span class="u-icon-computer"></span>计算机</span></a></li>

<li><a href="/category/foreign-language"><span class="u-nav-name f-thide ga-click"><span class="u-icon-foreign-language"></span>外语</span></a></li>

<li><a href="/category/psychology"><span class="u-nav-name f-thide ga-click"><span class="u-icon-psychology"></span>心理学</span></a></li>

<li><a href="/category/ECO"><span class="u-nav-name f-thide ga-click"><span class="u-icon-economics"></span>经济学</span></a></li>

<li><a href="/category/management theory"><span class="u-nav-name f-thide ga-click"><span class="u-icon-management"></span>管理学</span></a></li>

<li><a href="/category/law"><span class="u-nav-name f-thide ga-click"><span class="u-icon-law"></span>法学</span></a></li>

<li><a href="/category/literature"><span class="u-nav-name f-thide ga-click"><span class="u-icon-literature"></span>文学文化</span></a></li>

<li><a href="/category/historiography"><span class="u-nav-name f-thide ga-click"><span class="u-icon-history"></span>历史</span></a></li>

<li><a href="/category/philosophy"><span class="u-nav-name f-thide ga-click"><span class="u-icon-philosophy"></span>哲学</span></a></li>

<li><a href="/category/engineering"><span class="u-nav-name f-thide ga-click"><span class="u-icon-engineering"></span>工学</span></a></li>

<li><a href="/category/science"><span class="u-nav-name f-thide ga-click"><span class="u-icon-science"></span>理学</span></a></li>

<li><a href="/category/biomedicine"><span class="u-nav-name f-thide ga-click"><span class="u-icon-biomedicine"></span>医药卫生</span></a></li>

<li><a href="/category/agriculture"><span class="u-nav-name f-thide ga-click"><span class="u-icon-agriculture"></span>农林园艺</span></a></li>

<li><a href="/category/art-design"><span class="u-nav-name f-thide ga-click"><span class="u-icon-art"></span>艺术设计</span></a></li>

<li><a href="/category/teaching-method"><span class="u-nav-name f-thide ga-click"><span class="u-icon-teaching-method"></span>教育教学</span></a></li>

<li class="f-pr more-li"><span class="u-nav-more"><span class="u-icon-more2"></span>其他<span class="u-icon-thin-caret-down"></span></span>
<div class="more-box-wrap">
<ul class="more-box">
<!--Regular list-->
<li><a href="//www.icourse163.org/topics/CAPmooc2018summer" target="_blank"><span class="f-thide ga-click">大学先修课</span> <span class="u-icon-caret-right2 f-fr"></span></a></li>

<li><a href="//www.icourse163.org/vemooc" target="_blank"><span class="f-thide ga-click">职业教育课程</span> <span class="u-icon-caret-right2 f-fr"></span></a></li>

<li><a href="//www.icourse163.org/topics/teachermooc/" target="_blank"><span class="f-thide ga-click">教师系列MOOC</span> <span class="u-icon-caret-right2 f-fr"></span></a></li>

</ul></div></li>
</ul>

--------

<div class="u-nav-v2 f-cb">
<!--Regular if7-->
<li><a href="/category/computer"><span class="u-name ga-click current">全部</span></a></li>

<!--Regular list-->
<li><a href="/category/frontier technology"><span class="u-name f-thide ga-click">前沿技术</span></a></li>

<li><a href="/category/programminglanguage"><span class="u-name f-thide ga-click">程序设计与开发</span></a></li>

<li><a href="/category/ComputerBasics"><span class="u-name f-thide ga-click">计算机基础与应用</span></a></li>

<li><a href="/category/SoftwareEngineering"><span class="u-name f-thide ga-click">软件工程</span></a></li>

<li><a href="/category/networksecurity"><span class="u-name f-thide ga-click">网络与安全技术</span></a></li>

<li><a href="/category/computerorganization"><span class="u-name f-thide ga-click">硬软件系统及原理</span></a></li>

</div>

-------

<div class="u-clist f-bgw f-cb f-pr j-href ga-click" data-href="/course/DLUT-1002602073" data-action="课程点击" data-label="1002602073_1206261224">
	<div class="g-sd1">
		<div class="u-img f-fl">
			<img src="https://edu-image.nosdn.127.net/9EDE0A063193FC9E7B060A8F735FE921.png?imageView&amp;thumbnail=510y288&amp;quality=100&amp;thumbnail=223x125&amp;quality=100" alt="系统分析与设计" height="150px" width="265px">
		</div>
	</div>
	<div class="g-mn1">
		<div class="g-mn1c">
			<div class="cnt f-pr">
				<div class="t1 f-f0 f-cb first-row">
					<a href="//www.icourse163.org/course/DLUT-1002602073" target="_blank">
						<span class=" u-course-name f-thide">系统分析与设计</span>
					</a>
				</div>
				<div class="t2 f-fc3 f-nowrp f-f0">
					<a class="t21 f-fc9" href="/university/DLUT" target="_blank">大连理工大学</a>                                 
					<a class="f-fc9" href="/u/2354354432" target="_blank">马瑞新</a>
				</div>
				<a href="//www.icourse163.org/course/DLUT-1002602073" target="_blank">
					<span class="p5 brief f-ib f-f0 f-cb">本课程以培养信息系统分析与设计的能力为核心，采用项目导向与案例的方式，辅以软件开发云的真实企业生产环境，全面而又系统地阐述了信息系统建设的基本理论和方法。</span>
				</a>
				<div class="t2 f-fc3 f-nowrp f-f0 margin-top0">
					<span class="u-icon-person f-fc9"></span>
					<span class="hot">581人参加</span>
					<div class="over ">
						<span class="f-icon clock u-icon-clock2"></span>
						<span class="txt">进行至第1周</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<ul class="ux-pager">
  <li class="ux-pager_btn ux-pager_btn__prev">
      <a class="th-bk-disable-gh">上一页</a>
  </li>
  <li class="ux-pager_itm">
      <a class="th-bk-main">1</a>
  </li>
  <!--Regular if43-->
  
  <!--Regular list-->
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">2</a>
  </li>
  
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">3</a>
  </li>
  
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">4</a>
  </li>
  
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">5</a>
  </li>
  
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">6</a>
  </li>
  
  <!--Regular if44-->
  
  <li class="ux-pager_sep ux-pager_sep__right">
      <span>...</span>
  </li>
  <!--Regular if45-->
  <!--Regular if46-->
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">151</a>
  </li>
  
  <li class="ux-pager_btn ux-pager_btn__next">
      <a class="th-bk-main-gh">下一页</a>
  </li>
</ul>

Step1: Search

https://www.icourse163.org/search.htm?search=python#/
https://www.icourse163.org/search.htm?search=算法#/

https://www.icourse163.org/search.htm?search=%E7%AE%97%E6%B3%95#type=30&orderBy=0&pageIndex=2&courseTagType=null
https://www.icourse163.org/search.htm?search=%E7%AE%97%E6%B3%95#type=30&orderBy=0&pageIndex=3&courseTagType=null

//*[@id="j-courseNode"]

	//*[@id="j-courseCardListBox"]
		//*[@id="auto-id-1556601478080"]

Search out Item:

<div class="u-clist f-bgw f-cb f-pr j-href ga-click" data-href="/course/PKU-1001894005" data-action="课程点击" data-label="1001894005_1205957211">
	<div class="g-sd1">
		<div class="u-img f-fl">
			<img src="https://edu-image.nosdn.127.net/0FD1753D11D5BDA3E091A1040F71CE21.jpg?imageView&thumbnail=426y240&quality=100&thumbnail=223x125&quality=100" alt="程序设计与<span class=“f-fcorange f-ib“>算法</span>（二）<span class=“f-fcorange f-ib“>算法</span>基础" height="150px" width="265px">
		</div>
	</div>
	<div class="g-mn1">
		<div class="g-mn1c">
			<div class="cnt f-pr">
				<div class="t1 f-f0 f-cb first-row">
					<a href="//www.icourse163.org/course/PKU-1001894005" target="_blank">
						<span class=" u-course-name f-thide">程序设计与
							<span class="f-fcorange f-ib">算法</span>（二）
							<span class="f-fcorange f-ib">算法</span>基础</span>
					</a>
					<a target="_blank" href="http://www.icourse163.org/topics/2018NationalLevelMOOC/" class="tag u-course-tag f-f0 ga-click " data-action="国家精品" style="background-color: #CBA265">
						<span>国家精品</span>
						<div class="more-tag-info-hover">
							<div class="more-tag-info">
								<span>获得国家精品在线开放课程认定的课程</span>
								<div class="tipBg f-pa"></div>
								<div class="tipTp f-pa"></div>
							</div>
						</div>
					</a>
				</div>
				<div class="t2 f-fc3 f-nowrp f-f0">
					<a class="t21 f-fc9" href="/university/PKU" target="_blank">北京大学</a>                                 
					<a class="f-fc9" href="/u/mooc1456736596782" target="_blank">郭炜</a>            
				</div>
				<a href="//www.icourse163.org/course/PKU-1001894005" target="_blank">
					<span class="p5 brief f-ib f-f0 f-cb">本门课程要求学习者已经掌握C语言，以及基本的程序设计思想。本课程将讲述枚举、递归、分治、动态规划、搜索这几种
						<span class="f-fcorange f-ib">算法</span>。一部分内容，难度与中学信息学奥赛NOIP提高组的较难题，ACM国际大学生程序设…</span>
				</a>
				<div class="t2 f-fc3 f-nowrp f-f0 margin-top0">
					<span class="u-icon-person f-fc9"></span>
					<span class="hot">11104人参加</span>
					<div class="over ">
						<span class="f-icon clock u-icon-clock2"></span>
						<span class="txt">进行至第11周</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>


<!--Regular if13-->
<div class="course-card-list-pager ga-click f-f0" data-action="翻页点击">
<ul class="ux-pager">
  <li class="ux-pager_btn ux-pager_btn__prev">
      <a class="th-bk-disable-gh">上一页</a>
  </li>
  <li class="ux-pager_itm">
      <a class="th-bk-main">1</a>
  </li>
  <!--Regular if14-->
  
  <!--Regular list-->
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">2</a>
  </li>
  
  <!--Regular if15-->
  <!--Regular if16-->
  <!--Regular if17-->
  <li class="ux-pager_itm">
      <a class="th-bk-main-gh">3</a>
  </li>
  
  <li class="ux-pager_btn ux-pager_btn__next">
      <a class="th-bk-main-gh">下一页</a>
  </li>
</ul>
</div>


Step2: Course Item Detail

db.course.find({'lesson_crawl':'Done'}).count()

db.course.updateMany({},{$set:{'lesson_crawl':''}})

db.course.updateMany({'_id':1001894005},{$set:{'lesson_crawl':''}})

db.material.find({contentId:{$exists:true},course_id:1001894005},
{'_id':1,'contentId':1,'contentType':1,'chapter_name':1,'name':1,'position':1}).sort({'chapterId':1,'position':1})


db.material.find({contentId:{$exists:true},course_id:1001894005}).sort({'chapterId':1,'position':1}).pretty()

db.material.find({contentId:{$exists:false},course_id:1001894005}).sort({'chapterId':1,'position':1})

db.material.updateMany({'material_crawl':'Done'},{$set:{'material_crawl':''}})
db.material.updateMany({'material_crawl':'Done','contentType':1},{$set:{'material_crawl':''}})
db.material.updateMany({'material_crawl':'Done','contentType':3},{$set:{'material_crawl':''}})

db.material.find({course_id:1001894005,contentId:{$exists:true},'material_crawl':{$ne:'Done'}}).pretty()

db.material.find({contentId:{$exists:true},course_id:1001894005,contentType:4}).sort({'chapterId':1,'position':1}).pretty()



db.material.updateMany({contentId:{$exists:true},course_id:1001894005,contentType:4},{$unset:{resource_url:true}})

268001_1206073223
https://www.icourse163.org/course/BIT-268001
https://www.icourse163.org/learn/BIT-268001?tid=1206073223

data-href=/course/BIT-1001871002
data-label=1001871002_1001963002

https://www.icourse163.org/learn/BIT-1001871002?tid=1001963002#/learn/content

tid: get from `data-label="1001894005_1205957211">`

程序设计与算法（二）算法基础
https://www.icourse163.org/course/PKU-1001894005
https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211
https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211#/learn/announce
https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211#/learn/content

ALL :

POST https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr
FormData:
	callCount=1
	scriptSessionId=${scriptSessionId}190
	httpSessionId=056ce6d4df5f4c58a131d4d03146e076
	c0-scriptName=CourseBean
	c0-methodName=getMocTermDto
	c0-id=0
	c0-param0=number:1205957211			tid
	c0-param1=number:0
	c0-param2=boolean:true
	batchId=1556602963546
Response:

	s27.chapterId=1209097098;
	s27.contentId=null;
	s27.contentType=1;
	s27.gmtCreate=1548990674634;
	s27.gmtModified=1548990674634;
	s27.id=1210422476;
	s27.isTestChecked=false;
	s27.name="5. \u4F8B\u9898\uFF1A\u7184\u706F\u95EE\u9898(2)";
	s27.position=4;
	s27.releaseTime=1550444400000;
	s27.termId=1205957211;
	s27.test=null;
	s27.testDraftStatus=0;
	s27.units=s38;
	s27.viewStatus=null;

	s28.chapterId=1209097098;
	s28.contentId=null;
	s28.contentType=1;
	s28.gmtCreate=1548990674644;
	s28.gmtModified=1548990674644;
	s28.id=1210422477;
	s28.isTestChecked=false;
	s28.name="\u7B2C\u4E00\u5468\u8BB2\u4E49";
	s28.position=5;
	s28.releaseTime=1550444400000;
	s28.termId=1205957211;
	s28.test=null;
	s28.testDraftStatus=0;
	s28.units=s40;
	s28.viewStatus=null;

	s39.anchorQuestions=null;
	s39.attachments=null;
	s39.chapterId=1209097098;
	s39.contentId=1005857411;
	s39.contentType=1;
	s39.durationInSeconds=1317;
	s39.freePreview=0;
	s39.gmtCreate=1548990674642;
	s39.gmtModified=1548990674642;
	s39.id=1212471890;
	s39.jsonContent=null;
	s39.learnCount=null;
	s39.lessonId=1210422476;
	s39.live=null;
	s39.liveInfoDto=null;
	s39.name="5.\u4F8B\u9898\uFF1A\u7184\u706F\u95EE\u9898(2)";
	s39.position=4;
	s39.resourceInfo=null;
	s39.termId=1205957211;
	s39.unitId=null;
	s39.viewStatus=null;


	s41.anchorQuestions=null;
	s41.attachments=null;
	s41.chapterId=1209097098;
	s41.contentId=1212867249;
	s41.contentType=3;
	s41.durationInSeconds=null;
	s41.freePreview=null;
	s41.gmtCreate=1548990674647;
	s41.gmtModified=1550709781522;
	s41.id=1212471891;
	s41.jsonContent=null;
	s41.learnCount=null;
	s41.lessonId=1210422477;
	s41.live=null;
	s41.liveInfoDto=null;
	s41.name="\u7B2C\u4E00\u5468\u8BB2\u4E49";
	s41.position=5;
	s41.resourceInfo=null;
	s41.termId=1205957211;
	s41.unitId=null;
	s41.viewStatus=null;

Video:
	<div class="u-learnLesson normal f-cb f-pr" id="auto-id-1556602963580">
		<div class="j-icon icon f-pa icon-1"></div>
		<h4 class="j-name name f-fl f-thide">5. 例题：熄灯问题(2)</h4>
		<div class="j-typebox f-cb f-fr"><div>
			<div class="f-icon lsicon f-fl " data-cid="1212471890" title="视频：5.例题：熄灯问题(2)" id="auto-id-1556602963583">
				<span class="u-icon-video2"></span>
			</div>
		</div>
	</div>
	=> 
	s27.id=1210422476;
	s39.id=1212471890;			data-cid="1212471890"
	s39.lessonId=1210422476;
	https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211#/learn/content?type=detail&id=1210422476

Document:
	<div class="u-learnLesson normal f-cb f-pr" id="auto-id-1556602963586">
		<div class="j-icon icon f-pa icon-1"></div>
		<h4 class="j-name name f-fl f-thide">第一周讲义</h4>
		<div class="j-typebox f-cb f-fr"><div>
			<div class="f-icon lsicon f-fl " data-cid="1212471891" title="文档：第一周讲义" id="auto-id-1556602963589">
				<span class="u-icon-doc"></span>
			</div>
		</div>
	</div>
	=> 
	s28.id=1210422477;
	s41.id=1212471891;				data-cid="1212471891"
	s41.lessonId=1210422477;
	https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211#/learn/content?type=detail&id=1210422477&sm=1
	:
		<a class="j-downpdf downpdf u-btn u-btn-sm u-btn-whiteGreen f-fr" target="_blank" href="https://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=sQm6lExz7mU8a8LZxV7ZkFFFZ6W6jcVmnroY60ykmDo%3D&Expires=1556612315&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf">文档下载</a>

		https://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=vR%2BGfNhoSzVpkSNxncG3HqWn0Kr6isYstnI5xp%2FyGU8%3D&Expires=1556546430&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf


https://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=vR%2BGfNhoSzVpkSNxncG3HqWn0Kr6isYstnI5xp%2FyGU8%3D&Expires=1657332060&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf

http://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=vR%2BGfNhoSzVpkSNxncG3HqWn0Kr6isYstnI5xp%2FyGU8%3D&Expires=1557341013&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf

https://www.icourse163.org/learn/PKU-1001894005?tid=1205957211#/learn/content?type=detail&id=1210422477&cid=1212471891

//#DWR-INSERT
//#DWR-REPLY
dwr.engine._remoteHandleCallback('1557327427032','0',{contentId:null,contentType:null,duration:null,hdMp4Url:null,htmlContent:null,id:null,learnedPosition:1,origSrtUrl:null,paper:null,parsedSrtUrl:null,post:null,randomKey:null,sdMp4Url:null,shdMp4Url:null,srtKeys:null,textOrigUrl:"http://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=Yrqg2clmouIEtouBNm0OYZIlek6SrlX%2FxdY8AzDCDgQ%3D&Expires=1557341740&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf",textPageWhRatio:1.78,textPages:51,textUrl:"http://nos.netease.com/edu-lesson-content/content-1212867249.swf?Signature=%2BjVZMyFLyaNhEgOx3JCH0guc5J8tjpVfwv4VX4J%2FQuc%3D&Expires=1557341740&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa",type:null,unitId:null,videoHDUrl:null,videoId:null,videoImgUrl:null,videoLearnTime:0,videoSHDUrl:null,videoUrl:null,videoVo:null});


---------------------------------------------------------------
Click Document

POST https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr
FormData:
	callCount=1
	scriptSessionId=${scriptSessionId}190
	httpSessionId=056ce6d4df5f4c58a131d4d03146e076
	c0-scriptName=CourseBean
	c0-methodName=getLessonUnitLearnVo
	c0-id=0
	c0-param0=number:1212867249			s41.contentId=1212867249;
	c0-param1=number:3					contentType=3
	c0-param2=number:0
	c0-param3=number:1212471891			id=1212471891
	batchId=1556605282842
Response:
	//#DWR-INSERT
	//#DWR-REPLY
	dwr.engine._remoteHandleCallback('1556605282842','0',{contentId:null,contentType:null,duration:null,hdMp4Url:null,htmlContent:null,id:null,learnedPosition:1,origSrtUrl:null,paper:null,parsedSrtUrl:null,post:null,randomKey:null,sdMp4Url:null,shdMp4Url:null,srtKeys:null,textOrigUrl:"http://nos.netease.com/edu-lesson-pdfsrc/626F8E379443065A16DB5E9B30F1C35D-1550709558538?Signature=DhcddLCPpajD5VYNwNxDas0uBxD3YJDG8a6MvVsbV7c%3D&Expires=1556612895&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa&download=1.+%E6%9E%9A%E4%B8%BE.pdf",textPageWhRatio:1.78,textPages:51,textUrl:"http://nos.netease.com/edu-lesson-content/content-1212867249.swf?Signature=hnUYn63xajTGb1lbUpqMNbJ8kQ2OXHNm3%2Bx2o6s9pMw%3D&Expires=1556612895&NOSAccessKeyId=7ba71f968e4340f1ab476ecb300190fa",type:null,unitId:null,videoHDUrl:null,videoId:null,videoImgUrl:null,videoLearnTime:0,videoSHDUrl:null,videoUrl:null,videoVo:null});


FormData:
	callCount=1
	scriptSessionId=${scriptSessionId}190
	httpSessionId=056ce6d4df5f4c58a131d4d03146e076
	c0-scriptName=CourseBean
	c0-methodName=getLessonUnitLearnVo
	c0-id=0
	c0-param0=number:1007912104			contentId=1007912104;
	c0-param1=number:1					contentType=1
	c0-param2=number:0
	c0-param3=number:1212471903			id=1212471903
	batchId=1556605282842
Response:
	//#DWR-INSERT
	//#DWR-REPLY
	var s0={};s0.clientEncryptKeyVersion=null;s0.duration=862;s0.encrypt=false;s0.flvCaption=null;s0.flvHdUrl="http://v.stu.126.net/mooc-video/nos/flv/2017/12/03/1007912104_dd71c334d57640da8eba501b79f6fd2f_hd.flv?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.flvSdUrl="http://v.stu.126.net/mooc-video/nos/flv/2017/12/03/1007912104_d98adb9a20784319b0c188010b3f51fe_sd.flv?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.flvShdUrl="http://v.stu.126.net/mooc-video/nos/flv/2017/12/03/1007912104_a5a00ddc15ed40848ccaea7de9ec0f27_shd.flv?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.isEncrypt=false;s0.key="99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.m3u8HdUrl=null;s0.m3u8SdUrl=null;s0.m3u8ShdUrl=null;s0.mp4Caption=null;s0.mp4HdUrl="http://v.stu.126.net/mooc-video/nos/mp4/2017/12/03/1007912104_5efd3f21a0e64ce38d363e70ddf74706_hd.mp4?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.mp4SdUrl="http://v.stu.126.net/mooc-video/nos/mp4/2017/12/03/1007912104_29ee655366bc4a21ada050e031ac52f1_sd.mp4?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.mp4ShdUrl="http://v.stu.126.net/mooc-video/nos/mp4/2017/12/03/1007912104_cdbdbad6828a4365827311efaa10f323_shd.mp4?ak=99ed7479ee303d1b1361b0ee5a4abceecdbd9838e45e7bda6a45fa35d61725ebfebc1e06643102c7580d4b0d308c025b67cec5b1f00ad996ce8a9d2e949399af0015e48ffc49c659b128bfe612dda086d65894b8ef217f1626539e3c9eb40879c29b730d22bdcadb1b4f67996129275fa4c38c6336120510aea1ae1790819de86e0fa3e09eeabea1b068b3d9b9b6597acf0c219eb000a69c12ce9d568813365b3e099fcdb77c69ca7cd6141d92c122af";s0.needKeyTimeValidate=false;s0.playerCollection=3;s0.signature=null;s0.srtKeys=null;s0.start=0;s0.status=null;s0.videoDecryptData=null;s0.videoId=1007912104;s0.videoImgUrl="http://nos.netease.com/mooc-video/09c1b1f4-39e7-4222-a79d-cb6401d2892d.jpg";s0.videoProtectedDataDto=null;
	dwr.engine._remoteHandleCallback('1','0',{contentId:null,contentType:null,duration:null,hdMp4Url:null,htmlContent:null,id:null,learnedPosition:1,origSrtUrl:null,paper:null,parsedSrtUrl:null,post:null,randomKey:null,sdMp4Url:null,shdMp4Url:null,srtKeys:null,textOrigUrl:"",textPageWhRatio:null,textPages:0,textUrl:"",type:null,unitId:null,videoHDUrl:null,videoId:null,videoImgUrl:null,videoLearnTime:0,videoSHDUrl:null,videoUrl:null,videoVo:s0});

attachment:

//#DWR-INSERT
//#DWR-REPLY
dwr.engine._remoteHandleCallback('1557478788401','0',{contentId:null,contentType:null,duration:null,hdMp4Url:null,htmlContent:"<p>\u8BF7\u4E0B\u8F7D\u9644\u4EF6</p>",id:null,learnedPosition:1,origSrtUrl:null,paper:null,parsedSrtUrl:null,post:null,randomKey:null,sdMp4Url:null,shdMp4Url:null,srtKeys:null,textOrigUrl:"",textPageWhRatio:null,textPages:0,textUrl:"",type:null,unitId:null,videoHDUrl:null,videoId:null,videoImgUrl:null,videoLearnTime:0,videoSHDUrl:null,videoUrl:null,videoVo:null});

<a class="j-downtxt downpdf u-btn u-btn-sm u-btn-whiteGreen f-fr" href="/course/attachment.htm?fileName=week9.zip&nosKey=E10AD03432E2BE51B2640F88BA83C191-1515898079229" target="_blank">下载附件</a>

https://www.icourse163.org/course/attachment.htm?fileName=week9.zip&nosKey=E10AD03432E2BE51B2640F88BA83C191-1515898079229


	"_id" : 1212471956,
	"chapterId" : 1209097117,
	"chapter_name" : "第九周测验答案",
	"contentId" : 1209176291,
	"contentType" : 4,
	"course_id" : 1001894005,
	"course_name" : "程序设计与算法（二）算法基础",
	"gmtCreate" : "1557098497829",
	"gmtModified" : "1557098497829",
	"jsonContent" : "\"{\"nosKey\":\"E10AD03432E2BE51B2640F88BA83C191-1515898079229\",\"fileName\":\"week9.zip\"}\"",
	"lessonId" : 1210422552,
	"lesson_name" : "第九周测验答案",
	"name" : "第九周测验答案",
	"position" : 0,
	"termId" : 1205957211

---------------------------------------------------------------

Click Video:

POST https://www.icourse163.org/web/j/resourceRpcBean.getVideoToken.rpc?csrfKey=056ce6d4df5f4c58a131d4d03146e076
Form Data:
	key: LEARN_PLAN_COURAGE_SLOGAN
Response:
{
code: 0
message: ""
result: {
	duration: 1317
	name: "枚举04_熄灯问题02.mp4"
	signature: "544f476f524c4b30624a69464745586e37614754427a716f667352716e694b76696b44596735554f4c4335433975716b4943475545594d474e554648394939467250796a6a39586157723670356e6e695672323832735971314a2f393676567936454842526b5249555039693372324231427959416562367038444875434352632f484754442b4e7932674174456c2f7948595761513d3d"
	status: 0
	videoId: 1005857411
	videoImgUrl: null
	}
}

POST https://vod.study.163.com/eds/api/v1/vod/video
form Data:
	videoId: 1005857411
	signature: 544f476f524c4b30624a69464745586e37614754427a716f667352716e694b76696b44596735554f4c4335433975716b4943475545594d474e554648394939467250796a6a39586157723670356e6e695672323832735971314a2f393676567936454842526b5249555039693372324231427959416562367038444875434352632f484754442b4e7932674174456c2f7948595761513d3d
	clientType: 1
Response:
{
code: 0
message: "ok"
result: {
		cdnPoints: [
			 {ip: "111.41.53.138", isp: "yd1", ispName: "移动一"}
			,{ip: "60.5.255.40", isp: "lt1", ispName: "联通一"}
			,{ip: "112.123.33.138", isp: "lt2", ispName: "联通二"}
			,{ip: "103.254.188.248", isp: "dx1", ispName: "电信一"}
			,{ip: "27.155.73.116", isp: "dx2", ispName: "电信二"}
		]
		defaultQuality: 1
		duration: 1317
		name: "枚举04_熄灯问题02.mp4"
		srtCaptions: []
		videoId: 1005857411
		videoImgUrl: "http://jdvodrvfb210d.vod.126.net/mooc-video/nos/mp4/2017/02/28/1005857411_big.jpg"
		videoThumbnail: null
		videos: [
			{
				e: false
				format: "mp4"
				k: null
				quality: 1
				size: 102126521
				v: null
				videoUrl: "http://jdvodrvfb210d.vod.126.net/mooc-video/nos/mp4/2017/02/28/1005857411_7d85a4772f334488acc2e53fe98aa7eb_sd.mp4?ak=7909bff134372bffca53cdc2c17adc27a4c38c6336120510aea1ae1790819de839f3c09380aeb76f86db8f73b30ee00f1af7c38c691a938d10d28e07d520a6933059f726dc7bb86b92adbc3d5b34b132da329e8799422b49118e96d631c477c3623591d5e74d0640a136e4a4f0e4eb71"
			}
			{quality: 2, size: 166944285,…}
			{quality: 3, size: 193460079,…}
			{quality: 1, size: 102441705,…}
			{quality: 2, size: 167259611,…}
			{quality: 3, size: 193414312,…}
		]
	}
uuid: null
}


--------------------------------------------


<div class="u-learnLesson normal f-cb f-pr" id="auto-id-1556624025716">
	<div class="j-icon icon f-pa icon-1"></div>
	<h4 class="j-name name f-fl f-thide">机器学习简介</h4>
	<div class="j-typebox f-cb f-fr"><div>
		<div class="f-icon lsicon f-fl " data-cid="1212966928" title="视频：机器学习的初步认识" id="auto-id-1556624025719">
			<span class="u-icon-video2"></span>
		</div>
		<div class="f-icon lsicon f-fl " data-cid="1212966940" title="文档：机器学习简介" id="auto-id-1556624025721">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl " data-cid="1213015060" title="测验题：机器学习的多学科性" id="auto-id-1556624025723">
			<span class="u-icon-test3"></span>
		</div>
		<div class="f-icon lsicon f-fl " data-cid="1213012587" title="测验题：机器学习的概念" id="auto-id-1556624025725">
			<span class="u-icon-test3"></span>
		</div>
		<div class="f-icon lsicon f-fl " data-cid="1213019185" title="测验题：机器学习的正确认识" id="auto-id-1556624025727">
			<span class="u-icon-test3"></span>
		</div>
	</div>
</div>


<div class="u-learnLesson normal f-cb f-pr last" id="auto-id-1556623953303">
	<div class="j-icon icon f-pa icon-2"></div>
	<h4 class="j-name name f-fl f-thide">第1周作业及学习资料</h4>
	<div class="j-typebox f-cb f-fr"><div>
		<div class="f-icon lsicon f-fl " data-cid="1212669645" title="视频：第1周练习与作业" id="auto-id-1556623954608">
			<span class="u-icon-video2"></span>
		</div>
		<div class="f-icon lsicon f-fl learned" data-cid="1212669646" title="文档：1.0&nbsp;第1周课程导学" id="auto-id-1556623954610">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl " data-cid="1212669647" title="文档：1.1&nbsp;程序设计基本方法" id="auto-id-1556623954612">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl learned" data-cid="1212669648" title="文档：1.2&nbsp;Python开发环境配置" id="auto-id-1556623954614">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl learned" data-cid="1212669649" title="文档：1.3&nbsp;实例1:&nbsp;温度转换" id="auto-id-1556623954616">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl learned" data-cid="1212669650" title="文档：1.4&nbsp;Python程序语法元素分析" id="auto-id-1556623954618">
			<span class="u-icon-doc"></span>
		</div>
		<div class="f-icon lsicon f-fl learned" data-cid="1212669651" title="富文本：实例1:&nbsp;温度转换源代码" id="auto-id-1556623954620">
			<span class="u-icon-text"></span>
		</div>
	</div>
</div>

<a class="j-downtxt downpdf u-btn u-btn-sm u-btn-whiteGreen f-fr" href="/course/attachment.htm?fileName=%E5%AE%9E%E4%BE%8B1-%E6%B8%A9%E5%BA%A6%E8%BD%AC%E6%8D%A2%E6%BA%90%E4%BB%A3%E7%A0%81.zip&nosKey=D8B78FFC2BD10BA5C0F33D53EE58F89D-1554123296502" target="_blank">下载附件</a>


--------------------------------------------


//*[@id="courseLearn-inner-box"]


//*[@id="courseLearn-inner-box"]/div/div/div[1]

<div class="j-moduletitle u-learn-moduletitle f-cb" style=""><h2 class="f-fl j-moduleName">课件</h2><p class="u-helplink f-fc9 f-fr"><a class="f-fcgreen" href="/help/help.htm#/hf?t=2" target="_blank">查看帮助</a></p></div>

//*[@id="courseLearn-inner-box"]/div/div/div[3]


//*[@id="courseLearn-inner-box"]/div/div/div[3]/div[3]

//*[@id="auto-id-1556536770354"]
<div class="u-learnLesson normal f-cb f-pr" id="auto-id-1556536770354"><div class="j-icon icon f-pa icon-1"></div><h4 class="j-name name f-fl f-thide">1. 例题：完美立方</h4><div class="j-typebox f-cb f-fr"><div><div class="f-icon lsicon f-fl " data-cid="1212471886" title="视频：1.完美立方" id="auto-id-1556536770357"><span class="u-icon-video2"></span></div></div></div></div>


<div class="u-learnLesson normal f-cb f-pr" id="auto-id-1556536770384"><div class="j-icon icon f-pa icon-1"></div><h4 class="j-name name f-fl f-thide">第一周讲义</h4><div class="j-typebox f-cb f-fr"><div><div class="f-icon lsicon f-fl " data-cid="1212471891" title="文档：第一周讲义" id="auto-id-1556536770387"><span class="u-icon-doc"></span></div></div></div></div>





//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div
<div class="u-learnBCUI f-cb"><a href="#/learn/content" target="_self" class="f-fl f-fc3 f-f0 link">课件</a><span class="f-icon f-fl icon u-icon-caret-right2"></span><div class="f-fl j-chapter"><div class="u-select">    											<div class="up j-up f-thide" id="auto-id-1556537737612">第一周 枚举</div>    											<div class="down f-bg j-list" style="display: none;"><div class="f-thide list" title="第一周 枚举" id="auto-id-1556537737724">第一周&nbsp;枚举</div><div class="f-thide list" title="第二周&nbsp;递归（一）" id="auto-id-1556537737726">第二周&nbsp;递归（一）</div><div class="f-thide list" title="第三周&nbsp;递归（二）" id="auto-id-1556537737728">第三周&nbsp;递归（二）</div><div class="f-thide list" title="第四周&nbsp;二分算法" id="auto-id-1556537737730">第四周&nbsp;二分算法</div><div class="f-thide list" title="第五周&nbsp;分治" id="auto-id-1556537737732">第五周&nbsp;分治</div><div class="f-thide list" title="第六周&nbsp;动态规划（一）" id="auto-id-1556537737734">第六周&nbsp;动态规划（一）</div><div class="f-thide list" title="第七周&nbsp;动态规划(二)" id="auto-id-1556537737736">第七周&nbsp;动态规划(二)</div><div class="f-thide list" title="第八周&nbsp;深度优先搜索（一）" id="auto-id-1556537737738">第八周&nbsp;深度优先搜索（一）</div><div class="f-thide list" title="第九周&nbsp;深度优先搜索（二）" id="auto-id-1556537737740">第九周&nbsp;深度优先搜索（二）</div><div class="f-thide list" title="第十周&nbsp;广度优先搜索" id="auto-id-1556537737742">第十周&nbsp;广度优先搜索</div><div class="f-thide list" title="第十一周&nbsp;贪心算法" id="auto-id-1556537737744">第十一周&nbsp;贪心算法</div><div class="f-thide list" title="第一周测验答案" id="auto-id-1556537737746">第一周测验答案</div><div class="f-thide list" title="第二周测验答案" id="auto-id-1556537737748">第二周测验答案</div><div class="f-thide list" title="第三周测验答案" id="auto-id-1556537737750">第三周测验答案</div><div class="f-thide list" title="第四周测验答案" id="auto-id-1556537737752">第四周测验答案</div><div class="f-thide list" title="第五周测验答案" id="auto-id-1556537737754">第五周测验答案</div><div class="f-thide list" title="第六周测验答案" id="auto-id-1556537737756">第六周测验答案</div><div class="f-thide list" title="第七周测验答案" id="auto-id-1556537737758">第七周测验答案</div></div>    									      </div></div><span class="f-icon f-fl icon u-icon-caret-right2"></span><div class="f-fl j-lesson"><div class="u-select">    											<div class="up j-up f-thide" id="auto-id-1556537737630">1. 例题：完美立方</div>    											<div class="down f-bg j-list" style="display: none;"><div class="f-thide list" title="1.&nbsp;例题：完美立方" id="auto-id-1556537737762">1.&nbsp;例题：完美立方</div><div class="f-thide list" title="2.&nbsp;例题：生理周期" id="auto-id-1556537737764">2.&nbsp;例题：生理周期</div><div class="f-thide list" title="3.&nbsp;例题：称硬币" id="auto-id-1556537737766">3.&nbsp;例题：称硬币</div><div class="f-thide list" title="4.&nbsp;例题：熄灯问题(1)" id="auto-id-1556537737768">4.&nbsp;例题：熄灯问题(1)</div><div class="f-thide list" title="5.&nbsp;例题：熄灯问题(2)" id="auto-id-1556537737770">5.&nbsp;例题：熄灯问题(2)</div><div class="f-thide list" title="第一周讲义" id="auto-id-1556537737772">第一周讲义</div><div class="f-thide list" title="Openjudge在线做题必读" id="auto-id-1556537737774">Openjudge在线做题必读</div></div>    									      </div></div></div>









