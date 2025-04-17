import json
from main import app

def generate_openapi_schema():
    openapi_schema = app.openapi()
    with open("openapi.json", "w") as file:
        json.dump(openapi_schema, file, indent=2)
    print("OpenAPI schema generated successfully at openapi.json")

if __name__ == "__main__":
    generate_openapi_schema()