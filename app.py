from email import message
from flask import Flask, render_template, jsonify
from paystackapi.subaccount import SubAccount
from paystackapi.paystack import Paystack
from paystackapi.transaction_split import TransactionSplit
import os

paystack_secret_key = os.environ.get('PAYSTACK_SECRET_KEY')
transaction_charges = os.environ.get('TRANSACTION_CHARGE')
paystack = Paystack(secret_key=paystack_secret_key)

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/create_account')
def create_sub_account():
    response = SubAccount.create(
        business_name="Another biz account",
        settlement_bank="Ecobank Nigeria",
        account_number="2260002520",
        percentage_charge=transaction_charges
    )
    print(response)
    if response.status == False:
        message = 'An error occured'
        return(jsonify(message))
    if response.status == True:
        return render_template('account_created.html')

@app.route('/get_accounts')
def get_sub_accounts():
    response = SubAccount.list(
        perPage=3, 
        page=1
    )
    print(response)
    return(jsonify(response))

@app.route('/init_split_pay')
def init_split_pay():
    response = TransactionSplit.create(
            name="Another biz account",
            type="percentage",
            currency="NGN",
            subaccount= 'ACCT_rk87ysu3o4tbq7k',
            bearer_type="subaccount"
        )
    print(response)
    return jsonify(response)
    if response.status == False:
        message = 'An error occured'
        return(jsonify(message))
    if response.status == True:
        return jsonify(response)

"""
https://pypi.org/project/paystackapi/

https://github.com/andela-sjames/paystack-python/tree/master/docs


Successful response code looks like this:

{'status': True, 'message': 'Subaccount created', 'data': {'business_name': 'Another biz account', 'account_number': '2260002520', 'percentage_charge': 10, 'settlement_bank': 'Ecobank Nigeria', 'currency': 'NGN', 'bank': 4, 'integration': 424236, 'domain': 'test', 'subaccount_code': 'ACCT_rk87ysu3o4tbq7k', 'is_verified': False, 'settlement_schedule': 'AUTO', 'active': True, 'migrate': False, 'id': 590045, 'createdAt': '2022-09-04T22:33:32.113Z', 'updatedAt': '2022-09-04T22:33:32.113Z'}}


- Once sub account is created, we add "subaccount_code", "settlement_bank" to vendors database
, To create transaction split, we first

"""



    
