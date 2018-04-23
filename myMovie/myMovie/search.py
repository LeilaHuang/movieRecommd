# -*- coding: utf-8 -*-
# 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import pandas
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise import*

 
# 表单
def search_form(request):

    return render_to_response('search_form.html')
 
# 接收请求数据


userID = 'cevia'

def search(request):  
    request.encoding='utf-8'
    if 'userId' in request.GET:
    	userID = request.GET['userId']
    	message = 'the userId: ' + request.GET['userId']

    	context = {}
    	context['recomdMoive'] = prepareJob(userID)
    	context['userId'] = request.GET['userId']
    	return render(request, 'search_form.html', context)
        #context['recomdMoive'] = getTopN(movielist,ratedMovieList)
      
    else:
        message = 'no userId submitted'
    return HttpResponse(message)

def SVDFun(data,userSet, movieSet, userID):
	# Evaluate performances of our algorithm on the dataset.
#	itemList = [[0] * userNumber] * itemNumber
#	userList = [[0] * itemNumber] * userNumber
	algo = SVD()
	# perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
	trainset = data.build_full_trainset()
	algo.fit(trainset)
	# meanRMSE = average(perf['RMSE'])
	# meanMAE = average(perf['MAE'])
	movielist = dict()
	for movie in movieSet:
		est = algo.predict(userID,movie).est
		movielist[movie] = est
	return movielist


def getTopN(movielist,ratedMovieList):

	numberSort = sorted(movielist.items(),key=lambda d : d[0],reverse = False)
	numberSort2 = sorted(numberSort,key=lambda d : d[1],reverse = True)


	top = []
	for l in list(tuple(numberSort2)):
		top.append(l[0])

	top = [l for l in top if l not in ratedMovieList]
	top_n = []
	for n in top[0:10]:
		top_n.append(n)
	return top_n	

def prepareJob(userID):

	douban_comments = pandas.read_csv('/Users/huangzeqian/Downloads/douban_yingping.csv')
	douban_comments.duplicated()
	comments = douban_comments.iloc[:,[8,9,10]]

	ratedList = comments[comments['userId'] == userID].values
	ratedMovieList = []
	for i in range(0,ratedList.shape[0]):
		ratedMovieList.append(ratedList[i][1])

	comments = comments.values

	ratings = []
	movieids = []
	userIds = []

	for i in range(0,comments.shape[0]):
		rating = comments[i][0]
		movieid = comments[i][1]
		userId = comments[i][2]
		try:
			rating = int(rating)
			movieid = int(movieid)
			ratings.append(rating)
			movieids.append(movieid)
			userIds.append(userId)
		except:
			print('str cannot convert to int')

	ratings_dict = {'itemID': movieids,
	                'userID': userIds,
	                'rating': ratings}

	df = pandas.DataFrame(ratings_dict)
	# A reader is still needed but only the rating_scale param is requiered.
	reader = Reader(rating_scale=(1, 5))

	# The columns must correspond to user id, item id and ratings (in that order).
	data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

	# We can now use this dataset as we please, e.g. calling cross_validate
	data.split(2)

	userSet = set(userIds)
	movieSet = set(movieids)

	movielist = SVDFun(data,userSet,movieSet,userID)

	return getTopN(movielist,ratedMovieList)# 这里运行getTopN()

def average(seq, total=0.0): 
  num = 0 
  for item in seq: 
    total += item 
    num += 1 
  return total / num
