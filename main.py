from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import randint

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def json_cafe(cafe):
    return jsonify(cafe={
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        # "id": cafe.id,
        "amenities": {
           "seats": cafe.seats,
           "has_toilet": cafe.has_toilet,
           "has_wifi": cafe.has_wifi,
           "has_sockets": cafe.has_sockets,
           "can_take_calls": cafe.can_take_calls,
           "coffee_price": cafe.coffee_price
            }
        }
    )


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random_cafe():
    cafe_length = len(db.session.execute(db.select(Cafe.id)).all())
    cafe = db.get_or_404(Cafe, randint(1, cafe_length))
    print(cafe)
    jsonified_cafe = json_cafe(cafe)
    print(jsonified_cafe)
    return jsonified_cafe


@app.route("/all", methods=["GET"])
def all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    #This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(cafes=[to_dict(cafe) for cafe in all_cafes])


# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
