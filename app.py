from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='9a613ea82541832497a318e0e0472d3fe96c77899d97537c33fbea6016ee06ee'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vgqgkfvkgnvqce:f42eab86ddc59280e42241c23077adb2319cb2203f5be6cb4a3033aef83a668b@ec2-184-73-249-9.compute-1.amazonaws.com:5432/d10cjj7l4rg7p1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    # group = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, comments):
        self.customer = customer
        self.comments = comments
        # self.group = group


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        comments = request.form['comments']
        # group = request.form['group']
        if customer == '':
            flash('Please enter required fields','danger')
            return redirect(url_for('index'))
        
        if db.session.query(Feedback).filter(Feedback.customer == customer).count()==0:
            data = Feedback(customer,comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        flash('You have already submitted.','warning')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()