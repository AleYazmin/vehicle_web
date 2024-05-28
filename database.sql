-- Crear tabla para los vehículos
CREATE TABLE vehicle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    transmision VARCHAR(50) NOT NULL,
    carroceria VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    vendedor VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha_venta DATE NOT NULL
);

-- Crear tabla para los usuarios
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);

-- Crear tabla para las ventas
CREATE TABLE sale (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT,
    user_id INT,
    sale_date DATE NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
