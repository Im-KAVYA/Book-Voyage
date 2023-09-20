from flask import Flask, render_template, request
import pickle
import pandas as pd

popular_50=pickle.load(open('popular.pkl','rb'))

cosine_sim_df=pickle.load(open('cosine_sim_df.pkl','rb'))
filtered_books=pickle.load(open('filtered_books.pkl','rb'))


app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html',
                           image=list(popular_50['Image-URL-M'].values),
                           book=list(popular_50['Book-Title'].values),
                           author=list(popular_50['Book-Author'].values),
                           votes=list(popular_50['Ratings_count'].values),
                           rating=list(popular_50['Ratings_mean'].values))

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend_books():
    book_name= request.form.get('book-input')
    distances_df = cosine_sim_df[book_name].sort_values(ascending=False).head(6)
    suggested_books = list(distances_df.index)
    suggested_books.remove(book_name)
    suggested_df = pd.DataFrame()
    for book in suggested_books:
        suggested_df = suggested_df.append(
            filtered_books[filtered_books['Book-Title'] == book][['Book-Title', 'Book-Author', 'Image-URL-M']])
    suggested_df.drop_duplicates('Book-Title', inplace=True)

    print(suggested_df.values)
    return render_template('recommend.html',data=suggested_df.values)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)
