from flask import Flask,render_template,request,redirect
import pandas as pd
import numpy as np
import random

app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    global F,L
    F=0
    L=50
    return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])

@app.route('/nextlist')
def indexN():  # put application's code here
    global F,L
    try:
        if(L<2000):
            F += 50
            L += 50
    except:
        F=0
        L=50
    return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])

@app.route('/previouslist')
def indexP():  # put application's code here
    global F,L
    try:
        if(F>49):
            F -= 50
            L -= 50
    except:
        F=0
        L=50
    return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])

@app.route('/movie',methods=["POST","GET"])
def movie():
    global F,L
    link = request.form['link']
    if link=="nan":
        try:
            return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])
        except:
            F=0
            L=50
            return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])
    return redirect(link, code=302)


def recommend(movie):
    Temp = pd.read_csv('static/HomePageDataSet.csv')
    try:
        movie_index = Temp[Temp['original_title'] == movie].index[0]
        distances = np.load("static/similarity.npy")[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        RData = []
        for i in movie_list:
            RData.append(Temp.iloc[i[0]]["original_title"])
        return RData[:15]
    except:
        TempI = Temp[Temp.vote_average > 7].index
        TempI = Temp.iloc[TempI[random.randint(1, len(TempI) - 50):][:15]]["original_title"]
        return list(TempI.values)

def MakeCapital(word):
    temp = []
    for i in word.split(" "):
        T = []
        Flag=True
        for j in i:
            if Flag:
                Flag=False
                T.append(j.upper())
            else:
                T.append(j)
        temp.append("".join(T))
    temp = " ".join(temp)
    return temp

@app.route('/recommend',methods=["POST","GET"])
def predict():
    global F,L
    data = pd.read_csv('static/HomePageDataSet.csv')
    keyword = request.form["search"]
    if keyword.strip()=="":
        try:
            return render_template('Arcon Theater.html', data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])
        except:
            F=0
            L=50
            return render_template('Arcon Theater.html', data=pd.read_csv('static/HomePageDataSet.csv').values[F:L])
    RD = recommend(MakeCapital(keyword))
    Rdata = []
    for i in RD:
        Temp = []
        for j in data.columns:
            Temp.append(data[data["original_title"] == i][j].values[0])
        Rdata.append(Temp)
    try:
        return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L],suggestion=True,Rdata=Rdata)
    except:
        F=0
        L=50
        return render_template('Arcon Theater.html',data=pd.read_csv('static/HomePageDataSet.csv').values[F:L],suggestion=True,Rdata=Rdata)

if __name__ == '__main__':
    app.run(debug=True)
