from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:fime@localhost/VentasVehiculos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'admin'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    transmision = db.Column(db.String(20), nullable=False)
    carroceria = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    vendedor = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    search = request.args.get('search')
    if search:
        filtered_vehicles = Vehicle.query.filter(Vehicle.marca.ilike(f'%{search}%')).all()
    else:
        filtered_vehicles = Vehicle.query.all()
    return render_template('index.html', vehicles=filtered_vehicles, search=search)

@app.route('/add', methods=('GET', 'POST'))
@login_required
def add_vehicle():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        transmision = request.form['transmision']
        carroceria = request.form['carroceria']
        color = request.form['color']
        vendedor = request.form['vendedor']
        precio = request.form['precio']
        fecha_venta = request.form['fecha_venta']

        vehicle = Vehicle(
            marca=marca,
            modelo=modelo,
            transmision=transmision,
            carroceria=carroceria,
            color=color,
            vendedor=vendedor,
            precio=precio,
            fecha_venta=datetime.strptime(fecha_venta, '%Y-%m-%d')
        )
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_vehicle.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    if request.method == 'POST':
        vehicle.marca = request.form['marca']
        vehicle.modelo = request.form['modelo']
        vehicle.transmision = request.form['transmision']
        vehicle.carroceria = request.form['carroceria']
        vehicle.color = request.form['color']
        vehicle.vendedor = request.form['vendedor']
        vehicle.precio = request.form['precio']
        vehicle.fecha_venta = datetime.strptime(request.form['fecha_venta'], '%Y-%m-%d')

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_vehicle.html', vehicle=vehicle)

@app.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/details/<int:id>')
@login_required
def vehicle_details(id):
    vehicle = Vehicle.query.get_or_404(id)
    return render_template('vehicle_details.html', vehicle=vehicle)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')


###########################################################################################
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


