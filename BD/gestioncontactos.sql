-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-09-2020 a las 18:17:40
-- Versión del servidor: 10.1.30-MariaDB
-- Versión de PHP: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestioncontactos`
--
CREATE DATABASE IF NOT EXISTS `gestioncontactos` DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;
USE `gestioncontactos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos`
--

CREATE TABLE `contactos` (
  `idContacto` int(11) NOT NULL,
  `conIdentificacion` varchar(15) COLLATE utf8_spanish_ci NOT NULL,
  `conNombres` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `conApellidos` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `conCorreo` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `conFechaNacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `contactos`
--

INSERT INTO `contactos` (`idContacto`, `conIdentificacion`, `conNombres`, `conApellidos`, `conCorreo`, `conFechaNacimiento`) VALUES
(1, '2020', 'Faustino', 'Asprilla', 'fasprilla@yahoo.com', '1968-09-13'),
(2, '2232', 'wqe', 'wew', 'mgalindo@misena.edu.co', '2020-08-30');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contactos`
--
ALTER TABLE `contactos`
  ADD PRIMARY KEY (`idContacto`),
  ADD UNIQUE KEY `uq_identificacion` (`conIdentificacion`),
  ADD UNIQUE KEY `uq_correo` (`conCorreo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contactos`
--
ALTER TABLE `contactos`
  MODIFY `idContacto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
