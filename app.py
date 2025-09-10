from flask import Flask
from flask_cors import CORS
from routes.api import api_bp

## FUNÇÃO DE CRIAÇÃO DO APP
def create_app(): 
    app = Flask(__name__) # CRIA A INSTANCIA DO SERVIDOR
    CORS(app)
    app.register_blueprint(api_bp, url_prefix="/api") # CONECTA O PACOTE DE ROTAS (BLUEPRINT) AO APP CRIADO
    return app                                        # TUDO O QUE FOR REGISTRADO NO BP RECEBE O PREFIXO DE /API                  
                                                      # http://127.0.0.1:5000/api/FUNÇÃO              
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # FACILITAR PROCESSO DE DESENVOLVIMENTO: HOT RELOAD E STACKTRACE COM EXCEPTIONS

print("\nROTAS REGISTRADAS:")
for rule in app.url_map.iter_rules():
    print(rule, rule.methods)
print()