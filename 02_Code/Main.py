#from QueryLogic import QueryLogic
import json

from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import logging
from Logic.QueryLogic import QueryLogic

#logger setup, use logger.info(or level needed)('Log message') to log
logging.basicConfig(filename='log.txt', level=logging.INFO, format='Class: %(name)s - Time: %(asctime)s - Level: %(levelname)s - Message: %(message)s')
logger = logging.getLogger('Main')


app = Flask(__name__)
app.config["SECRET_KEY"] = "DBSProject"
logic = QueryLogic()


class db_query_form(FlaskForm):
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Last Name:", validators=[DataRequired()])
    select = SelectField("Test", [DataRequired()], choices=[("Likes", "like"), ("Views of the video", "views")])
    submit = SubmitField("Submit")


class db_query_form_getResults(FlaskForm):
    select = SelectField("Wählen Sie eine Abfrage", [DataRequired()], choices=[("1", "Which category has the most dislikes compared to views?"),
                                                                  ("2", "Which category has the most likes compared to views?"),
                                                                  ("3", "Which category has the most comments compared to views?"),
                                                                  ("4", "Which category gets the most views per video?"),
                                                                  ("5", "Which category has the best ratio between likes and dislikes?"),
                                                                  ("6", "Which category has the highest ammount of uploads?"),
                                                                  ("7", 'Do dislikes have a negative impact on views? (Sorted by Ratio)'),
                                                                               ("16",
                                                                                'Do dislikes have a negative impact on views? (Sorted by Dislikes)'),
                                                                               ("17",
                                                                                'Do dislikes have a negative impact on views? (Sorted by Views)'),
                                                                  ("8", 'Are likes relevant for views? (Sorted by Ratio)'),
                                                                  ("12", "Are likes relevant for views? (Sorted by Views)"),
                                                                  ("13", "Are likes relevant for views? (Sorted by Likes)"),
                                                                  ("9", 'Are comments relevant for views? (Sorted by Ratio)'),
                                                                    ("14", 'Are comments relevant for views? (Sorted by Views)'),
                                                                               ("15", 'Are comments relevant for views? (Sorted by Comment Count)'),
                                                                  ### ("10", 'Do views depend on channel settings?'),
                                                                  ("11", 'What is the general ratio between likes and dislikes?')])
    submit = SubmitField("Auswerten")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/datenquelle")
def datasource():
    return render_template("datenquelle.html")


@app.route("/abfrage", methods=["GET", "POST"])
def abfrage():
    form = db_query_form()
    result =""
    if form.validate_on_submit():
        pass
        #hier kommt abfragelogik!
        result = "result of our query"

    return render_template("abfrage.html", form=form, result=result)


@app.route("/auswertung", methods=["GET", "POST"])
def auswertung():
    form = db_query_form_getResults()
    dataFound = "Error. Nothing found!"
    keys = "Im everytime here"
    keyForGraph = 'nothing'
    labelForGraph = 'nothing'
    result = ("hi", "there")

    if form.is_submitted():
        print("submitted")

    if form.validate_on_submit():
        print(form.select)
        if form.select.data == "1":
            result = logic.calculate_categoryMostDislikesComparedToViews()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        elif form.select.data == "2":
            result = logic.calculate_categoryMostLikesComparedToViews()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        elif form.select.data == "3":
            result = logic.calculate_categoryMostCommentsComparedToViews()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        elif form.select.data == "4":
            result = logic.calculate_categoryMostViewsPerVideo()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        elif form.select.data == "5":
            result = logic.calculate_categoryBestLikeDislikeRatio()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        elif form.select.data == "6":
            result = logic.calculate_categoryMostUploads()
            keyForGraph = 'Videos'
            labelForGraph = '_id'
        elif form.select.data == "7":
            result = logic.calculate_viewRatioViewDislikeSortedByRatio()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "16":
            result = logic.calculate_viewRatioViewDislikeSortedByDislikes()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "17":
            result = logic.calculate_viewRatioViewDislikeSortedByViews()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "8":
            result = logic.calculate_viewRatioViewLikeSortedByRatio()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "12":
            result = logic.calculate_viewRatioViewLikeSortedByViews()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "13":
            result = logic.calculate_viewRatioViewLikeSortedByLikes()
            keyForGraph = "Ratio"
            labelForGraph = 'Rank'
        elif form.select.data == "9":
            result = logic.calculate_viewRatioViewCommentSortedByRatio()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "14":
            result = logic.calculate_viewRatioViewCommentSortedByViews()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "15":
            result = logic.calculate_viewRatioViewCommentSortedByComments()
            keyForGraph = 'Ratio'
            labelForGraph = 'Rank'
        elif form.select.data == "11":
            result = logic.calculate_interactionLikeDislikeRatio()
            keyForGraph = 'Ratio'
            labelForGraph = '_id'
        """
        elif form.select.data == "10":
            result = logic.calculate_imppactOfSettingsOnViews()
            keyForGraph = 'Views'
            labelForGraph = '_id'
        """


    print(form.errors)
    return render_template("auswertung.html", form=form, dataFound=result[0], keys=result[1], keyForGraph=keyForGraph, labelForGraph=labelForGraph)


if __name__ == '__main__':
    app.run(port=1337, debug=True)

