# Urban Routes - Automatización QA

## Descripción del proyecto

Este proyecto contiene pruebas automatizadas para validar el flujo completo de solicitud de un taxi en la aplicación Urban Routes.
Las pruebas verifican el comportamiento de la interfaz desde la configuración de la ruta hasta la asignación del conductor.

## Tecnologías utilizadas

- Python
- Selenium WebDriver
- Pytest
- Page Object Model (POM)

## Funcionalidades probadas

Las pruebas cubren el siguiente flujo:

1. Configurar dirección de origen y destino
2. Seleccionar tarifa Comfort
3. Registrar número de teléfono
4. Confirmar código SMS
5. Agregar tarjeta de crédito
6. Escribir mensaje al conductor
7. Solicitar manta y pañuelos
8. Agregar 2 helados
9. Solicitar taxi
10. Esperar asignación de conductor

## Cómo ejecutar las pruebas

1. Clonar el repositorio

```bash
git clone <repo-url>