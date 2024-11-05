-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-10-2024 a las 19:34:00
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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
  `id` int(11) NOT NULL,
  `codigo` varchar(5) NOT NULL,
  `descuento` decimal(5,2) NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cupones`
--

INSERT INTO `cupones` (`id`, `codigo`, `descuento`, `activo`) VALUES
(1, 'omen', 10.00, 1),
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
  `DESCRIPCION` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `historial_movimientos`
--

INSERT INTO `historial_movimientos` (`ID_MOVIMIENTO`, `ID_PRODUCTO`, `ID_SUCURSAL`, `ID_USUARIO`, `TIPO_MOVIMIENTO`, `CANTIDAD`, `FECHA`, `DESCRIPCION`) VALUES
(1, 1, 2, 2, 'entrada', 0, '2024-10-09 15:55:07', 'Producto nuevo añadido con stock inicial de 0'),
(2, 2, 2, 2, 'entrada', 0, '2024-10-09 15:55:20', 'Producto nuevo añadido con stock inicial de 0'),
(3, 3, 2, 2, 'entrada', 0, '2024-10-09 15:55:29', 'Producto nuevo añadido con stock inicial de 0'),
(4, 4, 2, 2, 'entrada', 0, '2024-10-09 15:55:38', 'Producto nuevo añadido con stock inicial de 0'),
(5, 5, 2, 2, 'entrada', 0, '2024-10-09 15:55:49', 'Producto nuevo añadido con stock inicial de 0'),
(6, 6, 2, 2, 'entrada', 0, '2024-10-09 15:55:58', 'Producto nuevo añadido con stock inicial de 0'),
(7, 7, 2, 2, 'entrada', 0, '2024-10-09 15:56:11', 'Producto nuevo añadido con stock inicial de 0'),
(8, 8, 2, 2, 'entrada', 0, '2024-10-09 15:56:46', 'Producto nuevo añadido con stock inicial de 0'),
(9, 9, 2, 2, 'entrada', 0, '2024-10-09 15:57:01', 'Producto nuevo añadido con stock inicial de 0'),
(10, 10, 2, 2, 'entrada', 0, '2024-10-09 15:57:09', 'Producto nuevo añadido con stock inicial de 0'),
(11, 11, 2, 2, 'entrada', 0, '2024-10-09 15:57:18', 'Producto nuevo añadido con stock inicial de 0'),
(12, 12, 2, 2, 'entrada', 0, '2024-10-09 15:57:29', 'Producto nuevo añadido con stock inicial de 0'),
(13, 13, 2, 2, 'entrada', 0, '2024-10-09 15:57:42', 'Producto nuevo añadido con stock inicial de 0'),
(14, 14, 2, 2, 'entrada', 0, '2024-10-09 15:57:56', 'Producto nuevo añadido con stock inicial de 0'),
(15, 15, 2, 2, 'entrada', 0, '2024-10-09 15:58:09', 'Producto nuevo añadido con stock inicial de 0'),
(16, 16, 2, 2, 'entrada', 0, '2024-10-09 15:58:24', 'Producto nuevo añadido con stock inicial de 0'),
(17, 17, 2, 2, 'entrada', 0, '2024-10-09 15:58:40', 'Producto nuevo añadido con stock inicial de 0'),
(18, 18, 2, 2, 'entrada', 0, '2024-10-09 15:59:00', 'Producto nuevo añadido con stock inicial de 0'),
(19, 19, 2, 2, 'entrada', 0, '2024-10-09 15:59:10', 'Producto nuevo añadido con stock inicial de 0'),
(20, 20, 2, 2, 'entrada', 0, '2024-10-09 15:59:19', 'Producto nuevo añadido con stock inicial de 0'),
(21, 21, 2, 2, 'entrada', 0, '2024-10-09 15:59:37', 'Producto nuevo añadido con stock inicial de 0'),
(22, 22, 2, 2, 'entrada', 0, '2024-10-09 15:59:56', 'Producto nuevo añadido con stock inicial de 0'),
(23, 23, 2, 2, 'entrada', 0, '2024-10-09 16:00:16', 'Producto nuevo añadido con stock inicial de 0'),
(24, 24, 2, 2, 'entrada', 0, '2024-10-09 16:00:31', 'Producto nuevo añadido con stock inicial de 0'),
(25, 25, 2, 2, 'entrada', 0, '2024-10-09 16:00:39', 'Producto nuevo añadido con stock inicial de 0'),
(26, 1, 1, 1, 'salida', 2, '2024-10-22 16:32:28', 'Venta de producto'),
(27, 1, 1, 1, 'salida', 1, '2024-10-22 16:35:37', 'Venta de producto'),
(28, 1, 2, 2, 'salida', 2, '2024-10-22 16:53:49', 'Venta de producto'),
(29, 3, 2, 2, 'salida', 2, '2024-10-22 16:53:57', 'Venta de producto'),
(30, 3, 2, 2, 'salida', 2, '2024-10-22 16:53:58', 'Venta de producto'),
(31, 3, 2, 2, 'salida', 2, '2024-10-22 16:54:26', 'Venta de producto'),
(32, 3, 2, 2, 'salida', 2, '2024-10-22 16:54:33', 'Venta de producto'),
(33, 3, 2, 2, 'salida', 2, '2024-10-22 16:55:27', 'Venta de producto'),
(34, 3, 2, 2, 'salida', 3, '2024-10-22 16:55:53', 'Venta de producto'),
(35, 2, 2, 4, 'entrada', 2, '2024-10-22 16:56:55', 'Se añadió stock de 2 unidades'),
(36, 3, 2, 2, 'salida', 2, '2024-10-22 18:35:45', 'Venta de producto'),
(37, 3, 2, 2, 'salida', 3, '2024-10-22 18:35:50', 'Venta de producto'),
(38, 3, 2, 2, 'salida', 3, '2024-10-22 18:36:28', 'Venta de producto'),
(39, 1, 2, 2, 'salida', 2, '2024-10-22 18:37:37', 'Venta de producto'),
(40, 3, 2, 2, 'salida', 2, '2024-10-25 15:07:28', 'Venta de producto'),
(41, 3, 2, 2, 'salida', 2, '2024-10-25 15:08:26', 'Venta de producto'),
(42, 3, 2, 2, 'salida', 2, '2024-10-25 15:08:28', 'Venta de producto'),
(43, 3, 2, 2, 'salida', 2, '2024-10-25 15:08:28', 'Venta de producto'),
(44, 3, 2, 2, 'salida', 2, '2024-10-25 15:14:00', 'Venta de producto'),
(45, 3, 2, 2, 'salida', 2, '2024-10-25 15:15:58', 'Venta de producto'),
(46, 3, 2, 2, 'salida', 2, '2024-10-25 15:17:19', 'Venta de producto'),
(47, 3, 2, 2, 'salida', 2, '2024-10-25 15:17:27', 'Venta de producto'),
(48, 3, 2, 2, 'salida', 3, '2024-10-25 15:17:53', 'Venta de producto'),
(49, 3, 2, 2, 'salida', 3, '2024-10-25 15:18:01', 'Venta de producto'),
(50, 3, 2, 2, 'salida', 2, '2024-10-25 15:22:27', 'Venta de producto'),
(51, 3, 2, 2, 'salida', 3, '2024-10-25 15:22:32', 'Venta de producto'),
(52, 3, 2, 2, 'salida', 4, '2024-10-25 15:22:40', 'Venta de producto'),
(53, 3, 2, 2, 'salida', 5, '2024-10-25 15:22:47', 'Venta de producto'),
(54, 2, 2, 1, 'salida', 2, '2024-10-28 15:23:32', 'Se modificó el stock en 2 unidades'),
(55, 3, 2, 1, 'salida', 2, '2024-10-28 15:23:42', 'Se modificó el stock en 2 unidades'),
(56, 1, 2, 1, 'salida', 10, '2024-10-28 15:30:03', 'Se modificó el stock en 10 unidades'),
(57, 1, 2, 1, 'salida', 10, '2024-10-28 15:30:07', 'Se modificó el stock en 10 unidades'),
(58, 1, 2, 1, 'salida', 10, '2024-10-28 15:30:26', 'Se modificó el stock en 10 unidades'),
(59, 1, 2, 1, 'salida', 10, '2024-10-28 15:32:11', 'Se modificó el stock en 10 unidades'),
(60, 1, 2, 3, 'salida', 10, '2024-10-28 15:33:34', 'Se modificó el stock en 10 unidades'),
(61, 1, 2, 3, 'salida', 10, '2024-10-28 15:34:59', 'Se modificó el stock en 10 unidades'),
(62, 1, 2, 1, 'salida', 10, '2024-10-28 15:50:26', 'Se modificó el stock en 10 unidades'),
(63, 1, 2, 1, 'salida', 10, '2024-10-28 15:51:02', 'Se modificó el stock en 10 unidades'),
(64, 1, 2, 1, 'salida', 10, '2024-10-28 16:00:31', 'Se modificó el stock en 10 unidades'),
(65, 1, 2, 1, 'salida', 1, '2024-10-28 16:06:59', 'Se modificó el stock en 1 unidades'),
(66, 1, 2, 1, 'salida', 1, '2024-10-28 16:07:29', 'Se modificó el stock en 1 unidades');

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
(25, 'Mollejas 1kg', 7500, 4, 1, 2);

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
(1, 2, 1, 8),
(2, 2, 2, 0),
(3, 2, 3, 29),
(4, 2, 4, 0),
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
(4, 'admin', 'admin', 'admin', 'admin', 1, 3),
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
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `historial_movimientos`
--
ALTER TABLE `historial_movimientos`
  ADD PRIMARY KEY (`ID_MOVIMIENTO`),
  ADD KEY `ID_PRODUCTO` (`ID_PRODUCTO`),
  ADD KEY `ID_SUCURSAL` (`ID_SUCURSAL`),
  ADD KEY `ID_USUARIO` (`ID_USUARIO`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `historial_movimientos`
--
ALTER TABLE `historial_movimientos`
  MODIFY `ID_MOVIMIENTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `ID_PERMISO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `ID_PRODUCTO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

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
