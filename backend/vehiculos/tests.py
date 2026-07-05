from django.test import TestCase
from ninja.testing import TestClient

from catalogos.models import Color, ColorPlaca, EstatusVehiculo, Marca, Modelo, TipoVehiculo
from config.api import api
from organizacion.models import CentroDeServicio, Estado, Gerencia
from usuarios.models import Usuario

from ninja_jwt.tokens import RefreshToken

from .models import Vehiculo

client = TestClient(api)


class TestVehiculoCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado")
        cls.gerencia = Gerencia.objects.create(nombre="Test Gerencia")
        cls.centro = CentroDeServicio.objects.create(nombre="Test Centro")
        cls.marca = Marca.objects.create(nombre="Test Marca")
        cls.modelo = Modelo.objects.create(nombre="Test Modelo", marca=cls.marca)
        cls.categoria = TipoVehiculo.objects.create(nombre="Test Categoria")
        cls.color = Color.objects.create(nombre="Test Color")
        cls.color_placa = ColorPlaca.objects.create(nombre="Test Color Placa")
        cls.estatus_v = EstatusVehiculo.objects.create(nombre="Test Estatus")

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
            "placa_intt": "INTT-001",
            "serial_motor": "MOTOR-001",
        }
        base.update(kwargs)
        return base

    def test_list_vehiculos(self):
        Vehiculo.objects.create(**self._valid_payload())
        response = client.get("/vehiculos/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        nums = [v["numero_economico"] for v in response.json()]
        self.assertIn("VEH-001", nums)

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
        response = client.get("/vehiculos/", headers=self.headers)
        nums = [v["numero_economico"] for v in response.json()]
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
        response = client.get("/vehiculos/?incluir_inactivos=true", headers=self.headers)
        nums = [v["numero_economico"] for v in response.json()]
        self.assertIn("VEH-002", nums)

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

        response = client.get("/vehiculos/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        response = client.get("/vehiculos/")
        self.assertEqual(response.status_code, 401)
