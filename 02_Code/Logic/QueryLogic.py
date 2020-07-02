from database.ConnectToDB import ConnectToDB
from pprint import pprint
import logging
import json


max_threshold = 10

class QueryLogic:
    # logger setup, use logger.info(or level needed)('Log message') to log
    logging.basicConfig(filename='log.txt', level=logging.INFO,
                        format='Class: %(name)s - Time: %(asctime)s - Level: %(levelname)s - Message: %(message)s')
    logger = logging.getLogger('QueryLogic')

    def __init__(self):
        remote_db = ConnectToDB()

        try:
            client = remote_db.get_clientRemote()
            client.server_info()
        except:
            print('Connection Error')

        db = client['DBSF20']
        client.server_info()
        self.collection = db['videos']
        self.categories = db['categories']


    '''VIEWS'''

    # DO DISLIKES HAVE A NEGATIVE IMPACT ON VIEWS? (Sorted by Ratio)
    def calculate_viewRatioViewDislikeSortedByRatio(self):
        View_RatioDislike = self.collection.aggregate([
            {'$project':
                {
                    'Dislikes': {'$sum' : '$interactions.dislikes'},
                    'Views' : {'$sum' : '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                          '$multiply': [{'$divide': ['$interactions.dislikes', '$interactions.views']}, 100]}]},
                    'interactions.dislikes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                },

            },
            {'$sort': {'Ratio': -1, 'interactions.views': -1}}
        ],
            allowDiskUse= True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        View_RatioDislike = sorted(View_RatioDislike, key=lambda x: x['Ratio'], reverse=True)
        View_RatioDislike2 = sorted(View_RatioDislike, key=lambda x: x['Ratio'], reverse=False)
        for i in range(len(View_RatioDislike)):
            sumRatio += View_RatioDislike[i]['Ratio']
            sumDislikes += View_RatioDislike[i]['Dislikes']
            sumLikes += View_RatioDislike[i]['Views']

        avgRatio = sumRatio/len(View_RatioDislike)
        avgDislikes = sumDislikes/len(View_RatioDislike)
        avgViews = sumLikes/len(View_RatioDislike)
        results = []
        global max_threshold
        for result in range(len(View_RatioDislike)):
            if result < max_threshold/2:
                results.append(View_RatioDislike[result])
        average = {'interactions': {'views': avgViews, 'dislikes': avgDislikes}, 'Dislikes': avgDislikes, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioDislike[len(View_RatioDislike)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioDislike2)):
            if View_RatioDislike2[i]['Ratio'] != 0:
                temp_vals.append(View_RatioDislike2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold/2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Ratio'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i+1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 6:
                print(sortedResults[i].update(Rank='median'))
            elif i == 5:
                sortedResults[i].update(Rank='average')

        keys = list(sortedResults[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # DO DISLIKES HAVE A NEGATIVE IMPACT ON VIEWS? (Sorted by Dislikes)
    def calculate_viewRatioViewDislikeSortedByDislikes(self):
        View_RatioDislike = self.collection.aggregate([
            {'$project':
                {
                    'Dislikes': {'$sum': '$interactions.dislikes'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.dislikes', '$interactions.views']}, 100]}]},
                    'interactions.dislikes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                },

            },
            {'$sort': {'interactions.dislikes': -1, 'interactions.views': -1}}
        ],
            allowDiskUse=True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        View_RatioDislike = sorted(View_RatioDislike, key=lambda x: x['Dislikes'], reverse=True)
        View_RatioDislike2 = sorted(View_RatioDislike, key=lambda x: x['Dislikes'], reverse=False)
        for i in range(len(View_RatioDislike)):
            sumRatio += View_RatioDislike[i]['Ratio']
            sumDislikes += View_RatioDislike[i]['Dislikes']
            sumLikes += View_RatioDislike[i]['Views']

        avgRatio = sumRatio / len(View_RatioDislike)
        avgDislikes = sumDislikes / len(View_RatioDislike)
        avgViews = sumLikes / len(View_RatioDislike)
        results = []
        global max_threshold
        for result in range(len(View_RatioDislike)):
            if result < max_threshold / 2:
                results.append(View_RatioDislike[result])
        average = {'interactions': {'views': avgViews, 'dislikes': avgDislikes}, 'Dislikes': avgDislikes,
                   'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioDislike[len(View_RatioDislike) // 2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioDislike2)):
            if View_RatioDislike2[i]['Dislikes'] != 0:
                temp_vals.append(View_RatioDislike2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Dislikes'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i + 1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 6:
                print(sortedResults[i].update(Rank='median'))
            elif i == 5:
                sortedResults[i].update(Rank='average')

        keys = list(sortedResults[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # DO DISLIKES HAVE A NEGATIVE IMPACT ON VIEWS? (Sorted by Views)
    def calculate_viewRatioViewDislikeSortedByViews(self):
        View_RatioDislike = self.collection.aggregate([
            {'$project':
                {
                    'Dislikes': {'$sum': '$interactions.dislikes'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.dislikes', '$interactions.views']}, 100]}]},
                    'interactions.dislikes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                },

            },
            {'$sort': {'interactions.dislikes': -1, 'interactions.views': -1}}
        ],
            allowDiskUse=True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        View_RatioDislike = sorted(View_RatioDislike, key=lambda x: x['Views'], reverse=True)
        View_RatioDislike2 = sorted(View_RatioDislike, key=lambda x: x['Views'], reverse=False)
        for i in range(len(View_RatioDislike)):
            sumRatio += View_RatioDislike[i]['Ratio']
            sumDislikes += View_RatioDislike[i]['Dislikes']
            sumLikes += View_RatioDislike[i]['Views']

        avgRatio = sumRatio / len(View_RatioDislike)
        avgDislikes = sumDislikes / len(View_RatioDislike)
        avgViews = sumLikes / len(View_RatioDislike)
        results = []
        global max_threshold
        for result in range(len(View_RatioDislike)):
            if result < max_threshold / 2:
                results.append(View_RatioDislike[result])
        average = {'interactions': {'views': avgViews, 'dislikes': avgDislikes}, 'Dislikes': avgDislikes,
                   'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioDislike[len(View_RatioDislike) // 2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioDislike2)):
            if View_RatioDislike2[i]['Views'] != 0 and View_RatioDislike2[i]['Ratio'] != 0:
                temp_vals.append(View_RatioDislike2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Views'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i + 1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 6:
                print(sortedResults[i].update(Rank='median'))
            elif i == 5:
                sortedResults[i].update(Rank='average')

        keys = list(sortedResults[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # Are Likes Relevant For views? (Sorted by Likes)
    def calculate_viewRatioViewLikeSortedByLikes(self):
        View_RatioLike = self.collection.aggregate([
            {'$project':
                {
                    'Likes': {'$sum': '$interactions.likes'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.likes', '$interactions.views']}, 100]}]},
                    'interactions.likes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'interactions.likes': -1, 'Ratio': -1}}
        ],
            allowDiskUse=True
        )
        avgRatio = 0
        avgLike = 0
        sumRatio = 0
        sumLike = 0
        sumViews = 0
        View_RatioLike = sorted(View_RatioLike, key=lambda x: x['Likes'], reverse=True)
        View_RatioLike2 = sorted(View_RatioLike, key=lambda x: x['Likes'], reverse=False)
        for i in range(len(View_RatioLike)):
            sumRatio += View_RatioLike[i]['Ratio']
            sumLike += View_RatioLike[i]['Likes']
            sumViews += View_RatioLike[i]['Views']
        avgRatio = sumRatio / len(View_RatioLike)
        avgLike = sumLike / len(View_RatioLike)
        avgViews = sumViews / len(View_RatioLike)

        results = []
        global max_threshold
        maxNew_threshold = 12
        for result in range(len(View_RatioLike)):
            if len(results) < max_threshold / 2 and View_RatioLike[result]['Ratio'] != View_RatioLike[result + 1]['Ratio']:
                results.append(View_RatioLike[result])
        average = {'interactions': {'views': avgViews, 'likes': avgLike}, 'Likes': avgLike, 'Views': avgViews,
                   'Ratio': avgRatio}
        median = View_RatioLike[len(View_RatioLike) // 2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioLike2)):
            if View_RatioLike2[i]['Likes'] != 0:
                temp_vals.append(View_RatioLike2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Likes'], reverse=True)
        print(sortedResults)

        print(sortedResults)

        for i in range(len(sortedResults)):
            if i < 5:
                sortedResults[i].update(Rank=i + 1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 6:
                print(sortedResults[i].update(Rank='median'))
            elif i == 5:
                sortedResults[i].update(Rank='average')

        keys = list(results[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # Are Likes Relevant For views? (Sorted by Views)
    def calculate_viewRatioViewLikeSortedByViews(self):
        View_RatioLike = self.collection.aggregate([
            {'$project':
                {
                    'Likes': {'$sum': '$interactions.likes'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.likes', '$interactions.views']}, 100]}]},
                    'interactions.likes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'interactions.views': -1, 'Ratio': -1}}
        ],
            allowDiskUse= True
        )
        avgRatio = 0
        avgLike = 0
        sumRatio = 0
        sumLike = 0
        sumViews = 0
        View_RatioLike = sorted(View_RatioLike, key=lambda x: x['Views'], reverse=True)
        View_RatioLike2 = sorted(View_RatioLike, key=lambda x: x['Views'], reverse=False)
        for i in range(len(View_RatioLike)):
            sumRatio += View_RatioLike[i]['Ratio']
            sumLike += View_RatioLike[i]['Likes']
            sumViews += View_RatioLike[i]['Views']
        avgRatio = sumRatio/len(View_RatioLike)
        avgLike = sumLike/len(View_RatioLike)
        avgViews = sumViews/len(View_RatioLike)

        results = []
        global max_threshold
        for result in range(len(View_RatioLike)):
            if result < max_threshold / 2:
                results.append(View_RatioLike[result])
        average = {'interactions': {'views': avgViews, 'likes': avgLike}, 'Likes': avgLike, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioLike[len(View_RatioLike)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioLike2)):
            if View_RatioLike2[i]['Views'] != 0:
                temp_vals.append(View_RatioLike2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Views'], reverse=True)
        print(sortedResults)
        print(sortedResults)
        for i in range(len(sortedResults)):
            if i < 5:
                sortedResults[i].update(Rank=i + 1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 6:
                print(sortedResults[i].update(Rank='median'))
            elif i == 5:
                sortedResults[i].update(Rank='average')

        keys = list(sortedResults[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # ARE LIKES RELEVANT FOR VIEWS? (Sorted by Ratio)
    def calculate_viewRatioViewLikeSortedByRatio(self):
        View_RatioLikeR = self.collection.aggregate([
            {'$project':
                {
                    'Likes': {'$sum': '$interactions.likes'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.likes', '$interactions.views']}, 100]}]},
                    'interactions.likes': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'Ratio': -1, 'interactions.views': -1}}
        ],
            allowDiskUse= True
        )
        avgRatio = 0
        avgLike = 0
        sumRatio = 0
        sumLike = 0
        sumViews = 0
        View_RatioLikeR = sorted(View_RatioLikeR, key=lambda x: x['Ratio'], reverse=True)
        View_RatioLike2R = sorted(View_RatioLikeR, key=lambda x: x['Ratio'], reverse=False)
        for i in range(len(View_RatioLikeR)):
            sumRatio += View_RatioLikeR[i]['Ratio']
            sumLike += View_RatioLikeR[i]['Likes']
            sumViews += View_RatioLikeR[i]['Views']
        avgRatio = sumRatio/len(View_RatioLikeR)
        avgLike = sumLike/len(View_RatioLikeR)
        avgViews = sumViews/len(View_RatioLikeR)

        results = []
        global max_threshold
        for result in range(len(View_RatioLikeR)):
            if result < max_threshold / 2:
                results.append(View_RatioLikeR[result])
        average = {'interactions': {'views': avgViews, 'likes': avgLike}, 'Likes': avgLike, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioLikeR[len(View_RatioLikeR)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)
        temp_vals = []
        for i in range(len(View_RatioLike2R)):
            if View_RatioLike2R[i]['Ratio'] != 0:
                temp_vals.append(View_RatioLike2R[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Ratio'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i+1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 5:
                print(sortedResults[i].update(Rank='average'))
            elif i == 6:
                sortedResults[i].update(Rank='median')

        keys = list(results[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # ARE COMMENTS RELEVANT FOR VIEWS (Sorted by Views)?
    def calculate_viewRatioViewCommentSortedByViews(self):
        View_RatioComment = self.collection.aggregate([
            {'$project':
                {
                    'Comment Count': {'$sum': '$interactions.comment_count'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.comment_count', '$interactions.views']}, 100]}]},
                    'interactions.comment_count': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'Ratio': -1, 'interactions.views': -1}}
        ],
            allowDiskUse= True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        sumComments = 0
        sumViews = 0
        View_RatioComment = sorted(View_RatioComment, key=lambda x: x['Views'], reverse=True)
        View_RatioComment2 = sorted(View_RatioComment, key=lambda x: x['Views'], reverse=False)
        for i in range(len(View_RatioComment)):
            sumRatio += View_RatioComment[i]['Ratio']
            sumComments += View_RatioComment[i]['Comment Count']
            sumViews += View_RatioComment[i]['Views']
        avgRatio = sumRatio/len(View_RatioComment)
        avgComments = sumComments/len(View_RatioComment)
        avgViews = sumViews/len(View_RatioComment)
        results = []
        global max_threshold
        for result in range(len(View_RatioComment)):
            if result < max_threshold / 2:
                results.append(View_RatioComment[result])
        average = {'interactions': {'views': avgViews, 'comment_count': avgComments}, 'Comment Count': avgComments, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioComment[len(View_RatioComment)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)

        temp_vals = []
        for i in range(len(View_RatioComment2)):
            if View_RatioComment2[i]['Views'] != 0:
                temp_vals.append(View_RatioComment2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Views'], reverse=True)
        for i in range(len(sortedResults)):
            if i < 5:
                sortedResults[i].update(Rank=i+1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 5:
                print(sortedResults[i].update(Rank='average'))
            elif i == 6:
                sortedResults[i].update(Rank='median')

        keys = list(results[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # ARE COMMENTS RELEVANT FOR VIEWS (Sorted by Ratio)?
    def calculate_viewRatioViewCommentSortedByRatio(self):
        View_RatioComment = self.collection.aggregate([
            {'$project':
                {
                    'Comment Count': {'$sum': '$interactions.comment_count'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.comment_count', '$interactions.views']}, 100]}]},
                    'interactions.comment_count': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'Ratio': -1, 'interactions.views': -1}}
        ],
            allowDiskUse= True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        sumComments = 0
        sumViews = 0
        View_RatioComment = sorted(View_RatioComment, key=lambda x: x['Ratio'], reverse=True)
        View_RatioComment2 = sorted(View_RatioComment, key=lambda x: x['Ratio'], reverse=False)
        for i in range(len(View_RatioComment)):
            sumRatio += View_RatioComment[i]['Ratio']
            sumComments += View_RatioComment[i]['Comment Count']
            sumViews += View_RatioComment[i]['Views']
        avgRatio = sumRatio/len(View_RatioComment)
        avgComments = sumComments/len(View_RatioComment)
        avgViews = sumViews/len(View_RatioComment)
        results = []
        global max_threshold
        for result in range(len(View_RatioComment)):
            if result < max_threshold / 2:
                results.append(View_RatioComment[result])
        average = {'interactions': {'views': avgViews, 'comment_count': avgComments}, 'Comment Count': avgComments, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioComment[len(View_RatioComment)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)

        temp_vals = []
        for i in range(len(View_RatioComment2)):
            if View_RatioComment2[i]['Ratio'] != 0:
                temp_vals.append(View_RatioComment2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Ratio'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i+1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 5:
                print(sortedResults[i].update(Rank='average'))
            elif i == 6:
                sortedResults[i].update(Rank='median')

        keys = list(results[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # ARE COMMENTS RELEVANT FOR VIEWS (Sorted by Comment Count)?
    def calculate_viewRatioViewCommentSortedByComments(self):
        View_RatioComment = self.collection.aggregate([
            {'$project':
                {
                    'Comment Count': {'$sum': '$interactions.comment_count'},
                    'Views': {'$sum': '$interactions.views'},
                    'Ratio': {'$cond': [{'$eq': ['$interactions.views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$interactions.comment_count', '$interactions.views']}, 100]}]},
                    'interactions.comment_count': 1,
                    'interactions.views': 1,
                    '_id': 0,
                }
            },
            {'$sort': {'interactions.comment_count': -1, 'Ratio': -1}}
        ],
            allowDiskUse= True
        )
        sumRatio = 0
        sumDislikes = 0
        sumLikes = 0
        sumComments = 0
        sumViews = 0
        View_RatioComment = sorted(View_RatioComment, key=lambda x: x['Comment Count'], reverse=True)
        View_RatioComment2 = sorted(View_RatioComment, key=lambda x: x['Comment Count'], reverse=False)
        for i in range(len(View_RatioComment)):
            sumRatio += View_RatioComment[i]['Ratio']
            sumComments += View_RatioComment[i]['Comment Count']
            sumViews += View_RatioComment[i]['Views']
        avgRatio = sumRatio/len(View_RatioComment)
        avgComments = sumComments/len(View_RatioComment)
        avgViews = sumViews/len(View_RatioComment)
        results = []
        global max_threshold
        for result in range(len(View_RatioComment)):
            if result < max_threshold / 2:
                results.append(View_RatioComment[result])
        average = {'interactions': {'views': avgViews, 'comment_count': avgComments}, 'Comment Count': avgComments, 'Views': avgViews, 'Ratio': avgRatio}
        median = View_RatioComment[len(View_RatioComment)//2]
        print(median)
        print(average)
        results.append(dict(average))
        results.append(median)

        temp_vals = []
        for i in range(len(View_RatioComment2)):
            if View_RatioComment2[i]['Comment Count'] != 0:
                temp_vals.append(View_RatioComment2[i])

        for i in range(len(temp_vals)):
            if i < max_threshold / 2:
                results.append(temp_vals[i])

        sortedResults = sorted(results, key=lambda k: k['Comment Count'], reverse=True)
        for i in range(len(sortedResults)):

            if i < 5:
                sortedResults[i].update(Rank=i+1)
            elif i > 6:
                sortedResults[i].update(Rank='last')
            elif i == 5:
                print(sortedResults[i].update(Rank='average'))
            elif i == 6:
                sortedResults[i].update(Rank='median')

        keys = list(results[0].keys())
        keys.remove('interactions')
        return sortedResults, keys

    # DO VIEWS DEPEND ON CHANNEL SETTINGS
    # TODO: What should we do with this method?
    """
    def calculate_imppactOfSettingsOnViews(self):

        cfrf = self.collection.count_documents({'settings.comments_disabled': False, 'settings.ratings_disabled': False})
        cfrt = self.collection.count_documents({'settings.comments_disabled': False, 'settings.ratings_disabled': True})
        ctrf = self.collection.count_documents({'settings.comments_disabled': True, 'settings.ratings_disabled': False})
        ctrt = self.collection.count_documents({'settings.comments_disabled': True, 'settings.ratings_disabled':True})

        pipe_cfrf = [{'$match': {'settings.comments_disabled': False, 'settings.ratings_disabled': False}},
                     {'$group': {'_id': None, 'Views': {'$sum': '$interactions.views'}}}]
        pipe_cfrt = [{'$match': {'settings.comments_disabled': False, 'settings.ratings_disabled': True}},
                     {'$group': {'_id': None, 'Views': {'$sum': '$interactions.views'}}}]
        pipe_ctrf = [{'$match': {'settings.comments_disabled': True, 'settings.ratings_disabled': False}},
                     {'$group': {'_id': None, 'Views': {'$sum': '$interactions.views'}}}]
        pipe_ctrt = [{'$match': {'settings.comments_disabled': True, 'settings.ratings_disabled': True}},
                     {'$group': {'_id': None, 'Views': {'$sum': '$interactions.views'}}}]

        views_of_cfrf = self.collection.aggregate(pipeline=pipe_cfrf)
        resultCFRF = list(views_of_cfrf)
        try:
            resultCFRF[0].update({"_id": "Comments and Ratings enabled"});
            print(resultCFRF)
        except IndexError:
            print("Problem with CFRF. No results found")
            resultCFRF.append({"_id": "Comments and Ratings enabled", "Views": "0"})
        views_of_cfrt = self.collection.aggregate(pipeline=pipe_cfrt)
        resultCFRT = list(views_of_cfrt)
        try:
            resultCFRT[0].update({"_id": "Comments enabled and Ratings disabled"})
            print(resultCFRT)
        except IndexError:
            print("Problem with CFRT. No results found.")
            resultCFRT.append({"_id": "Comments enabled and Ratings disabled", "Views": "0"})
        views_of_ctrf = self.collection.aggregate(pipeline=pipe_ctrf)
        resultCTRF = list(views_of_ctrf)
        try:
            resultCTRF[0].update({"_id": "Comments disabled and Ratings enabled"})
            print(resultCTRF)
        except IndexError:
            print("Problem with CTRG. No results found.")
            resultCTRF.append({"_id": "Comments disabled and Ratings enabled", "Views": "0"})
        views_of_ctrt = self.collection.aggregate(pipeline=pipe_ctrt)
        resultCTRT = list(views_of_ctrt)
        try:
            resultCTRT[0].update({"_id": "Comments and Ratings disabled"})
        except IndexError:
            print("Problem with CTRT. No results found.")
            resultCTRT.append({"_id": "Comments and Ratings disabled", "Views": "0"})

        resultList = list()
        resultList.extend(resultCTRF)
        resultList.extend(resultCTRT)
        resultList.extend(resultCFRT)
        resultList.extend(resultCFRF)
        keys = list(resultList[0].keys())
        print(resultList)
        print(keys)
        return resultList, keys


    def test(self):
        test = self.categories.aggregate([
        {'$lookup':
            {
                'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
            }
        },
        {'$unwind': '$category'},
        ])
        for item in test:
            print(item)
    """


    '''CATEGORY'''

    # WHICH CATEGORY HAS THE MOST DISLIKES COMPARED TO VIEWS?
    def calculate_categoryMostDislikesComparedToViews(self):
        Category_MostDislikesComparedToViews = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                 {
                     'path': '$category',
                     'preserveNullAndEmptyArrays': False
                 }
            },
            {'$group': {
                '_id': '$name',
                'Dislikes': {'$sum': '$category.interactions.dislikes'},
                'Views': {'$sum': '$category.interactions.views'},
            }
            },
            {'$project':
                    {
                        'Ratio': {'$cond': [{'$eq': ['$Views', 0]}, 'N/A', {
                            '$multiply': [{'$divide': ['$Dislikes', '$Views']}, 100]}]},
                        'Dislikes': 1,
                        'Views': 1
                    }
            },
            {'$sort': {'Ratio': -1}}
        ])
        results = list(Category_MostDislikesComparedToViews)
        keys = list(results[0].keys())
        return results, keys



    # WHICH CATEGORY HAS THE MOST LIKES COMPARED TO VIEWS?
    def calculate_categoryMostLikesComparedToViews(self):
        Category_MostLikesComparedToViews = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                {
                    'path': '$category',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {'$group': {
                '_id': '$name',
                'Likes': {'$sum': '$category.interactions.likes'},
                'Views': {'$sum': '$category.interactions.views'}
            }
            },
            {'$project':
                {
                    'Ratio': {'$cond': [{'$eq': ['$Views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$Likes', '$Views']}, 100]}]},
                    'Likes': 1,
                    'Views': 1,
                }
            },
            {'$sort': {'Ratio': -1}}
        ])

        results = list(Category_MostLikesComparedToViews)
        keys = list(results[0].keys())
        return results, keys




    # WHICH CATEGORY HAS THE MOST COMMENTS COMPARED TO VIEWS?
    def calculate_categoryMostCommentsComparedToViews(self):
        Category_MostCommentsComparedToViews = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                {
                    'path': '$category',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {'$group': {
                '_id': '$name',
                'Comments': {'$sum': '$category.interactions.comment_count'},
                'Views': {'$sum': '$category.interactions.views'}
            }
            },
            {'$project':
                {
                    'Ratio': {'$cond': [{'$eq': ['$Views', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$Comments', '$Views']}, 100]}]},
                    'Comments': 1,
                    'Views': 1,
                }
            },
            {'$sort': {'Ratio': -1}}
        ])

        results = list(Category_MostCommentsComparedToViews)
        keys = list(results[0].keys())
        return results, keys



    # WHICH CATEGORY GETS THE MOST VIEWS PER VIDEO?
    def calculate_categoryMostViewsPerVideo(self):
        Category_MostViewsPerVideo = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                {
                    'path': '$category',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {'$group': {
                '_id': '$name',
                'Videos': {'$sum': 1},
                'Views': {'$sum': '$category.interactions.views'}
            }
            },
            {'$project':
                {
                    'Ratio': {'$cond': [{'$eq': ['$Videos', 0]}, 'N/A',
                        {'$divide': ['$Views', '$Videos']}]},
                    'Videos': 1,
                    'Views': 1,
                }
            },
            {'$sort': {'Ratio': -1}}
        ])

        results = list(Category_MostViewsPerVideo)
        keys = list(results[0].keys())
        print(keys)
        return results, keys




    # WHICH CATEGORY HAS THE BEST RATIO BETWEEN LIKES AND DISLIKES?
    def calculate_categoryBestLikeDislikeRatio(self):
        Category_BestLikeDislikeRatio = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                {
                    'path': '$category',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {'$group': {
                '_id': '$name',
                'Likes': {'$sum': '$category.interactions.likes'},
                'Dislikes': {'$sum': '$category.interactions.dislikes'}
            }
            },
            {'$project':
                {
                    'Ratio': {'$cond': [{'$eq': ['$Likes', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$Dislikes', '$Likes']}, 100]}]},
                    'Dislikes': 1,
                    'Likes': 1,
                }
            },
            {'$sort': {'Ratio': 1}}
        ])

        results = list(Category_BestLikeDislikeRatio)
        keys = list(results[0].keys())
        print(keys)
        return results, keys



    # WHICH CATEGORY HAS THE HIGHEST AMOUNT OF UPLOADS?
    def calculate_categoryMostUploads(self):
        Category_MostUploads = self.categories.aggregate([
            {'$match': {}},
            {'$lookup':
                {
                    'from': 'videos', 'localField': '_id', 'foreignField': 'category_id', 'as': 'category'
                }
            },
            {'$unwind':
                {
                    'path': '$category',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {'$group': {
                '_id': '$name',
                'Videos': {'$sum': 1}
            }
            },
            {'$sort': {'Videos': -1}}
        ])

        results = list(Category_MostUploads)
        keys = list(results[0].keys())
        print(keys)
        return results, keys




    '''INTERACTIONS'''

    # WHAT IS THE GENERAL RATIO BETWEEN LIKES AND DISLIKES?
    def calculate_interactionLikeDislikeRatio(self):
        Interaction_LikeDislikeRatio = self.collection.aggregate([
            {'$match': {}},
            {'$group': {
                '_id': None,
                'Dislikes': {'$sum': '$interactions.dislikes'},
                'Likes': {'$sum': '$interactions.likes'}
            }
            },
            {'$project':
                {
                    'Dislikes': {'$sum': '$interactions.dislikes'},
                    'Likes': {'$sum': '$interactions.likes'},
                    'Ratio': {'$cond': [{'$eq': ['$Likes', 0]}, 'N/A', {
                        '$multiply': [{'$divide': ['$Dislikes', '$Likes']}, 100]}]},
                    'Dislikes': 1,
                    'Likes': 1,
                }
            },
            {'$sort': {'Ratio': 1}}
        ])

        """for result in Interaction_LikeDislikeRatio:
            print(result)

        """
        results = list(Interaction_LikeDislikeRatio)
        keys = list(results[0].keys())
        print(keys)
        del results[0]["_id"]
        keysWithoutID = list(results[0].keys())
        print(keysWithoutID)
        return results, keysWithoutID

if __name__ == '__main__':
    ql = QueryLogic()
    ql.calculate_viewRatioViewComment()