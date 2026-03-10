# Modelo Relacional - Proyecto_Finanzas_80

Este documento detalla la estructura de la base de datos utilizada en el sistema.

## Tablas

### 1. Usuarios (`users`)
Almacena la información de los usuarios registrados.
- `email` (PK, TEXT): Correo electrónico único.
- `password` (TEXT): Contraseña (encriptada en producción).
- `name` (TEXT): Nombre completo del usuario.
- `is_new` (INTEGER): Flag para usuarios nuevos (1 o 0).

### 2. Movimientos (`movements`)
Registra todos los ingresos y egresos.
- `id` (PK, INTEGER): Identificador único.
- `user_email` (FK, TEXT): Referencia al usuario.
- `type` (TEXT): Tipo ('income' o 'expense').
- `concept` (TEXT): Descripción del movimiento.
- `amount` (REAL): Valor monetario.
- `date` (TEXT): Fecha del registro.
- `category` (TEXT): Categoría asociada.

### 3. Inversiones (`investments`)
Gestión de activos como Cryptos o Acciones.
- `id` (PK, INTEGER): Identificador único.
- `user_email` (FK, TEXT): Referencia al usuario.
- `symbol` (TEXT): Símbolo del activo (BTC, AAPL).
- `name` (TEXT): Nombre descriptivo.
- `investment` (REAL): Monto invertido inicial.
- `current` (REAL): Valor actual de mercado.
- `pnl` (REAL): Ganancia o pérdida.
- `type` (TEXT): Tipo de inversión ('crypto', 'stock').

### 4. Deudas (`debts`)
Seguimiento de saldos pendientes.
- `id` (PK, INTEGER): Identificador único.
- `user_email` (FK, TEXT): Referencia al usuario.
- `name` (TEXT): Nombre de la deuda.
- `total_amount` (REAL): Monto total.
- `paid_amount` (REAL): Monto pagado.
- `due_date` (TEXT): Fecha límite.

### 5. Pagos (`payments`)
Calendario de pagos recurrentes o servicios.
- `id` (PK, INTEGER): Identificador único.
- `user_email` (FK, TEXT): Referencia al usuario.
- `name` (TEXT): Nombre del servicio/pago.
- `amount` (REAL): Monto a pagar.
- `due_date` (TEXT): Fecha de vencimiento.

## Relaciones
- Todas las tablas secundarias se relacionan con `users` mediante el campo `user_email`.
