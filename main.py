import flask
from flask import Flask, request
from flask_restful import Api, Resource
from file_manipulator import fill_array, find_by_geonameid, geonames_on_pages, find_by_ru_names, find_by_part

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

api = Api()


class Main(Resource):
    def get(self):
        args = request.args.to_dict()
        if 'geonameid' in args:  # поиск города по geonameid
            return flask.jsonify(find_by_geonameid(args['geonameid']))
        elif 'page' in args and 'count' in args:  # построение страниц с городами
            return flask.jsonify(geonames_on_pages(int(args['page']), int(args['count'])))
        elif 'name1' in args and 'name2' in args:  # информация о двух городах
            return flask.jsonify(find_by_ru_names(args['name1'], args['name2']))
        elif 'part' in args:  # поиск похожих названий по части названия
            return flask.jsonify(find_by_part(args['part']))
        else:  # если режим не был определен
            return {"message": "it was not possible to set the operating mode"}


api.add_resource(Main, "/api/v1/ru")
api.init_app(app)


if __name__ == '__main__':
    fill_array()
    app.run(debug=True, port=8000, host='127.0.0.1')







