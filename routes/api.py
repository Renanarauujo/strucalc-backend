from flask import Blueprint, request, jsonify
from datetime import datetime
import json

from repositories.project_repository import add_project, get_all_projects, delete_project
from repositories.structural_element_repository import (add_element, get_elements_by_project, delete_element)
from services.slab_service import slab_precalc

## CRIAÇÃO DE UM BLUEPRINT(PACOTE DE ROTAS)
api_bp = Blueprint("api", __name__) 

## ROTA PARA CRIAÇÃO DE PROJETOS
@api_bp.route("/projects", methods=["POST"]) 
def create_project():
    try:
        data = request.get_json(force=True, silent=False) or {}
    except Exception:
        return {"error": "JSON inválido"}, 400

    name = (data.get("name") or "").strip()
    if not name:
        return {"error": "Campo 'name' é obrigatório."}, 400

    created_in = datetime.now().isoformat() + "Z"
    project_id = add_project(name, created_in)

    return {"id": project_id, "name": name, "created_in": created_in}, 201

## ROTA PARA CRIAÇÃO DE ELEMENTOS ESTRUTURAIS
@api_bp.route("/structural-elements", methods=["POST"])
def create_element():
    try:
        data = request.get_json(force=True, silent=False) or {}
    except Exception:
        return {"error": "JSON inválido"}, 400

    # Validações básicas
    try:
        project_id = int(data.get("project_id"))
    except Exception:
        return {"error": "Campo 'project_id' deve ser inteiro."}, 400

    structural_type = (data.get("structural_type") or "").strip()
    if not structural_type:
        return {"error": "Campo 'structural_type' é obrigatório."}, 400

    structural_data = data.get("structural_data")
    if not isinstance(structural_data, dict):
        return {"error": "Campo 'structural_data' deve ser um objeto JSON."}, 400

    created_in = datetime.utcnow().isoformat() + "Z"

    # Executa cálculo (stub) com os dados de entrada
    results_dict = slab_precalc(structural_data)

    # Serializa para salvar no SQLite (TEXT)
    structural_data_json = json.dumps(structural_data, ensure_ascii=False)
    results_json = json.dumps(results_dict, ensure_ascii=False)

    element_id = add_element(
        project_id=project_id,
        structural_type=structural_type,
        structural_data_json=structural_data_json,
        results_json=results_json,
        created_in=created_in
    )

    # Resposta: já devolvemos os objetos em JSON (dict)
    return {
        "id": element_id,
        "project_id": project_id,
        "structural_type": structural_type,
        "structural_data": structural_data,
        "results": results_dict,
        "created_in": created_in
    }, 201

## ROTA PARA LISTA OS ELEMENTOS
@api_bp.route("/structural-elements", methods=["GET"])
def list_elements():
    project_id = request.args.get("project_id")
    if project_id is None:
        return {"error": "Parâmetro 'project_id' é obrigatório."}, 400

    try:
        project_id_int = int(project_id)
    except Exception:
        return {"error": "Parâmetro 'project_id' deve ser inteiro."}, 400

    rows = get_elements_by_project(project_id_int)

    # Convertemos TEXT JSON → dict para a resposta
    def parse_json_safe(s):
        try:
            return json.loads(s) if s is not None else None
        except Exception:
            return None

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "project_id": r["project_id"],
            "structural_type": r["structural_type"],
            "structural_data": parse_json_safe(r["structural_data"]),
            "results": parse_json_safe(r["results"]),
            "created_in": r["created_in"],
        })

    return jsonify(items), 200

## ROTA PARA REMOVER ELEMENTOS
@api_bp.route("/structural-elements/<int:element_id>", methods=["DELETE"])
def remove_element(element_id: int):
    ok = delete_element(element_id)
    if not ok:
        return {"error": "Elemento não encontrado."}, 404
    # Sem conteúdo (HTTP 204) é o mais comum para DELETE
    return "", 204

## ROTA PARA LISTAR PROJETOS
@api_bp.route("/projects", methods=["GET"])
def list_projects():
    projects = get_all_projects()
    return jsonify(projects), 200

## ROTA PARA DELETAR PROJETOS
@api_bp.route("/projects/<int:project_id>", methods=["DELETE"])
def remove_project(project_id: int):
    ok = delete_project(project_id)
    if not ok:
        return {"error": "Projeto não encontrado."}, 404
    # Sem conteúdo (HTTP 204) é o mais comum para DELETE
    return "", 204

