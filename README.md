# Actualización Automatizada de Tasas de Cambio en Google Sheets

## Descripción
Este proyecto automatiza la obtención de tasas de cambio (dólar y euro) desde el sitio web de Banamex y las actualiza en una hoja de cálculo de Google Sheets. Utiliza **Python** para el web scraping con **Selenium** y la integración con la **API de Google Sheets**. El proceso se ejecuta diariamente mediante **GitHub Actions**, lo que garantiza que los datos estén siempre actualizados sin intervención manual.

## Características principales
- **Web scraping**: Extrae las tasas de cambio del sitio web de Banamex.
- **Integración con Google Sheets**: Actualiza automáticamente una hoja de cálculo con los datos obtenidos.
- **Automatización**: Se ejecuta diariamente o manualmente mediante GitHub Actions.
- **Seguridad**: Usa secretos de GitHub para proteger las credenciales de la API y el ID de la hoja de cálculo.

## Tecnologías utilizadas
- **Python**: Para el scraping y la integración con Google Sheets.
- **Selenium**: Para interactuar con el navegador y extraer datos.
- **Google Sheets API**: Para actualizar la hoja de cálculo.
- **GitHub Actions**: Para la automatización y ejecución programada.

## Cómo funciona
1. El script de Python obtiene las tasas de cambio del sitio web de Banamex.
2. Los datos se envían a una hoja de cálculo de Google Sheets utilizando la API de Google Sheets.
3. El proceso se ejecuta automáticamente todos los días a las 18:00 UTC mediante GitHub Actions.

## Instalación y uso
1. Clona el repositorio.
2. Configura las credenciales de Google Sheets y el ID de la hoja de cálculo como secretos en GitHub.
3. Ejecuta el workflow manualmente o espera a que se ejecute automáticamente según la programación.

## Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el proyecto, abre un **issue** o envía un **pull request**.

## Licencia
Este proyecto está bajo la licencia [MIT](LICENSE).