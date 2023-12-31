from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os, sys

# @app.route('/')
# def hello():
#   return 'Hello World!'
# from markupsafe import escape

# @app.route('/user/<name>')
# def user_page(name):
#     return f'User: {escape(name)}'

# name = 'Grey Li'
# movies = [
#   {'title': 'My Neighbor Totoro', 'year': '1988'},
#   {'title': 'Dead Poets Society', 'year': '1989'},
#   {'title': 'A Perfect World', 'year': '1993'},
#   {'title': 'Leon', 'year': '1994'},
#   {'title': 'Mahjong', 'year': '1996'},
#   {'title': 'Swallowtail Butterfly', 'year': '1996'},
#   {'title': 'King of Comedy', 'year': '1999'},
#   {'title': 'Devils on the Doorstep', 'year': '1999'},
#   {'title': 'WALL-E', 'year': '2008'},
#   {'title': 'The Pork of Music', 'year': '2012'},
# ]
# @app.route('/')
# def index():
#   return render_template('index.html', name=name, movies=movies)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
# 创建自定义命令 forge,把所有虚拟数据添加到数据库里flask forge
import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.route('/')
def index():
    # user = User.query.get(2)
    # db.session.delete(user)
    # db.session.commit()
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)

