from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

# 获取当前脚本所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 使用 pymysql 作为 MySQL 驱动
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/barrage'
db = SQLAlchemy(app)

# 导入蓝图对象
from blueprints.danmu.views import danmu_bp
from blueprints.sentiment.views import senti_bp
from blueprints.theme.views import theme_bp
from blueprints.statistics.views import stat_bp
from blueprints.history.views import history_bp

# 注册蓝图
app.register_blueprint(danmu_bp)
app.register_blueprint(senti_bp)
app.register_blueprint(theme_bp)
app.register_blueprint(stat_bp)
app.register_blueprint(history_bp)

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
    app.run(debug=True)
