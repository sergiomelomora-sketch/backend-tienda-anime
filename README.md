# Backend Tienda Anime (Django)

Proyecto backend desarrollado en Django para la gestión de una tienda de productos relacionados con anime (merchandising), como figuras, posters, poleras,  pedidos realizados por distintas plataformas.



---

##  Tecnologías utilizadas

* Python 3
* Django 5
* SQLite3
* Django Admin
* Git & GitHub

---

##  Funcionalidades principales

* Gestión de **categorías** de productos
* Gestión de **productos** de la tienda
* Gestión de **insumos** asociados a productos
* Gestión de **pedidos**
* Estados de pedido y de pago mediante `choices`
* Registro de pedidos desde distintas **plataformas** (Instagram, WhatsApp, presencial, etc.)
* Panel de administración personalizado con Django Admin

---

##  Seguimiento de pedidos (Token)

Cada pedido genera automáticamente un **token único (UUID)** que permite al cliente acceder al estado de su pedido mediante una URL de seguimiento.

Ejemplo de URL:

```
/seguimiento/<token_uuid>/
```

Esto permite:

* Consultar el estado del pedido
* Consultar el estado del pago
* Acceso sin autenticación

---

##  Funcionalidad extra

Para mejorar la usabilidad del panel de control (Admin), implementamos una función extra:

Se modificó la vista de listado de Pedidos en el Django Admin para reemplazar el texto simple del campo Estado por etiquetas de color .

Esto permite al administrador identificar visualmente el estado de un pedido (ej: 🔴 Cancelado, 🟢 Finalizado, 🟠 En proceso) sin tener que leer el campo completo, optimizando la gestión  de trabajo.

##  Estructura del proyecto

```
backend-tienda-anime/
│
├── appTienda/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
├── tienda_articulos/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

##  Instalación y ejecución

1. Clonar el repositorio:

```bash
https://github.com/sergiomelomora-sketch/backend-tienda-anime/tree/main
```

2. Entrar al proyecto:

```bash
cd tienda_articulos
```

3. Ejecutar migraciones:

```bash
python manage.py migrate
```

4. Crear superusuario:

```bash
python manage.py createsuperuser
```

5. Ejecutar el servidor:

```bash
python manage.py runserver
```

6. Acceder al panel de administración:

```
http://127.0.0.1:8000/admin/
```

---

## Decisiones de diseño

* Se utilizaron **UUID** para el seguimiento de pedidos por seguridad.
* Se emplearon **choices** en los modelos para estandarizar estados.
* Se personalizó Django Admin para mejorar la usabilidad.
* La temática del proyecto fue adaptada a **tienda de anime** manteniendo los requerimientos de la pauta.

---

##  Declaración de uso de Inteligencia Artificial

> Para el desarrollo de este proyecto se utilizó Inteligencia Artificial (ChatGPT) como herramienta de apoyo, principalmente para:

* Comprensión del framework Django y su estructura.
* Apoyo en la definición de modelos, vistas y rutas.
* Resolución de errores puntuales durante el desarrollo.
* Explicación de conceptos técnicos como uso de `choices`.

> La herramienta fue utilizada como apoyo al aprendizaje. Todas las decisiones de diseño, comprensión del código y la implementación final fueron realizadas y validadas por el equipo.

---

## 👨‍💻 Autores

**Sergio Melo y Alejandra Paez**
Proyecto académico – Backend Django
