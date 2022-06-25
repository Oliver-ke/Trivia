import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def make_pagination(req, selection):
    page = req.args.get("page", 1, type=int)
    pg_start = (page - 1) * QUESTIONS_PER_PAGE
    pg_end = pg_start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    pg_questions = questions[pg_start:pg_end]

    return pg_questions


def make_category_obj(categories):
    category_obj = {}
    for category in categories:
        formatted_category = category.format()
        id = formatted_category["id"]
        category_obj[id] = formatted_category["type"]
    return category_obj


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        category_payload = make_category_obj(categories)
        return jsonify(
            {
                "success": True,
                "categories": category_payload,
            }
        )

    @app.route("/questions", methods=["GET"])
    def get_questions():
        categories = Category.query.order_by(Category.id).all()
        category_payload = make_category_obj(categories)

        questions = Question.query.order_by(Question.id).all()
        current_questions = make_pagination(request, questions)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": category_payload,
                "current_category": "All",
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()
            questions = Question.query.order_by(Question.id).all()
            questions_list = make_pagination(request, questions)

            categories = Category.query.order_by(Category.id).all()
            category_payload = make_category_obj(categories)

            return jsonify(
                {
                    "success": True,
                    "questions": questions_list,
                    "total_questions": len(questions),
                    "categories": category_payload,
                    "current_category": "All",
                }
            )

        except Exception as e:
            print(e.args)
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        payload = request.get_json()

        question = payload.get("question", None)
        answer = payload.get("answer", None)
        category = payload.get("category", None)
        difficulty = payload.get("difficulty", None)

        category_exist = Category.query.filter(Category.id == category).one_or_none()

        if category_exist is None:
            abort(400)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )

            new_question.insert()
            questions = Question.query.order_by(Question.id).all()
            pag_question_array = make_pagination(request, questions)

            categories = Category.query.order_by(Category.id).all()
            category_payload = make_category_obj(categories)

            return jsonify(
                {
                    "success": True,
                    "questions": pag_question_array,
                    "total_questions": len(questions),
                    "categories": category_payload,
                    # "added": new_question.format(),
                    "current_category": "All",
                }
            )

        except:
            abort(422)

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        payload = request.get_json()
        search_term = payload.get("searchTerm", "")
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))
            )

            pag_question_array = make_pagination(request, selection)
            return jsonify(
                {
                    "success": True,
                    "questions": pag_question_array,
                    "total_questions": len(selection.all()),
                    "current_category": "All",
                }
            )
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_question_by_category(category_id):
        try:
            # get current category
            category = Category.query.filter(Category.id == category_id).one_or_none()
            selection = Question.query.order_by(Question.id).filter(
                Question.category == category_id
            )
            pag_question_array = make_pagination(request, selection)

            return jsonify(
                {
                    "success": True,
                    "questions": pag_question_array,
                    "total_questions": len(selection.all()),
                    "current_category": category.type,
                }
            )
        except:
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        payload = request.get_json()
        previous_questions = payload.get("previous_questions", [])
        quiz_category = payload.get("quiz_category", None)
        selection = []
        if quiz_category["type"] == "All":
            selection = Question.query.order_by(Question.id).all()
        else:
            selection = Question.query.order_by(Question.id).filter(
                Question.category == quiz_category["id"]
            )
        questions = [question.format() for question in selection]
        # filter to removed previous questions
        result = [q for q in questions if q["id"] not in previous_questions]

        max_idx = 0 if len(result) == 0 else len(result) - 1
        question_idx = max_idx

        if max_idx > 0:
            # generate random number if item is not the last
            question_idx = random.randint(0, max_idx)
        question = "" if max_idx == 0 else result[question_idx]
        return jsonify({"success": True, "question": question})

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_input(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad input"}),
            400,
        )

    return app
