from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
# new added for success
from flask import render_template
from datetime import datetime
# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='harshithbhaskar'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/farmers'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class Farming(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    farmingtype=db.Column(db.String(100))


class Addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    farmername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.String(50))
    address=db.Column(db.String(50))
    farming=db.Column(db.String(50))

# transaction added by us:
# Add this to your existing models in app.py
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    addr = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class addtocart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
# heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(255), nullable=False)
    productdesc = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
# ////////////////////////////////////////////////////////

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/farmerdetails')
@login_required
def farmerdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=Register.query.all()
    return render_template('farmerdetails.html',query=query)

@app.route('/agroproducts')
def agroproducts():
    # query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    query=Addagroproducts.query.all()
    return render_template('agroproducts.html',query=query)

@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=Addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')


   
# Initial empty list of products

products = []

from flask import render_template, redirect, url_for

@app.route('/addtocart', methods=['POST'])
def addtocart():
    # Get product details submitted by the user
    pid = request.args.get('pid', type=int)

    # Find the product with the given ID in the database
    product = Addagroproducts.query.filter_by(pid=pid).first()

    if product:
        # Add the product to the cart in the database (you may need to create a Cart model)
        # cart_item = addtocart(Addagroproducts=product.pid, user_id=id)  # Adjust this based on your User model
        cart_item = Product(pid=pid)
        db.session.add(cart_item)
        # db.session.commit()

        # Render the cart page
        return render_template('carts.html', product=product)
    else:
        return jsonify({"error": "Product not found"}), 404



# @app.route('/addtocart', methods=['POST'])
# def addtocart():
#     # Get product details submitted by the user
#     pid = request.args.get('pid', type=int)

#     # Find the product with the given ID in the database
#     product = Addagroproducts.query.filter_by(pid=pid).first()

#     if product:
#         # Return the product details as HTML
#         return render_template('addtocart.html', product=product)
#     else:
#         # Return an error if the product is not found
#         return jsonify({"error": "Product not found"}), 404


@app.route('/getproductdetails')
def get_product_details_route():
    # Fetch the product details using the provided product ID (adjust as needed)
    product_id = request.args.get('pid', type=int)
    product = Product.query.get(product_id)

    if product:
        return render_template('carts.html', product=product)
    else:
        return jsonify({"error": "Product not found"}), 404


# tillllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
@app.route('/triggers')
@login_required
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/addfarming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/addfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Addes","success")
    return render_template('farming.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    # db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    post=Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/farmerdetails')


@app.route("/edit/<string:rid>",methods=['POST','GET'])
@login_required
def edit(rid):
    # farming=db.engine.execute("SELECT * FROM `farming`") 
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        # query=db.engine.execute(f"UPDATE `register` SET `farmername`='{farmername}',`adharnumber`='{adharnumber}',`age`='{age}',`gender`='{gender}',`phonenumber`='{phonenumber}',`address`='{address}',`farming`='{farmingtype}'")
        post=Register.query.filter_by(rid=rid).first()
        print(post.farmername)
        post.farmername=farmername
        post.adharnumber=adharnumber
        post.age=age
        post.gender=gender
        post.phonenumber=phonenumber
        post.address=address
        post.farming=farmingtype
        db.session.commit()
        flash("Slot is Updated","success")
        return redirect('/farmerdetails')
    posts=Register.query.filter_by(rid=rid).first()
    farming=Farming.query.all()
    return render_template('edit.html',posts=posts,farming=farming)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/register',methods=['POST','GET'])
@login_required
def register():
    farming=Farming.query.all()
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=Register(farmername=farmername,adharnumber=adharnumber,age=age,gender=gender,phonenumber=phonenumber,address=address,farming=farmingtype)
        db.session.add(query)
        db.session.commit()
        # query=db.engine.execute(f"INSERT INTO `register` (`farmername`,`adharnumber`,`age`,`gender`,`phonenumber`,`address`,`farming`) VALUES ('{farmername}','{adharnumber}','{age}','{gender}','{phonenumber}','{address}','{farmingtype}')")
        # flash("Your Record Has Been Saved","success")
        return redirect('/farmerdetails')
    return render_template('farmer.html',farming=farming)

# traansction
@app.route('/transaction/<int:pid>', methods=['POST'])
@login_required
def transaction(pid):
    if request.method == "POST":
        name = request.form.get('name')
        city = request.form.get('city')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        pincode = request.form.get('pincode')
        addr = request.form.get('addr')
        bid = current_user.id  # Assuming current_user has an 'id' attribute
        timestamp = datetime.utcnow()
        # Ensure 'name' is not None before inserting into the database
        if name is not None:
            # Perform the database insertion or any other processing as needed
            transaction = Transaction(bid=bid, pid=pid, name=name, city=city, mobile=mobile, email=email, pincode=pincode, addr=addr, timestamp =timestamp)
            db.session.add(transaction)
            db.session.commit()

            flash("Order Successfully placed! Thanks for shopping with us!!!", "success")
            return redirect(url_for('success'))  # Change 'success' to the appropriate route
        # else:
        #     flash("Error: Name cannot be null.", "danger")

    return render_template('transaction.html', pid=pid)


# class Transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bid = db.Column(db.Integer, nullable=False)
#     pid = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     city = db.Column(db.String(100), nullable=False)
#     mobile = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     pincode = db.Column(db.String(10), nullable=False)
#     addr = db.Column(db.String(300), nullable=False)

# def call_insert_transaction_stored_procedure(bid, pid, name, city, mobile, email, pincode, addr):
#     try:
#         # Call the stored procedure using SQLAlchemy
#         db.session.execute('CALL InsertTransaction(:bid, :pid, :name, :city, :mobile, :email, :pincode, :addr)',
#                            {'bid': bid, 'pid': pid, 'name': name, 'city': city, 'mobile': mobile, 'email': email,
#                             'pincode': pincode, 'addr': addr})
#         db.session.commit()
#         return True  # Indicate success
#     except Exception as e:
#         # Handle errors appropriately
#         print(f"Error calling stored procedure: {str(e)}")
#         db.session.rollback()
#         return False  # Indicate failure


@app.route('/success')
def success():
    return render_template('success.html')

# @app.route('/displayproducts')
# @login_required
# def display_products():
#     # Retrieve selected agricultural products for the current user
#     selected_products = addtocart.query.filter_by(bid=current_user.id).all()

#     # Retrieve product details for each selected product
#     products = []
#     for item in selected_products:
#         product = Addagroproducts.query.get(item.pid)
#         if product:
#             products.append(product)

#     return render_template('selected_products.html', products=products)

                                                                                                                                  
from flask import render_template, abort

# ...

@app.route('/productdetails/<int:pid>')
def product_details(pid):
    product = Addagroproducts.query.get(pid)

    if product:
        return render_template('product_details.html', product=product)
    else:
        abort(404)

# ...
# stored procedureeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
from sqlalchemy import text

@app.route('/call_stored_procedure', methods=['POST'])
@login_required
def call_stored_procedure():
    if request.method == "POST":
        name = request.form.get('name')
        city = request.form.get('city')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        pincode = request.form.get('pincode')
        addr = request.form.get('addr')
        bid = current_user.id
        timestamp = datetime.utcnow()
        pid = request.args.get('pid', type=int)  # Assuming you retrieve pid from request args

        try:
            # Call the stored procedure to insert the transaction
            db.session.execute(text('CALL InsertTransaction(:bid, :pid, :name, :city, :mobile, :email, :pincode, :addr, :timestamp)'),
                               {'bid': bid, 'pid': pid, 'name': name, 'city': city, 'mobile': mobile, 'email': email,
                                'pincode': pincode, 'addr': addr, 'timestamp': timestamp})
            db.session.commit()  # Commit the transaction if successful

            flash("Order Successfully placed! Thanks for shopping with us!!!", "success")
            return redirect(url_for('success'))  # Change 'success' to the appropriate route
        except Exception as e:
            # Handle errors appropriately
            flash("An error occurred while placing the order. Please try again later.", "danger")
            print(f"Error calling stored procedure: {str(e)}")
            db.session.rollback()  # Roll back the transaction if an error occurs
            return redirect(url_for('transaction', pid=pid))  
# stored procedureee endssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

# from here original
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    
