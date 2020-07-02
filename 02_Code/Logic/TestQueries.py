from Logic.QueryLogic import QueryLogic

# OBJECT CREATION OF QUERY LOGIC
ql = QueryLogic()



'''VIEWS'''

# DO DISLIKES HAVE A NEGATIVE IMPACT ON VIEWS?
#ql.calculate_viewRatioViewDislike()

# Are Likes relevant for views? (Sorted by Likes)
ql.calculate_viewRatioViewLikeSortedByLikes()
# ARE LIKES RELEVANT FOR VIEWS? (Sorted by Ratio)
#ql.calculate_viewRatioViewLikeSortedByRatio()

# Are likes relevant for views? (Sorted by Likes)
#ql.calculate_viewRatioViewLikeSortedByViews()

# ARE COMMENTS RELEVANT FOR VIEWS?
#ql.calculate_viewRatioViewComment()


# DO VIEWS DEPEND ON CHANNEL SETTINGS
#ql.calculate_imppactOfSettingsOnViews()



'''CATEGORY'''
#JOIN TEST
#ql.test()


# WHICH CATEGORY HAS THE MOST DISLIKES COMPARED TO VIEWS?
# ql.calculate_categoryMostDislikesComparedToViews()

# WHICH CATEGORY HAS THE MOST LIKES COMPARED TO VIEWS?
# ql.calculate_categoryMostLikesComparedToViews()

# WHICH CATEGORY HAS THE MOST COMMENTS COMPARED TO VIEWS?
# ql.calculate_categoryMostCommentsComparedToViews()

# WHICH CATEGORY GETS THE MOST VIEWS PER VIDEO?
# ql.calculate_categoryMostViewsPerVideo()

# WHICH CATEGORY HAS THE BEST RATIO BETWEEN LIKES AND DISLIKES?
#ql.calculate_categoryBestLikeDislikeRatio()

# WHICH CATEGORY HAS THE HIGHEST AMOUNT OF UPLOADS?
#ql.calculate_categoryMostUploads()



'''INTERACTIONS'''
# WHAT IS THE GENERAL RATIO BETWEEN LIKES AND DISLIKES?
#ql.calculate_interactionLikeDislikeRatio()