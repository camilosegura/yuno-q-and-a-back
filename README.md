# Fast API Template

Template de servicio web construido usando [Fast API](https://fastapi.tiangolo.com/)

## Variables de entorno

Las variables de entorno que usa el proyecto estan contenidas en el archivo [.env.example](.env.example)

## Flujo de los datos

Los datos siguen el siguiente flujo :

routes -> controller -> use_cases

[routes](src/posts/routes/__init__.py) : Describe los endpoints de la aplicacion

[controller](src/posts/controllers/__init__.py) : Sirven como intermediario entre los rutas y los casos de uso

[use cases](src/posts/functions/example/use_cases.py) : Se encuentran separados en carpetas, con base en los recursos (modelos) propuestos para el API, y son los encargados de dar solucion al caso de uso propuesto; Ejemplo: guardar elementos en la base de datos, interactuar con API externas

## Usando PDM como gestor de paquetes

Puedes encontrar informacion de PDM en el siguiente link [PDM DOCS](https://pdm.fming.dev/latest/usage/dependency/)

- Para agregar paquetes

  - `pdm add <PACKAGE>`

- Para agregar paquetes como una dependencia de desarrollo

  - `pdm add -dG dev <PACKAGE>`

- Para instalar los paquetes presentes en el proyecto

  - `pdm install`

- Para generar el archivo `requirements.txt`, a partir de las dependencias del proyecto
  - `pdm run export`
