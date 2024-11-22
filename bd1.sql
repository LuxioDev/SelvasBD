-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-11-2024 a las 04:01:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `ID_CATEGORIA` int(11) NOT NULL,
  `DESCRIPCION` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`ID_CATEGORIA`, `DESCRIPCION`) VALUES
(1, 'Carnes de Res'),
(2, 'Carnes de Cerdo'),
(3, 'Pollos'),
(4, 'Otros');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cupones`
--

CREATE TABLE `cupones` (
  `ID_CUPON` int(11) NOT NULL,
  `codigo` varchar(5) NOT NULL,
  `descuento` decimal(5,2) NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cupones`
--

INSERT INTO `cupones` (`ID_CUPON`, `codigo`, `descuento`, `activo`) VALUES
(1, '', 0.00, 1),
(2, 'selva', 19.99, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_movimientos`
--

CREATE TABLE `historial_movimientos` (
  `ID_MOVIMIENTO` int(11) NOT NULL,
  `ID_PRODUCTO` int(11) DEFAULT NULL,
  `ID_SUCURSAL` int(11) DEFAULT NULL,
  `ID_USUARIO` int(11) DEFAULT NULL,
  `TIPO_MOVIMIENTO` enum('entrada','salida') DEFAULT NULL,
  `CANTIDAD` int(11) DEFAULT NULL,
  `FECHA` timestamp NOT NULL DEFAULT current_timestamp(),
  `DESCRIPCION` varchar(255) DEFAULT NULL,
  `ID_CUPON` int(11) NOT NULL,
  `MPAGO` enum('Efectivo','Tarjeta') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `ID_PERMISO` int(11) NOT NULL,
  `DESCRIPCION` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`ID_PERMISO`, `DESCRIPCION`) VALUES
(1, 'usuario'),
(2, 'gestor'),
(3, 'gestor global');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `ID_PRODUCTO` int(11) NOT NULL,
  `DESCRIPCION` varchar(100) NOT NULL,
  `PRECIO` int(11) NOT NULL,
  `ID_CATEGORIA` int(11) NOT NULL,
  `ID_PROVEEDOR` int(11) NOT NULL,
  `ID_SUCURSAL` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`ID_PRODUCTO`, `DESCRIPCION`, `PRECIO`, `ID_CATEGORIA`, `ID_PROVEEDOR`, `ID_SUCURSAL`) VALUES
(1, 'Bife de Chorizo 1kg', 6500, 1, 1, 2),
(2, 'Asado de Tira 1kg', 7500, 1, 1, 2),
(3, 'Lomo 1kg', 7250, 1, 1, 2),
(4, 'Roast Beef 1kg', 8200, 1, 1, 2),
(5, 'Tapa de Asado 1kg', 9000, 1, 1, 2),
(6, 'Nalga 1kg', 8750, 1, 1, 2),
(7, 'Vacío 1kg', 6750, 1, 1, 2),
(8, 'Colita de Cuadril 1kg', 8500, 1, 1, 2),
(9, 'Bondiola 1kg', 6800, 2, 1, 2),
(10, 'Costillas 1kg', 7000, 2, 1, 2),
(11, 'Jamón 1kg', 7250, 2, 1, 2),
(12, 'Panceta Ahumada 1kg', 2500, 2, 1, 2),
(13, 'Carré de cerdo 1kg', 5800, 2, 1, 2),
(14, 'Paleta de Cerdo 1kg', 12500, 2, 1, 2),
(15, 'Lomo de Cerdo 1kg', 9500, 2, 1, 2),
(16, 'Pechuga de Pollo 1kg', 15000, 3, 1, 2),
(17, 'Muslo de Pollo 1kg', 12500, 3, 1, 2),
(18, 'Alitas de Pollo 1kg', 7500, 3, 2, 2),
(19, 'Suprema de Pollo 1kg', 8500, 3, 2, 2),
(20, 'Pollo Entero 1kg', 8500, 3, 2, 2),
(21, 'Pata y Muslo de Pollo 1kg', 11500, 3, 1, 2),
(22, 'Chorizo de Cerdo  1kg', 15000, 4, 1, 2),
(23, 'Morcilla 1kg', 15500, 4, 2, 2),
(24, 'Chinchulines 1kg', 12500, 4, 2, 2),
(25, 'Mollejas 1kg', 7500, 4, 1, 2),
(26, 'T-Bone 1kg', 11000, 1, 1, 3),
(27, 'Entrecot 1kg', 12500, 1, 1, 3),
(28, 'Bife Angosto 1kg', 13500, 1, 1, 3),
(29, 'Bife de lomo 1kg', 15000, 1, 1, 3),
(30, 'Cuadril 1kg', 10500, 1, 1, 3),
(31, 'Asado de costilla 1kg', 9500, 1, 1, 3),
(32, 'Pechito de cerdo 1kg', 8000, 2, 1, 3),
(33, 'Morcilla 1kg', 3000, 2, 1, 3),
(34, 'Bondiola de cerdo 1kg', 9500, 2, 1, 3),
(35, 'Costillas de cerdo 1kg', 7500, 2, 1, 3),
(36, 'Pechuga de pollo 1kg', 12000, 3, 1, 3),
(37, 'Muslo de pollo 1kg', 11500, 3, 1, 3),
(38, 'Alitas de pollo 1kg', 7000, 3, 1, 3),
(39, 'Pollo entero 1kg', 9500, 3, 1, 3),
(40, 'Chorizo parrillero 1kg', 6000, 4, 1, 3),
(41, 'Morcilla parrillera 1kg', 5000, 4, 1, 3),
(42, 'Mollejas 1kg', 7500, 4, 1, 3),
(43, 'Riñon 1kg', 6000, 4, 1, 3),
(44, 'Chinchulines 1kg', 5500, 4, 1, 3),
(45, 'Matambre 1kg', 10500, 1, 1, 3),
(46, 'Bife de costilla 1kg', 12500, 1, 1, 3),
(47, 'Filet de merluza 1kg', 10000, 1, 1, 3),
(48, 'Cordero 1kg', 18000, 1, 1, 3),
(49, 'Chorizo de cerdo 1kg', 7000, 2, 1, 3),
(50, 'Lomo de cerdo 1kg', 9500, 2, 1, 3),
(51, 'Pechuga de pollo sin hueso 1kg', 12000, 3, 1, 3),
(52, 'Jamón cocido 1kg', 8000, 2, 1, 3),
(53, 'Patas de pollo 1kg', 6000, 3, 1, 3),
(54, 'T-Bone 1kg', 11000, 1, 1, 2),
(55, 'Entrecot 1kg', 12500, 1, 1, 2),
(56, 'Bife Angosto 1kg', 13500, 1, 1, 2),
(57, 'Bife de lomo 1kg', 15000, 1, 1, 2),
(58, 'Cuadril 1kg', 10500, 1, 1, 2),
(59, 'Asado de costilla 1kg', 9500, 1, 1, 2),
(60, 'Pechito de cerdo 1kg', 8000, 2, 1, 2),
(61, 'Morcilla 1kg', 3000, 2, 1, 2),
(62, 'Bondiola de cerdo 1kg', 9500, 2, 1, 2),
(63, 'Costillas de cerdo 1kg', 7500, 2, 1, 2),
(64, 'Pechuga de pollo 1kg', 12000, 3, 1, 2),
(65, 'Muslo de pollo 1kg', 11500, 3, 1, 2),
(66, 'Alitas de pollo 1kg', 7000, 3, 1, 2),
(67, 'Pollo entero 1kg', 9500, 3, 1, 2),
(68, 'Chorizo parrillero 1kg', 6000, 4, 1, 2),
(69, 'Morcilla parrillera 1kg', 5000, 4, 1, 2),
(70, 'Mollejas 1kg', 7500, 4, 1, 2),
(71, 'Riñon 1kg', 6000, 4, 1, 2),
(72, 'Chinchulines 1kg', 5500, 4, 1, 2),
(73, 'Matambre 1kg', 10500, 1, 1, 2),
(74, 'Bife de costilla 1kg', 12500, 1, 1, 2),
(75, 'Filet de merluza 1kg', 10000, 1, 1, 2),
(76, 'Cordero 1kg', 18000, 1, 1, 2),
(77, 'Chorizo de cerdo 1kg', 7000, 2, 1, 2),
(78, 'Lomo de cerdo 1kg', 9500, 2, 1, 2),
(79, 'Pechuga de pollo sin hueso 1kg', 12000, 3, 1, 2),
(80, 'Jamón cocido 1kg', 8000, 2, 1, 2),
(81, 'Patas de pollo 1kg', 6000, 3, 1, 2),
(82, 'T-Bone 1kg', 11000, 1, 1, 1),
(83, 'Entrecot 1kg', 12500, 1, 1, 1),
(84, 'Bife Angosto 1kg', 13500, 1, 1, 1),
(85, 'Bife de lomo 1kg', 15000, 1, 1, 1),
(86, 'Cuadril 1kg', 10500, 1, 1, 1),
(87, 'Asado de costilla 1kg', 9500, 1, 1, 1),
(88, 'Pechito de cerdo 1kg', 8000, 2, 1, 1),
(89, 'Morcilla 1kg', 3000, 2, 1, 1),
(90, 'Bondiola de cerdo 1kg', 9500, 2, 1, 1),
(91, 'Costillas de cerdo 1kg', 7500, 2, 1, 1),
(92, 'Pechuga de pollo 1kg', 12000, 3, 1, 1),
(93, 'Muslo de pollo 1kg', 11500, 3, 1, 1),
(94, 'Alitas de pollo 1kg', 7000, 3, 1, 1),
(95, 'Pollo entero 1kg', 9500, 3, 1, 1),
(96, 'Chorizo parrillero 1kg', 6000, 4, 1, 1),
(97, 'Morcilla parrillera 1kg', 5000, 4, 1, 1),
(98, 'Mollejas 1kg', 7500, 4, 1, 1),
(99, 'Riñon 1kg', 6000, 4, 1, 1),
(100, 'Chinchulines 1kg', 5500, 4, 1, 1),
(101, 'Matambre 1kg', 10500, 1, 1, 1),
(102, 'Bife de costilla 1kg', 12500, 1, 1, 1),
(103, 'Filet de merluza 1kg', 10000, 1, 1, 1),
(104, 'Cordero 1kg', 18000, 1, 1, 1),
(105, 'Chorizo de cerdo 1kg', 7000, 2, 1, 1),
(106, 'Lomo de cerdo 1kg', 9500, 2, 1, 1),
(107, 'Pechuga de pollo sin hueso 1kg', 12000, 3, 1, 1),
(108, 'Jamón cocido 1kg', 8000, 2, 1, 1),
(109, 'Patas de pollo 1kg', 6000, 3, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `ID_PROVEEDOR` int(11) NOT NULL,
  `NOMBRE` varchar(50) NOT NULL,
  `TELEFONO` int(10) NOT NULL,
  `CORREO` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`ID_PROVEEDOR`, `NOMBRE`, `TELEFONO`, `CORREO`) VALUES
(1, 'Pepito Ramirez', 1154545454, 'pepito.ramirez@gmail.com'),
(2, 'Julian Jose', 1157584467, 'Julian.jose@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stock`
--

CREATE TABLE `stock` (
  `ID_STOCK` int(11) NOT NULL,
  `ID_SUCURSAL` int(11) NOT NULL,
  `ID_PRODUCTO` int(11) NOT NULL,
  `CANTIDAD` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `stock`
--

INSERT INTO `stock` (`ID_STOCK`, `ID_SUCURSAL`, `ID_PRODUCTO`, `CANTIDAD`) VALUES
(1, 1, 1, 274),
(2, 2, 2, 1230421),
(3, 2, 3, 123123176),
(4, 1, 4, 32131321),
(5, 2, 5, 0),
(6, 2, 6, 0),
(7, 2, 7, 0),
(8, 2, 8, 0),
(9, 2, 9, 0),
(10, 2, 10, 0),
(11, 2, 11, 0),
(12, 2, 12, 0),
(13, 2, 13, 0),
(14, 2, 14, 0),
(15, 2, 15, 0),
(16, 2, 16, 0),
(17, 2, 17, 0),
(18, 2, 18, 0),
(19, 2, 19, 0),
(20, 2, 20, 0),
(21, 2, 21, 0),
(22, 2, 22, 0),
(23, 2, 23, 0),
(24, 2, 24, 0),
(25, 2, 25, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursales`
--

CREATE TABLE `sucursales` (
  `ID_SUCURSAL` int(11) NOT NULL,
  `DIRECCION` varchar(100) NOT NULL,
  `LOCALIDAD` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `sucursales`
--

INSERT INTO `sucursales` (`ID_SUCURSAL`, `DIRECCION`, `LOCALIDAD`) VALUES
(1, 'Calle 123, Muñiz', 'San Miguel'),
(2, 'calle 321, Bella Vista', 'San Miguel'),
(3, 'calle falsa 443, Frino', 'Jose C. Paz');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID_USUARIO` int(11) NOT NULL,
  `NOMBRE` varchar(20) NOT NULL,
  `APELLIDO` varchar(20) NOT NULL,
  `USUARIO` varchar(12) NOT NULL,
  `CONTRASEÑA` varchar(50) NOT NULL,
  `ID_SUCURSAL` int(11) NOT NULL,
  `ID_PERMISO` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`ID_USUARIO`, `NOMBRE`, `APELLIDO`, `USUARIO`, `CONTRASEÑA`, `ID_SUCURSAL`, `ID_PERMISO`) VALUES
(1, 'Lucas', 'Fernandez', 'luxio', 'admin', 1, 1),
(2, 'Josesito', 'Ramirez', 'jose', '123', 2, 2),
(3, 'Matias', 'Bracale', 'quantum', 'global', 2, 1),
(4, 'admin', 'admin', 'admin', 'admin', 2, 3),
(5, 'Gabriel', 'Dolores', 'ripgabi', 'rawr', 3, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`ID_CATEGORIA`);

--
-- Indices de la tabla `cupones`
--
ALTER TABLE `cupones`
  ADD PRIMARY KEY (`ID_CUPON`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `historial_movimientos`
--
ALTER TABLE `historial_movimientos`
  ADD PRIMARY KEY (`ID_MOVIMIENTO`),
  ADD KEY `ID_PRODUCTO` (`ID_PRODUCTO`),
  ADD KEY `ID_SUCURSAL` (`ID_SUCURSAL`),
  ADD KEY `ID_USUARIO` (`ID_USUARIO`),
  ADD KEY `historia_movimientos_ibfk_4` (`ID_CUPON`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`ID_PERMISO`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`ID_PRODUCTO`),
  ADD KEY `FK_PRODUCTOS_CATEGORIAS` (`ID_CATEGORIA`),
  ADD KEY `FK_PRODUCTOS_PROVEEDOR` (`ID_PROVEEDOR`),
  ADD KEY `FK_PRODUCTOS_SUCURSAL` (`ID_SUCURSAL`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`ID_PROVEEDOR`);

--
-- Indices de la tabla `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`ID_STOCK`),
  ADD KEY `FK_STOCK_SUCURSALES` (`ID_SUCURSAL`),
  ADD KEY `FK_STOCK_PRODUCTOS` (`ID_PRODUCTO`) USING BTREE;

--
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`ID_SUCURSAL`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID_USUARIO`),
  ADD KEY `FK_USUARIOS_SUCURSAL` (`ID_SUCURSAL`),
  ADD KEY `FK_USUARIOS_PERMISOS` (`ID_PERMISO`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `ID_CATEGORIA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `cupones`
--
ALTER TABLE `cupones`
  MODIFY `ID_CUPON` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `historial_movimientos`
--
ALTER TABLE `historial_movimientos`
  MODIFY `ID_MOVIMIENTO` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `ID_PERMISO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `ID_PRODUCTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `ID_PROVEEDOR` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `stock`
--
ALTER TABLE `stock`
  MODIFY `ID_STOCK` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  MODIFY `ID_SUCURSAL` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID_USUARIO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `historial_movimientos`
--
ALTER TABLE `historial_movimientos`
  ADD CONSTRAINT `historia_movimientos_ibfk_4` FOREIGN KEY (`ID_CUPON`) REFERENCES `cupones` (`ID_CUPON`),
  ADD CONSTRAINT `historial_movimientos_ibfk_1` FOREIGN KEY (`ID_PRODUCTO`) REFERENCES `productos` (`ID_PRODUCTO`),
  ADD CONSTRAINT `historial_movimientos_ibfk_2` FOREIGN KEY (`ID_SUCURSAL`) REFERENCES `sucursales` (`ID_SUCURSAL`),
  ADD CONSTRAINT `historial_movimientos_ibfk_3` FOREIGN KEY (`ID_USUARIO`) REFERENCES `usuarios` (`ID_USUARIO`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `FK_PRODUCTOS_SUCURSAL` FOREIGN KEY (`ID_SUCURSAL`) REFERENCES `sucursales` (`ID_SUCURSAL`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
