from flask import Flask, redirect, url_for, render_template, request
import random
import psycopg2
import re
# connection = psycopg2.connect(
#     host="10.17.5.97",
#     database="group_22",
#     user="group_22",
#     password="kzw90ZbIq7gCl",
#     port="5432"
# )

connection = psycopg2.connect(
    host="localhost",
    database="apnabazar",
    user="shrutikumari",
    password="skpostgres9"
)

cursor = connection.cursor()

app = Flask(__name__)

regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def emailcheck(email):
    if(re.search(regex_email,email)):
        return False
    else:
        return True

cats = ['Accessories', 'Bags', 'Beauty', 'House', 'Jewelry', 'Kids', 'Men', 'Shoes', 'Women']
filters = ['Price : Low to High', 'Price : High to Low','Discount : Low to High', 'Discount : High to Low','--Select--']
# @app.route('/<string:userid>/home', methods=['POST', 'GET'])
# def homePage():
#     if(request.method == 'POST'):
#         search = request.form['Search']
#         print(search)
#         return redirect('/search/key='+search)  
#     else:
#         #Get most popular and most discounted item details in 2 arrays and pass in render, also update the html file
#         return render_template('homepage.html', cats= cats)

# @app.route("/<string:userid>/home_temp")
# def home(userid):
#     return render_template('home.html', userid=userid)

@app.route("/<string:userid>/home")
def home(userid):
    cursor.execute(
                    f" select t.category, t.id, t.discount, t.likes_count, t.image_url, t.current_price, t.raw_price, t.name from \
                      (   (select category, id, discount, likes_count, image_url, current_price, raw_price, name from accessories order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from bags order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from beauty order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from house order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from jewelry order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from kids order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from men order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from shoes order by likes_count desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from women order by likes_count desc limit 3 ) \
                      ) as t \
                      order by t.likes_count desc \
                      limit 3;"
                  )
    popularItems = cursor.fetchall()
    cursor.execute(
                    f" select t.category, t.id, t.discount, t.likes_count, t.image_url, t.current_price, t.raw_price, t.name from \
                      (   (select category, id, discount, likes_count, image_url, current_price, raw_price, name from accessories order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from bags order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from beauty order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from house order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from jewelry order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from kids order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from men order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from shoes order by discount desc limit 3 ) \
                          union all \
                          (select category, id, discount, likes_count, image_url, current_price, raw_price, name from women order by discount desc limit 3 ) \
                      ) as t \
                      order by t.discount desc \
                      limit 3;"
                  )
    discountedItems = cursor.fetchall()
    return render_template('homepage.html', userid=userid, popularItems=popularItems, discountedItems=discountedItems, cats= cats)

@app.route("/<string:userid>/<string:category>/categorypage", methods=['POST', 'GET'])
def categorypage(userid, category):
    cursor.execute(f"select * from {category};")
    items = cursor.fetchall()
    if(request.method=='POST'):
        filter = request.form['filters']
        if(filter=='1'):
             cursor.execute(f"select * from {category} order by current_price;")
             items = cursor.fetchall()
        elif(filter=='2'):
             cursor.execute(f"select * from {category} order by current_price desc;")
             items = cursor.fetchall()
        elif(filter=='3'):
             cursor.execute(f"select * from {category} order by discount;")
             items = cursor.fetchall()
        elif(filter=='4'):
             cursor.execute(f"select * from {category} order by discount desc;")
             items = cursor.fetchall()
    return render_template('categorypage.html', items=items, userid=userid, cats=cats, category=category, filters=filters)

@app.route("/<string:userid>/<string:category>/processSearch", methods=['POST', 'GET'])
def processSearch(userid, category):
    searchword = request.form['searchbar']
    searchword = searchword.lower()
    print("searching for",searchword)
    if(searchword != None):
        cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%';")
        items = cursor.fetchall()
        return render_template('search.html', items=items, userid=userid, category=category)
    else:
        return categorypage(userid, category)

# @app.route("/<string:userid>/<string:category>/processSearch", methods=['POST', 'GET'])
# def processSearch(userid, category):
#     searchword = request.form['searchbar']
#     searchword = searchword.lower()
#     if(request.method=='POST'):
#         print("nikiiii")
#         filter = request.form['filters']
#         if(filter=='1'):
#             if(searchword != None):
#                  cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%' order by current_price;")
#                  items = cursor.fetchall()
#             else:
#                  cursor.execute(f"select * from {category} order by current_price;")
#                  items = cursor.fetchall()
#             render_template('search.html', items=items, userid=userid, category=category)
#         elif(filter=='2'):
#             if(searchword != None):
#                 cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%' order by current_price desc;")
#                 items = cursor.fetchall()
#             else:
#                 cursor.execute(f"select * from {category} order by current_price desc;")
#                 items = cursor.fetchall()
#             render_template('search.html', items=items, userid=userid, category=category)
#         elif(filter=='3'):
#             if(searchword != None):
#                 cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%' order by discount;")
#                 items = cursor.fetchall()
#             else:
#                 cursor.execute(f"select * from {category} order by discount;")
#                 items = cursor.fetchall()
#             render_template('search.html', items=items, userid=userid, category=category)
#         elif(filter=='4'):
#             if(searchword != None):
#                 cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%' order by discount desc;")
#                 items = cursor.fetchall()
#             else:
#                 cursor.execute(f"select * from {category} order by discount desc;")
#                 items = cursor.fetchall()
#             render_template('search.html', items=items, userid=userid, category=category)
#     if(searchword != None):
#         cursor.execute(f"select * from {category} where lower(name) like '%{searchword}%';")
#         items = cursor.fetchall()
#         return render_template('search.html', items=items, userid=userid, category=category)
#     else:
#         return categorypage(userid, category)

# @app.route("/<string:userid>/<string:category>/<string:itemid>/itempage", methods=['POST', 'GET'])
# def itempage(category, userid, itemid):
#     cursor.execute(f"select * from {category} where id = '{itemid}';")
#     item = cursor.fetchone()
#     quantity = min(5,item[22])
#     is_new = item[8]
#     if(is_new):
#         return render_template('itempage_newarrival.html', item=item, quantity=quantity, userid=userid)
#     else:
#         return render_template('itempage.html', item=item, quantity=quantity, userid=userid)

@app.route("/<string:userid>/<string:category>/<string:itemid>/itempage", methods=['POST', 'GET'])
def itempage(category, userid, itemid):
    cursor.execute(f"select * from {category} where id = '{itemid}';")
    item = cursor.fetchone()
    quantity = min(5,item[22])
    is_new = item[8]
    if((is_new == True) and (quantity <= 3)):
        return render_template('itempage_NewQuant.html', item=item, quantity=quantity, userid=userid)
    elif(is_new ==True):
        return render_template('itempage_New.html', item=item, quantity=quantity, userid=userid)
    elif(quantity <= 3):
        return render_template('itempage_Quant.html', item=item, quantity=quantity, userid=userid)
    else:
        return render_template('itempage.html', item=item, quantity=quantity, userid=userid)

#     if(quantity <= 3):
#         return render_template('itempage_quantitycons.html', item=item, quantity=quantity, numberofitems=quantity, userid=userid)
#     else:
#         return render_template('itempage.html', item=item, quantity=quantity, userid=userid)

@app.route("/<string:userid>/<string:category>/<string:itemid>/addtocart", methods=['POST', 'GET'])
def addtocart(userid, itemid, category):
    #if(request.method=='POST'):
    quant = request.form['quantity']
    cursor.execute(f"insert into cart values ('{userid}', '{category}', '{itemid}', {quant});")
    connection.commit()
    cursor.execute(f"update {category} set quantity=quantity-{quant} where id='{itemid}';") 
    connection.commit()
    return render_template('itemadded.html', userid=userid)
    
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/processLogin', methods=['POST', 'GET'])
def processLogin():
    if(request.method == 'POST'):
        username = request.form['Username']
        password = request.form['Password']
        cursor.execute(f"select * from users where userid = '{username}' and password='{password}';")
        #cursor.execute("select * from users where userid = %s and password = %s;", username, password)
        numrows = cursor.rowcount
        if(numrows == 0):
            return render_template('invalidlogin.html')
        else:
            return home(username)
            #return render_template('homepage.html', userid=username, cats= cats)

# @app.route('/processSignup', methods=['POST', 'GET'])
# def processSignup():
#     if(request.method == 'POST'):
#         username = request.form['Username']
#         password = request.form['Password']
#         cursor.execute(f"select * from users where userid = '{username}';")
#         numrows = cursor.rowcount
#         if(numrows == 0):
#             cursor.execute(f"insert into users (userid, password) values ('{username}', '{password}');")
#             connection.commit() 
#             return render_template('home.html', userid=username)
#         else:
#             return render_template('invalidsignup.html')

@app.route('/processSignup', methods=['POST', 'GET'])
def processSignup():
    if(request.method == 'POST'):
        userid = request.form['Username']
        password = request.form['Password']
        username = request.form['FullName']
        emailid = request.form['EmailId']
        mobile = request.form['MobileNo']
        x = random.randint(1000, 5000)
        walletbalance = x - (x % 100)

        cursor.execute(f"select * from users where userid = '{username}';")
        numrows = cursor.rowcount

        if(emailcheck(emailid)):
            return render_template('invalidsignupinvcred.html')

        if(numrows == 0):
            cursor.execute(f"insert into users (userid, password, username, emailid, mobile, wallet) values ('{userid}', '{password}', '{username}', '{emailid}', '{mobile}', {walletbalance});")
            connection.commit()
            return render_template('home.html', userid=userid)
        else:
            return render_template('invalidsignupuserexists.html')


@app.route("/<item>")
def product(item):
    return f"{item} is available to buy"

@app.route("/<string:userid>/addnewaddress")
def addnewaddress(userid):
    return render_template('addnewaddress.html', userid=userid)

@app.route("/<string:userid>/addmoney")
def addmoney(userid):
    return render_template('addmoney.html', userid=userid)

@app.route('/<string:userid>/updatebalance', methods=['POST', 'GET'])
def updatebalance(userid):
#    userid = 'skshruti'
    if(request.method == 'POST'):
        amt = request.form['Amount']
        cursor.execute(f"update users set wallet=wallet+{amt} where userid = '{userid}';")
        connection.commit() 
        return render_template('updatebalance.html', userid=userid)


@app.route('/<string:userid>/saveaddress', methods=['POST', 'GET'])
def saveaddress(userid):
#    userid = 'skshruti'
    if(request.method == 'POST'):
        name = request.form['Name']
        address = request.form['Address']
        cursor.execute(f"insert into addresses values('{userid}','{name}','{address}');")
        connection.commit() 
        return render_template('savedaddress.html', userid=userid)


# @app.route("/cart/<string:userid>")
# def cart(userid):
@app.route("/<string:userid>/cart")
def cart(userid):
#    userid = "skshruti"
    cursor.execute(f"with acc as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category from cart as t, accessories where accessories.id=t.itemid and userid='{userid}'), \
                bag as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, bags where bags.id=t.itemid and userid='{userid}'), \
                beaut as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, beauty where beauty.id=t.itemid and userid='{userid}'), \
                hous as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, house where house.id=t.itemid and userid='{userid}'), \
                jewel as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, jewelry where jewelry.id=t.itemid and userid='{userid}'), \
                kid as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, kids where kids.id=t.itemid and userid='{userid}'), \
                me as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, men where men.id=t.itemid and userid='{userid}'), \
                shoe as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, shoes where shoes.id=t.itemid and userid='{userid}'), \
                wome as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, women where women.id=t.itemid and userid='{userid}'), \
                alltables as (select * from acc union (select * from bag) union (select * from beaut) union (select * from hous) union (select * from jewel) union (select * from kid) union (select * from me) union (select * from shoe) union (select * from wome)) \
                select image_url,name,raw_price, discount, quantity, subtotal, sum(subtotal) over (partition by userid) as total, itemid, subcategory, category from alltables;")
    items = cursor.fetchall()
    cursor.execute(f"with acc as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category from cart as t, accessories where accessories.id=t.itemid and userid='{userid}'), \
                bag as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, bags where bags.id=t.itemid and userid='{userid}'), \
                beaut as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, beauty where beauty.id=t.itemid and userid='{userid}'), \
                hous as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, house where house.id=t.itemid and userid='{userid}'), \
                jewel as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, jewelry where jewelry.id=t.itemid and userid='{userid}'), \
                kid as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, kids where kids.id=t.itemid and userid='{userid}'), \
                me as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, men where men.id=t.itemid and userid='{userid}'), \
                shoe as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, shoes where shoes.id=t.itemid and userid='{userid}'), \
                wome as (select image_url,name,raw_price, discount, t.quantity, current_price* t.quantity as subtotal,itemid, subcategory, userid, t.category as total from cart as t, women where women.id=t.itemid and userid='{userid}'), \
                alltables as (select * from acc union (select * from bag) union (select * from beaut) union (select * from hous) union (select * from jewel) union (select * from kid) union (select * from me) union (select * from shoe) union (select * from wome)) \
                select distinct itemid from alltables;")
    itemids = cursor.fetchall()
    if(len(itemids)==0): return render_template('empty.html', userid=userid)
    return render_template('cart.html', items=items, itemids = itemids, userid=userid)


# @app.route("/addresses/<string:userid>")
# def addresses(userid):
@app.route("/<string:userid>/addresses")
def addresses(userid):
#    userid = "skshruti"
    cursor.execute(f"SELECT * \
            FROM addresses \
            where userid = '{userid}';" )
    addresses = cursor.fetchall()
    print(addresses)
    return render_template('addresses.html', addresses=addresses, userid=userid)

# @app.route("/addresses/<string:userid>/<int:paid>")
# def addresses(userid):
@app.route("/<string:userid>/checkout/<float:paid>/<string:itemid>")
def checkout(paid, itemid, userid):
#    userid = "skshruti"
    cursor.execute(f"UPDATE users \
            SET wallet=wallet-{paid} \
            where userid = '{userid}';" )
    connection.commit()
    cursor.execute(f"SELECT wallet \
            FROM users \
            where userid = '{userid}';" )
    
    val = cursor.fetchone()[0]
    cursor.execute(f"DELETE \
            FROM cart \
            where userid = '{userid}' and itemid = '{itemid}';" )
    connection.commit()
    cursor.execute(f"INSERT \
            INTO orders \
            values('{userid}', '{itemid}');" )
    connection.commit() 
    return render_template('checkout.html', balance=val, paid=paid, userid=userid)

# @app.route("/addresses/<string:userid>/<int:paid>")
# def addresses(userid):
@app.route("/<string:userid>/checkoutall/<float:paid>/<itemids>")
def checkoutall(paid, itemids, userid):
#    userid = "skshruti"
    cursor.execute(f"UPDATE users \
            SET wallet=wallet-{paid} \
            where userid = '{userid}';" )
    connection.commit()
    cursor.execute(f"SELECT wallet \
            FROM users \
            where userid = '{userid}';" )
    
    val = cursor.fetchone()[0]
    itemids = re.split(r'[(\',%)]',itemids)
    for itemid in itemids:
        print(itemid, len(itemid))
        if(len(itemid)>2):
            print(itemid)
            cursor.execute(f"DELETE \
                    FROM cart \
                    where userid = '{userid}' and itemid = '{itemid}';" )
            connection.commit()
            cursor.execute(f"INSERT \
            INTO orders \
            values('{userid}', '{itemid}');" )
            connection.commit() 
    return render_template('checkout.html', balance=val, paid=paid, userid=userid)

# @app.route("/orders/<string:userid>")
# def orders(userid):
@app.route("/<string:userid>/orders")
def orders(userid):
#    userid = "skshruti"
    cursor.execute(f"with acc as (select image_url,name,itemid, subcategory, userid, category from orders, accessories where accessories.id=orders.itemid and userid='{userid}'), \
        bag as (select image_url,name,itemid, subcategory, userid, category from orders, bags where bags.id=orders.itemid and userid='{userid}'), \
        beaut as (select image_url,name,itemid, subcategory, userid, category from orders, beauty where beauty.id=orders.itemid and userid='{userid}'), \
        hous as (select image_url,name,itemid, subcategory, userid, category from orders, house where house.id=orders.itemid and userid='{userid}'), \
        jewel as (select image_url,name,itemid, subcategory, userid, category from orders, jewelry where jewelry.id=orders.itemid and userid='{userid}'), \
        kid as (select image_url,name,itemid, subcategory, userid, category from orders, kids where kids.id=orders.itemid and userid='{userid}'), \
        me as (select image_url,name,itemid, subcategory, userid, category from orders, men where men.id=orders.itemid and userid='{userid}'), \
        shoe as (select image_url,name,itemid, subcategory, userid, category from orders, shoes where shoes.id=orders.itemid and userid='{userid}'), \
        wome as (select image_url,name,itemid, subcategory, userid, category from orders, women where women.id=orders.itemid and userid='{userid}'), \
        alltables as (select * from acc union (select * from bag) union (select * from beaut) union (select * from hous) union (select * from jewel) union (select * from kid) union (select * from me) union (select * from shoe) union (select * from wome)) \
        select image_url,name, itemid, subcategory, category from alltables;")
    items = cursor.fetchall()
    if(len(items)==0): return render_template('empty.html', userid=userid)
    return render_template('orders.html', items=items, userid=userid)

# @app.route("/info/<string:userid>")
# def info(userid):
@app.route("/<string:userid>/info")
def info(userid):
#    userid = "skshruti"
    cursor.execute(f"SELECT * \
            FROM users \
            where userid = '{userid}';" )
    information = cursor.fetchone()
    print(information)
    return render_template('info.html', information=information, userid=userid)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5022, debug=True)