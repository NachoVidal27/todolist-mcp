TodoList API con FastAPI y MCP

Este proyecto es una API REST para gestionar tareas (TodoList), desarrollada con FastAPI e integrada con el protocolo MCP (Model Context Protocol). Permite ejecutar herramientas desde un LLM como Claude utilizando un servidor MCP local.

Requisitos:

- Python 3.9 o superior
- Node.js (recomendado v18+)
- pip
- (opcional) virtualenv

Pasos para ejecutar localmente:

1.  Clonar el repositorio:
    git clone https://github.com/tu-usuario/todolist-mcp.git
    cd todolist-mcp

2.  Crear y activar entorno virtual (opcional pero recomendado):
    python -m venv venv
    source venv/bin/activate # En Windows: venv\Scripts\activate

3.  Instalar dependencias:
    pip install -r requirements.txt

4.  Instalar mcp-remote (si no lo tienes):
    npm install -g mcp-remote

5.  Iniciar el servidor FastAPI:
    uvicorn main:app --reload
    El servidor estará disponible en: http://localhost:8000

6.  Iniciar el servidor MCP (en otra terminal):
    npx mcp-remote http://localhost:8000/mcp --allow-http --transport sse-only
    Esto iniciará el servidor MCP en: http://localhost:8080

7.  Conectarse desde Claude Desktop:
    Abre la aplicación Claude Desktop y escribe en el chat:
    Connect to MCP server at http://localhost:8080
    Claude detectará automáticamente las herramientas disponibles en tu servidor MCP.
    // En caso de que Claude rechace la conexión
    En Claude Desktop:

        File > Settings > Developer > "Edit config" > claude_desktop_config.json
          Agregar el siguiente codigo presente en el archivo claude_desktop_config.json de la raiz del proyecto
        Reiniciar Claude
        File > Settings > Developer
          todolist debe aparecer como tool, en caso contrario contactar al correo igjovidal@gmail.com

Estructura típica del proyecto:

- main.py Archivo principal FastAPI
- models.py Modelos Pydantic y SQLAlchemy
- routes.py Rutas de la API REST
- requirements.txt
- README.md

Notas:

- Asegúrate de tener fastapi-mcp instalado en tu entorno Python.
- Puedes verificar las herramientas MCP accediendo a http://localhost:8000/mcp/status
- Usa Postman o curl para probar los endpoints REST de forma manual.

Autor: Ignacio Vidal
Contacto: igjovidal@gmail.com

PROYECTO DESARROLLADO PARA CRUNCHLOOP
