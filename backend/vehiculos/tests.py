from django.test import TestCase
from ninja.testing import TestClient

from catalogos.models import (
    Color,
    ColorPlaca,
    EstatusVehiculo,
    Marca,
    Modelo,
    TipoUso,
    TipoVehiculo,
)
from config.api import api
from organizacion.models import CentroDeServicio, Estado, Gerencia
from usuarios.models import Usuario

from ninja_jwt.tokens import RefreshToken

from .models import Vehiculo

client = TestClient(api)


def _paginated_items(response):
    return response.json()["items"]


def _paginated_count(response):
    return response.json()["count"]


class TestVehiculoCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado")
        cls.estado2 = Estado.objects.create(nombre="Otro Estado")
        cls.gerencia = Gerencia.objects.create(nombre="Test Gerencia")
        cls.centro = CentroDeServicio.objects.create(nombre="Test Centro", estado=cls.estado)
        cls.marca = Marca.objects.create(nombre="Test Marca")
        cls.modelo = Modelo.objects.create(nombre="Test Modelo", marca=cls.marca)
        cls.categoria = TipoVehiculo.objects.create(nombre="Test Categoria")
        cls.color = Color.objects.create(nombre="Test Color")
        cls.color_placa = ColorPlaca.objects.create(nombre="Test Color Placa")
        cls.estatus_v = EstatusVehiculo.objects.create(nombre="Test Estatus")
        cls.tipo_uso = TipoUso.objects.create(nombre="Test TipoUso")

        cls.admin = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.admin)
        cls.token = str(refresh.access_token)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def _valid_payload(self, **kwargs):
        base = {
            "numero_economico": "VEH-001",
            "numero_unidad": "UN-001",
            "gerencia_id": self.gerencia.id,
            "categoria_id": self.categoria.id,
            "marca_id": self.marca.id,
            "modelo_id": self.modelo.id,
            "anio": 2024,
            "vin": "1HGCM82633A123456",
            "estado_id": self.estado.id,
            "emplazamiento_id": self.centro.id,
            "estatus_id": self.estatus_v.id,
            "placa": "ABC-123",
            "color_placa_id": self.color_placa.id,
            "color_id": self.color.id,
            "tipo_uso_id": self.tipo_uso.id,
            "placa_intt": "INTT-001",
            "serial_motor": "MOTOR-001",
        }
        base.update(kwargs)
        return base

    def test_list_vehiculos_paginated(self):
        Vehiculo.objects.create(**self._valid_payload())
        response = client.get("/vehiculos/?limit=10&offset=0", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertIn("count", data)
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["numero_economico"], "VEH-001")

    def test_list_vehiculos_only_active(self):
        Vehiculo.objects.create(**self._valid_payload())
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="VEH-002",
                numero_unidad="UN-002",
                vin="2HGCM82633A123456",
                placa="XYZ-999",
                estatus_activo=False,
            )
        )
        response = client.get("/vehiculos/?limit=50&offset=0", headers=self.headers)
        items = _paginated_items(response)
        nums = [v["numero_economico"] for v in items]
        self.assertIn("VEH-001", nums)
        self.assertNotIn("VEH-002", nums)

    def test_list_vehiculos_incluir_inactivos(self):
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="VEH-002",
                numero_unidad="UN-002",
                vin="2HGCM82633A123456",
                placa="XYZ-999",
                estatus_activo=False,
            )
        )
        response = client.get(
            "/vehiculos/?incluir_inactivos=true&limit=50&offset=0", headers=self.headers
        )
        items = _paginated_items(response)
        nums = [v["numero_economico"] for v in items]
        self.assertIn("VEH-002", nums)

    def test_list_vehiculos_search(self):
        Vehiculo.objects.create(**self._valid_payload())
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="TOYOTA-001",
                numero_unidad="UN-002",
                vin="2HGCM82633A123457",
                placa="XYZ-998",
            )
        )
        response = client.get("/vehiculos/?search=toyota&limit=50&offset=0", headers=self.headers)
        items = _paginated_items(response)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["numero_economico"], "TOYOTA-001")

    def test_list_vehiculos_search_placa(self):
        Vehiculo.objects.create(**self._valid_payload())
        response = client.get("/vehiculos/?search=ABC-123&limit=50&offset=0", headers=self.headers)
        items = _paginated_items(response)
        self.assertEqual(len(items), 1)

    def test_list_vehiculos_sort_asc(self):
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="B-002",
                numero_unidad="UN-002",
                vin="2HGCM82633A123456",
                placa="PLA-002",
            )
        )
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="A-001",
                numero_unidad="UN-003",
                vin="3HGCM82633A123457",
                placa="PLA-001",
                color_placa_id=None,
            )
        )
        response = client.get(
            "/vehiculos/?sort_by=numero_economico&sort_order=asc&limit=50&offset=0",
            headers=self.headers,
        )
        items = _paginated_items(response)
        self.assertEqual(items[0]["numero_economico"], "A-001")
        self.assertEqual(items[1]["numero_economico"], "B-002")

    def test_list_vehiculos_sort_desc(self):
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="A-001",
                numero_unidad="UN-004",
                vin="2HGCM82633A123456",
                placa="PLA-003",
            )
        )
        Vehiculo.objects.create(
            **self._valid_payload(
                numero_economico="B-002",
                numero_unidad="UN-005",
                vin="3HGCM82633A123457",
                placa="PLA-004",
                color_placa_id=None,
            )
        )
        response = client.get(
            "/vehiculos/?sort_by=numero_economico&sort_order=desc&limit=50&offset=0",
            headers=self.headers,
        )
        items = _paginated_items(response)
        self.assertEqual(items[0]["numero_economico"], "B-002")
        self.assertEqual(items[1]["numero_economico"], "A-001")

    def test_list_vehiculos_empty(self):
        response = client.get("/vehiculos/?limit=50&offset=0", headers=self.headers)
        data = response.json()
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["items"], [])

    def test_get_vehiculo(self):
        v = Vehiculo.objects.create(**self._valid_payload())
        response = client.get(f"/vehiculos/{v.id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["numero_economico"], "VEH-001")

    def test_get_vehiculo_not_found(self):
        response = client.get("/vehiculos/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_create_vehiculo(self):
        payload = self._valid_payload()
        response = client.post("/vehiculos/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["numero_economico"], "VEH-001")
        self.assertEqual(data["vin"], "1HGCM82633A123456")
        self.assertIn("codigo_qr", data)
        self.assertTrue(data["codigo_qr"].startswith("data:image/png;base64,"))
        self.assertEqual(data["gerencia_nombre"], "Test Gerencia")
        self.assertEqual(data["categoria_nombre"], "Test Categoria")
        self.assertEqual(data["marca_nombre"], "Test Marca")
        self.assertEqual(data["modelo_nombre"], "Test Modelo")
        self.assertEqual(data["estado_nombre"], "Test Estado")
        self.assertEqual(data["emplazamiento_nombre"], "Test Centro")
        self.assertEqual(data["estatus_nombre"], "Test Estatus")
        self.assertEqual(data["color_nombre"], "Test Color")
        self.assertEqual(data["color_placa_nombre"], "Test Color Placa")
        self.assertEqual(data["tipo_uso"], self.tipo_uso.id)
        self.assertEqual(data["tipo_uso_nombre"], "Test TipoUso")
        self.assertEqual(data["numero_unidad"], "UN-001")
        self.assertEqual(data["placa_intt"], "INTT-001")
        self.assertEqual(data["serial_motor"], "MOTOR-001")

    def test_create_vehiculo_duplicate_numero_economico(self):
        Vehiculo.objects.create(**self._valid_payload())
        payload = self._valid_payload(numero_unidad="UN-002", vin="2HGCM82633A123456")
        response = client.post("/vehiculos/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 409)

    def test_create_vehiculo_duplicate_numero_unidad(self):
        Vehiculo.objects.create(**self._valid_payload())
        payload = self._valid_payload(numero_economico="VEH-002", vin="2HGCM82633A123456")
        response = client.post("/vehiculos/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 409)

    def test_create_vehiculo_duplicate_vin(self):
        Vehiculo.objects.create(**self._valid_payload())
        payload = self._valid_payload(numero_economico="VEH-002", numero_unidad="UN-002")
        response = client.post("/vehiculos/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 409)

    def test_create_vehiculo_duplicate_placa_mismo_color(self):
        Vehiculo.objects.create(**self._valid_payload())
        payload = self._valid_payload(
            numero_economico="VEH-002",
            numero_unidad="UN-002",
            vin="2HGCM82633A123456",
        )
        response = client.post("/vehiculos/", headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 409)

    def test_update_vehiculo(self):
        v = Vehiculo.objects.create(**self._valid_payload())
        response = client.put(
            f"/vehiculos/{v.id}",
            headers=self.headers,
            json={"placa": "XYZ-999"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["placa"], "XYZ-999")

    def test_deactivate_vehiculo(self):
        v = Vehiculo.objects.create(**self._valid_payload())
        response = client.delete(f"/vehiculos/{v.id}", headers=self.headers)
        self.assertEqual(response.status_code, 204)
        v.refresh_from_db()
        self.assertFalse(v.estatus_activo)

    def test_non_nacional_cannot_create(self):
        mecanico = Usuario.objects.create_user(
            username="mecanico_test",
            email="mecanico_test@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "mecanico_test", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/vehiculos/",
            headers=headers,
            json=self._valid_payload(),
        )
        self.assertEqual(response.status_code, 403)

    def test_mecanico_can_list(self):
        mecanico = Usuario.objects.create_user(
            username="mecanico2",
            email="mecanico2@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "mecanico2", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/vehiculos/?limit=10&offset=0", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        response = client.get("/vehiculos/?limit=10&offset=0")
        self.assertEqual(response.status_code, 401)
