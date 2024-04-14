import numpy as np
from flask import Flask,render_template,request
import pickle
import pandas as pd


popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
content = pickle.load(open('content.pkl', 'rb'))
books2 = pickle.load(open('contentwn.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))


app = Flask(__name__)

@app.route('/',methods=["GET"])
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html', booklist2 = list(books['Book-Title'].values))

@app.route('/recommend',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    data=[]
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:

        return render_template('recommend.html', ver=1)  # Adjust the template name as needed

    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:8]
    print(similar_items)

    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    try:
        index = books2[books2['Book-Title'] == user_input].index[0]
    except IndexError:
        return render_template('recommend.html', ver=1)  # Adjust the template name as needed

    distances = sorted(list(enumerate(content[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        item = []
        temp_df = books[books['Book-Title'] == books2.iloc[i[0]]["Book-Title"]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        print(item)
        print(books2.iloc[i[0]]["Book-Title"])
        data.append(item)

    data2 = []
    [data2.append(item) for item in data if item not in data2]

    return render_template('recommend.html', data=data2, booklist2= list(books['Book-Title'].values))



if __name__ == '__main__':
    app.run(debug=True)