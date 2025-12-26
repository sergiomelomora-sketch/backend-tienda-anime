# 🎌 Sistema de Gestión - Tienda de Anime

Este proyecto es una plataforma de gestión de pedidos e insumos desarrollada con *Django* y *Django REST Framework*. Incluye un sistema de reportes dinámicos con visualización de datos y un conjunto de APIs robustas con validaciones de seguridad.

*URL del Proyecto:* [ https://sergiobastiann.pythonanywhere.com/ ]

## 👥 Integrantes
* Alejandra Paez
* Sergio Melo
* Profesor: Sebastian Callejas
* Fecha: 26-12-2025

---

## 📊 1. Reporte del Sistema (Vista Protegida)

URL : https://sergiobastiann.pythonanywhere.com/reporte/

El sistema cuenta con un panel de administración visual que permite analizar el estado del negocio en tiempo real.

* Seguridad: La vista está protegida por el sistema de autenticación de Django. Si se intenta acceder sin estar logueado (ej. modo incógnito), el sistema redirigirá al login del administrador.
* Gráficos Dinámicos: Implementamos un gráfico intuitivo para identificar rápidamente el producto más solicitado.
* Filtros: Permite agrupar y filtrar pedidos por:
     Rango de fechas.
     Plataforma (WhatsApp, Instagram, etc.).
* Detalle de Datos: En la parte inferior se presenta una tabla detallada con los pedidos filtrados directamente desde la base de datos.

---

## 🚀 2. Documentación de APIs

### API 1: CRUD de Insumos
Gestión completa de los productos e insumos de la tienda.
* Listado y Creación: https://sergiobastiann.pythonanywhere.com/api/insumos/  - Permite visualizar la lista completa y agregar nuevos ítems que se reflejan en el Admin.
* Detalle, Edición y Borrado: https://sergiobastiann.pythonanywhere.com/api/insumos/3/ Permite modificar o eliminar insumos específicos con la id al final de la url.

### API 2: Gestión de Pedidos (Restringida)
Diseñada para la creación y edición de pedidos, protegiendo la privacidad de los datos.

* Creación: https://sergiobastiann.pythonanywhere.com/api/pedidos/ Los pedidos se crean vía JSON. (Nota: Por seguridad, el listado general GET y el borrado están deshabilitados en esta ruta).
* Modificación: https://sergiobastiann.pythonanywhere.com/api/pedidos/13/ Permite actualizar los datos de un pedido existente.

### API 3: Filtros por Parámetros (Query Params)
Endpoint especializado para consultas avanzadas:
* Rango de Fechas: https://sergiobastiann.pythonanywhere.com/api/pedidos/filtrar/?desde=2025-12-16&hasta=2025-12-22
* Límite de Resultados: https://sergiobastiann.pythonanywhere.com/api/pedidos/filtrar/?desde=2025-12-16&hasta=2025-12-22&max=2 (Limita la cantidad de objetos devueltos).
* Por Estado: https://sergiobastiann.pythonanywhere.com/api/pedidos/filtrar/?estado=solicitado (Filtra por estado del pedido).

---

## ✅ 3. Mejoras y Retroalimentación (Evolución de Evaluación 3)
En esta entrega hemos corregido y mejorado puntos críticos detectados anteriormente:

1.  Validación de Fechas: Implementamos lógica en los Serializers para impedir la creación de pedidos con fechas anteriores a la actual. Esto funciona tanto en el Admin como en las peticiones JSON.
2.  Visualización en Admin: Se optimizó la visualización de las imágenes de referencia en el panel de administración para una mejor gestión.
3.  Token de Seguimiento: Se agregó el campo de token de seguimiento a los pedidos, mejorando el control de cada solicitud.
4.  Validación de Entradas: Si se ingresa un estado inexistente o una fecha inválida en la API 3, el sistema responde con un error *400 Bad Request* detallando el fallo.

---


