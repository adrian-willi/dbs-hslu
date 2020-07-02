import csv
import json

csvFiles1 = ["DEvideos.csv", "FRvideos.csv", "GBvideos.csv"]
csvFiles = ["USvideos.csv"]
jsonFilePath = "USdata.json"

data = {}
videos = []


def obj_dict(obj):
    return obj.__dict__


class video:
    def __init__(self, video_id, title, publish_time, tags, category_id, description, comments_disabled, ratings_disabled, video_error_or_removed, likes, views, comment_count, dislikes, channel_title):
        self.video_id = video_id
        self.country = "US"
        self.title = title
        self.publish_time = publish_time
        self.tags = tags
        self.category_id = int(category_id)
        self.description = description
        self.settings = settings(comments_disabled, ratings_disabled, video_error_or_removed)
        self.interactions = interactions(likes, views, comment_count, dislikes)
        self.channel = channel(channel_title)

class settings:
    def __init__(self, comments_disabled, ratings_disabled, video_error_or_removed):
        self.comments_disabled = bool(comments_disabled)
        self.ratings_disabled = bool(ratings_disabled)
        self.video_error_or_removed = bool(video_error_or_removed)

class interactions:
    def __init__(self, likes, views, comment_count, dislikes):
        self.likes = int(likes)
        self.views = int(views)
        self.comment_count = int(comment_count)
        self.dislikes = int(dislikes)

class channel:
    def __init__(self, channel_title):
        self.channel_title = channel_title


for myCsvFile in csvFiles:
    with open(myCsvFile, newline='', encoding='utf-8') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            videos.append(video(rows['video_id'], rows['title'], rows['publish_time'], rows['tags'], rows['category_id'], rows['description'], rows['comments_disabled'], rows['ratings_disabled'], rows['video_error_or_removed'], rows['likes'], rows['views'], rows['comment_count'], rows['dislikes'], rows['channel_title']))



with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(videos, default=obj_dict, indent=4))