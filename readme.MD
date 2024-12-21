# Tasa de Cambio Automática - Módulo Odoo

## Descripción General

Este módulo proporciona la funcionalidad para actualizar automáticamente las tasas de cambio (TRM) desde una API de tasas de cambio personalizada. El módulo recupera las tasas de cambio desde una API pública disponible y las actualiza en el sistema Odoo para cada empresa.

El módulo permite configurar un cron job para actualizar periódicamente los datos de las tasas de cambio sin intervención manual. Esta característica es esencial para las empresas que manejan múltiples monedas, asegurando que las tasas de conversión de divisas siempre estén actualizadas.

## Características

- **Actualización de Tasas de Cambio**: Recupera las tasas de cambio desde la API externa (`https://www.datos.gov.co/resource/32sa-8pi3.json`).
- **Actualizaciones Automáticas**: Un cron job que se ejecuta diariamente para actualizar las tasas de cambio.
- **Proveedor de Cambio Personalizado**: Configurable por empresa con la opción de seleccionar el proveedor "Custom Exchange" para actualizar las tasas de cambio.
- **Conversión en Tiempo Real**: Actualiza automáticamente la tasa de USD a la moneda principal de la empresa basada en el valor recuperado.
- **Registro de Eventos**: Registro detallado de las actualizaciones, errores y resultados de la recuperación de datos.

## Instrucciones de Instalación

### Paso 1: Instalar el Módulo en Odoo.sh

1. **Clonar el Repositorio**:
   - Clona el repositorio que contiene este módulo en tu instancia de Odoo.sh. Puedes hacerlo a través de la interfaz de GitHub o directamente usando el comando `git clone`.

2. **Activar el Modo Desarrollador**:
   - Antes de instalar cualquier módulo, asegúrate de que el modo desarrollador esté activado en Odoo. Puedes activarlo desde la interfaz de Odoo yendo a **Configuración > Activar Modo Desarrollador**.

3. **Instalar el Módulo**:
   - Una vez que el módulo esté agregado a tu instancia de Odoo.sh, ve a **Aplicaciones** en el backend de Odoo.
   - Busca el módulo "Tasa de Cambio Automática".
   - Haz clic en **Instalar** para instalar el módulo.

### Paso 2: Configurar el Módulo

1. **Seleccionar el Proveedor de Cambio**:
   - Después de instalar el módulo, ve a la sección **Empresas** bajo **Configuración > Usuarios y Empresas > Empresas**.
   - Elige la empresa para la cual deseas habilitar la actualización automática de las tasas de cambio.
   - En el formulario de la empresa, encuentra el campo **Proveedor de Cambio** y selecciona **Custom Exchange**.

2. **Configurar el Cron Job**:
   - El cron job se configura automáticamente durante la instalación del módulo. Este cron job se ejecutará diariamente para actualizar las tasas de cambio.
   - Puedes ver y gestionar el cron job yendo a **Configuración > Técnico > Automatización > Acciones Programadas**.
   - Asegúrate de que el cron job llamado **Actualizar Tasas de Cambio** esté activo.

### Paso 3: Usar el Módulo

- Una vez que el módulo esté instalado y configurado, el sistema recuperará automáticamente las tasas de cambio a diario.
- La tasa recuperada se aplicará a la conversión de **USD a la moneda local**.
- Puedes verificar las tasas de cambio actualizadas yendo a **Contabilidad > Configuración > Monedas**.
- El módulo actualiza las tasas para el día actual y, si es necesario, ajusta la tasa de cambio para la empresa correspondiente.

### Paso 4: Registros y Manejo de Errores

- Todas las operaciones relacionadas con la actualización de las tasas de cambio se registran.
- Para ver los registros, puedes consultar los **registros de Odoo** o utilizar la **Odoo shell** para asegurarte de que el cron job funcione correctamente.
- Los errores relacionados con las solicitudes API o cualquier otro problema se registran con mensajes de error detallados.

## Detalles del Cron Job

- **Nombre**: Actualizar Tasas de Cambio
- **Frecuencia de Ejecución**: Diaria
- **Modelo**: `res.company`
- **Método**: `_update_currency_rates()`
- **Activo**: Sí
- **Intervalo**: 1 día
- **Número de Llamadas**: Ilimitado

## Solución de Problemas

- Si encuentras problemas con el módulo que no actualiza las tasas de cambio:
  1. Asegúrate de que el **proveedor de cambio** para la empresa esté configurado como **Custom Exchange**.
  2. Revisa los registros de Odoo para cualquier error relacionado con el cron job o la solicitud API.
  3. Verifica la conectividad de tu instancia de Odoo con la API externa.
  4. Asegúrate de que la **moneda USD** esté activa en tu sistema Odoo.

## Licencia

Este módulo está licenciado bajo la licencia **LGPL-3**. Puedes modificar, distribuir y usarlo bajo los términos de esta licencia.