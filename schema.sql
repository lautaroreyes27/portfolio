-- Diseño físico (MySQL). Ejecutar en la base de Clever Cloud.
CREATE TABLE IF NOT EXISTS usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS perfil (
  id INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  titulo VARCHAR(150) NOT NULL,
  bio TEXT NOT NULL,
  email VARCHAR(120),
  github VARCHAR(150),
  linkedin VARCHAR(150)
);
CREATE TABLE IF NOT EXISTS estudio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  institucion VARCHAR(150) NOT NULL,
  titulo VARCHAR(150) NOT NULL,
  periodo VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS experiencia (
  id INT AUTO_INCREMENT PRIMARY KEY,
  empresa VARCHAR(150) NOT NULL,
  puesto VARCHAR(150) NOT NULL,
  periodo VARCHAR(50) NOT NULL,
  descripcion TEXT
);
CREATE TABLE IF NOT EXISTS habilidad (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  categoria VARCHAR(60) NOT NULL
);

INSERT INTO perfil VALUES (1, 'Lautaro Reyes', 'Estudiante técnico y desarrollador web',
 'Curso 6° año en el Instituto Técnico Renault, en Córdoba. Trabajo con bases de datos, redes, ciberseguridad y desarrollo web con Python. Quiero estudiar Ingeniería en Sistemas y Telecomunicaciones.', '', '', '');
INSERT INTO estudio (institucion, titulo, periodo) VALUES
 ('Instituto Técnico Renault', 'Secundario técnico', '4° año - actualidad'),
 ('Centro Educativo Santo Domingo', 'Jardín, primaria y hasta 3° año', 'Hasta 3° año');
INSERT INTO habilidad (nombre, categoria) VALUES
 ('Python', 'Programación'), ('Flask', 'Programación'), ('HTML y CSS', 'Programación'),
 ('SQL y MySQL', 'Bases de datos'), ('Modelado relacional', 'Bases de datos'),
 ('Redes', 'Infraestructura'), ('Certificados SSL/TLS', 'Infraestructura'), ('Ciberseguridad', 'Infraestructura'),
 ('Arquitectura de software', 'Otros'), ('Inglés', 'Otros');
