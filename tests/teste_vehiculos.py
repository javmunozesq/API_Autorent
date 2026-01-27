# tests/test_vehiculos.py
def test_list_vehiculos(monkeypatch, client):
    sample = [{"id":1,"matricula":"1234ABC","vin":"VIN1","modelo_id":1,"color":"Blanco","kilometraje":1000,"estado":"disponible","precio_dia":10.0,"ubicacion":"X"}]
    monkeypatch.setattr("app.controllers.vehiculos_api.fetch_all_vehiculos", lambda: sample)
    resp = client.get("/vehiculos")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert resp.json()[0]["matricula"] == "1234ABC"