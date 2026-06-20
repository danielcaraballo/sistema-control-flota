from django.test import TestCase
from ninja.testing import TestClient

from config.api import api
from usuarios.models import Usuario

from .models import Estado, Gerencia

client = TestClient(api)


class TestOrganizacionAPI(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nombre="Lara", estatus_activo=True)
        self.gerencia = Gerencia.objects.create(nombre="Gerencia Test", estatus_activo=True)
        self.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.GERENTE_NACIONAL,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.token = login_resp.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_list_estados(self):
        response = client.get("/organizacion/estados/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nombre"], "Lara")

    def test_list_estados_only_active(self):
        Estado.objects.create(nombre="Inactivo", estatus_activo=False)
        response = client.get("/organizacion/estados/", headers=self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_list_gerencias(self):
        response = client.get("/organizacion/gerencias/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nombre"], "Gerencia Test")

    def test_unauthorized(self):
        response = client.get("/organizacion/estados/")
        self.assertEqual(response.status_code, 401)
