from flask import Flask,request,jsonify
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
import linklist
import Hashtable as HT
import BTDict
import random
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQL_TRAK_MODIFICATIONS"] = 0
now = datetime.now()
# configure sqlite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

#routes
@app.route("/",methods=["GET"])
def Home():
    return "<h1>hello<h1>"

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200

@app.route("/user/descend",methods=["GET"])
def Get_all_usersDesending():
    with app.app_context():
        users = User.query.all()
    all_use_ll = linklist.LinkedList()
    for user in users:
        all_use_ll.addHead(
            {
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "address":user.address,
                "phone":user.phone,

            }
        )
    return jsonify(all_use_ll.to_list()) , 200

@app.route("/user/ascending_id",methods=["GET"])
def Get_all_usersAscending():
    with app.app_context():
        users = User.query.all()
    all_User_ll = linklist.LinkedList()
    for user in users:
        all_User_ll.addNode(
            {
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "address":user.address,
                "phone":user.phone,
            }
        )
    return jsonify(all_User_ll.to_list()), 200
@app.route("/user/<int:user_id>",methods=["GET"])
def getSingleUser(user_id):
    with app.app_context():
        user = User.query.filter_by(id=user_id).first()
    if type(user) == type(None):
        return f"user doesnt exist in DB may have already been deleted TS: {datetime.today()}"
    return f"User with ID {user_id}: Name: {user.name}, Email: {user.email}"

   
@app.route("/user/<user_id>",methods=["DELETE"])
def Delete_User(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"delete user":user_id}) , 200
@app.route("/blog_post/<user_id>",methods=["POST"])
def create_blog(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"user doesnt exist":f"User Id {user_id}"},{"User must exist before you can make post":""}),400
    """ if type(user) == type(None):
        return jsonify({f"user with id {user_id} doesnt exist":now})"""
    ht = HT.HashTable(10)
    ht.add_key_val("title",data["title"])
    ht.add_key_val("body",data["body"])
    ht.add_key_val("date",now)
    ht.add_key_val("user_id",user_id)
    
    newBlogPOst = BlogPost(
        title=ht.getvalue("title"),
        body=ht.getvalue("body"),
        date=ht.getvalue("date"),
        user_id= ht.getvalue("user_id")
        )
    db.session.add(newBlogPOst)
    db.session.commit()
    return jsonify({f"user {user_id} post create":f"created at {now}"}) , 200

@app.route("/blogs",methods=["GET"])
def get_all_blog_posts():
    with app.app_context():
        blogs = BlogPost.query.all()
    allpost = linklist.LinkedList()
    for post in blogs:
        allpost.addNode(
            {
                "id":post.id,
                "title":post.title,
                #"body":post.body,
                "date":post.date,
                "userid":post.user_id
            }

        )
    return jsonify(allpost.to_list()) ,200

@app.route("/blogs/<id>",methods=["GET"])
def get_one_blog_posts_Tree(id):
    bt =  BTDict.BinarySearchTree()
    with app.app_context():
        blogs = BlogPost.query.all()
    x = random.shuffle(blogs)
    for post in blogs:
        bt.insert({
            "id":post.id,
            "title":post.title,
            "body":post.body,
            "user_id":post.user_id,
        })
    post = bt.search(id)
    if not post:
        return jsonify({"response":"data not found "}) ,404
    
    return jsonify(post)


   
@app.route("/blog_post/<blog_post_id>",methods=["DELETE"])
def delete_blog_post(blog_post_id):
    with app.app_context():
        blogs = BlogPost.query.filter_by(id=blog_post_id).first()
    if type(blogs) != type(None):
        db.session.delete(blogs)
        db.session.commit()
        return jsonify({"delete post":blog_post_id}) , 200
    else:
        return jsonify({"Message":"user not found"}), 404


if __name__ == "__main__":
    print("run")
    with app.app_context():
        db.create_all()
    app.run(debug=True)