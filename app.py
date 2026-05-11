from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')

def home():

    try:
        df = pd.read_csv("data.csv")

        male = int(df["Male"][0])
        female = int(df["Female"][0])
        children = int(df["Children"][0])

    except:
        male = female = children = 0

    total = male + female + children

    return render_template("index.html",
                           total=total,
                           male=male,
                           female=female,
                           children=children)

if __name__ == '__main__':
    app.run(debug=True)
