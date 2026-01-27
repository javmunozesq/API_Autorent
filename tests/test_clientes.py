# tests/test_clientes.py
import pytest
from app import schemas

def test_list_clientes_empty(monkeypatch, client):
    # Simular fetch_all_clientes devolviendo lista vacía
    monkeypatch.setattr("app.controllers.clientes_api.fetch_all_clientes", lambda: [])
    resp = client.get("/clientes")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_and_get_cliente(monkeypatch, client):
    # Simular insert_cliente y fetch_cliente_by_id
    created = {"id": 42, "nombre": "Ana", "apellido": "Lopez", "email": "ana@example.com", "telefono": None, "direccion": None}
    def fake_insert(nombre, apellido, email, telefono, direccion):
        return 42
    def fake_fetch_by_id(cid):
        return created if cid == 42 else None

    monkeypatch.setattr("app.controllers.clientes_api.insert_cliente", fake_insert)
    monkeypatch.setattr("app.controllers.clientes_api.fetch_cliente_by_id", fake_fetch_by_id)

    payload = {"nombre": "Ana", "apellido": "Lopez", "email": "ana@example.com"}
    resp = client.post("/clientes", json=payload)
    assert resp.status_code == 201
    assert resp.json()["id"] == 42
    assert resp.json()["nombre"] == "Ana"

    # Obtener
    resp2 = client.get("/clientes/42")
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "ana@example.com"

def test_update_cliente_not_found(monkeypatch, client):
    # Simular update_cliente devolviendo False
    monkeypatch.setattr("app.controllers.clientes_api.update_cliente", lambda *args, **kwargs: False)
    payload = {"nombre": "X", "apellido": "Y", "email": "x@y.com"}
    resp = client.put("/clientes/999", json=payload)
    assert resp.status_code == 404

def test_delete_cliente(monkeypatch, client):
    monkeypatch.setattr("app.controllers.clientes_api.delete_cliente", lambda cid: True)
    resp = client.delete("/clientes/1")
    assert resp.status_code == 204