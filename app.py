from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)



#database 
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False,default= datetime.utcnow)
    description = db.Column(db.String(200), nullable = False)
    credit = db.Column(db.Float, nullable = True)
    debit = db.Column(db.Float, nullable = True)
    balance = db.Column(db.Float, nullable = False)
    


with app.app_context():
    db.create_all()



#routes for Transactions
@app.route('/',methods = ['get'])
def index():
    return render_template('index.html')


@app.route('/transaction',methods = ['GET' , 'POST'])
def transaction():
    if request.method == 'POST':
        description = request.form['description']      
        credit = float(request.form.get('credit', 0))
        debit = float(request.form.get('debit', 0))
        if credit == 0 and debit == 0:
            return 'Credit of Debit amount must be provided'
        latest_transaction = Transaction.query.order_by(Transaction.date.desc()).first()
        if latest_transaction:
            balance = latest_transaction.balance + credit - debit
        else:
            balance = credit - debit
        new_transaction = Transaction(description = description , credit = credit ,debit = debit, balance = balance)
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('transactions'))
    return render_template('transaction.html')


@app.route('/transactions')
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions = transactions)







if __name__ == '__main__':
    app.run(debug=True)