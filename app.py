from flask import Flask, render_template, make_response, request, jsonify
from bs4 import BeautifulSoup
import requests
from nlp import sentiment_score


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def home():
    """ Primary End Point """
    n_com = 100
    top_n = 10
    page = requests.get("https://news.ycombinator.com/newcomments")
    soup = BeautifulSoup(page.content, features='html.parser')
    com_scores = []
    usr_com = zip(soup.find_all('a', class_='hnuser')[:n_com],
                  soup.find_all('div', class_='comment')[:n_com])
    for usr, com in usr_com:
        score = sentiment_score(com.get_text())
        com_scores.append([usr.get_text(), score])
    com_scores.sort(key=lambda x: x[1], reverse=True)
    for idx in range(len(com_scores)):
        com_scores[idx].insert(0, idx+1)
    return render_template('index.html', data=com_scores[:top_n], num=top_n)


""" The following code is only required if this 
        API is called from a foreign server """
# @app.before_request
# def before_request():
#     """ CORS preflight """
#     def _build_cors_prelight_response():
#         response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "*")
#         response.headers.add("Access-Control-Allow-Methods", "*")
#         return response
#     if request.method == "OPTIONS":
#         return _build_cors_prelight_response()
#
#
# @app.after_request
# def after_request(response):
#     """ CORS headers """
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     return response


if __name__ == '__main__':
    app.run()
