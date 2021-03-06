
import pandas
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
from surprise.dump import dump
from sklearn.externals import joblib
from surprise import*

# userID = 'cevia' #通过这个userid（这个userid可以从douban影评csv里面任意取一个模拟）最终通过得到getTopN得到topN的电影ID

def SVDFun(data,userSet, movieSet, userID):
	# Evaluate performances of our algorithm on the dataset.
#	itemList = [[0] * userNumber] * itemNumber
#	userList = [[0] * itemNumber] * userNumber
	algo = SVD()
	# perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
	# trainset = data.build_full_trainset()
	trainset, testset = train_test_split(data, test_size=.25)
	# algo.fit(trainset)
	# predictions = algo.test(testset)
	algo = joblib.load('svdmodel.pkl') 
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

	douban_comments = pandas.read_csv('douban_yingping.csv')
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
			# print('str cannot convert to int')
			pass

	ratings_dict = {'itemID': movieids,
	                'userID': userIds,
	                'rating': ratings}

	df = pandas.DataFrame(ratings_dict)
	# A reader is still needed but only the rating_scale param is requiered.
	reader = Reader(rating_scale=(1, 5))

	# The columns must correspond to user id, item id and ratings (in that order).
	data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

	# We can now use this dataset as we please, e.g. calling cross_validate
	cross_validate(NormalPredictor(), data, cv=2)

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


print(prepareJob("cevia"))







	