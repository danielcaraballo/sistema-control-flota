from django.test import TestCase
from ninja.testing import TestClient

from config.api import api
from organizacion.models import Estado, Gerencia

from .models import Usuario

client = TestClient(api)


class TestUsuariosAPI(TestCase):
    def setUp(self):
        self.gerencia = Gerencia.objects.create(nombre="Test Gerencia")
        self.estado = Estado.objects.create(nombre="Test Estado", estatus_activo=True)
        self.admin = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.GERENTE_NACIONAL,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(login_resp.status_code, 200, "Login falló en setUp")
        self.token = login_resp.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_list_usuarios(self):
        response = client.get("/usuarios/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_usuario(self):
        response = client.post(
            "/usuarios/",
            headers=self.headers,
            json={
                "username": "newuser",
                "email": "new@test.com",
                "password": "pass123",
                "first_name": "New",
                "last_name": "User",
                "rol": "analista_nacional",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "new@test.com")

    def test_create_usuario_with_estado(self):
        response = client.post(
            "/usuarios/",
            headers=self.headers,
            json={
                "email": "estatal@test.com",
                "password": "pass123",
                "first_name": "Maria",
                "last_name": "Garcia",
                "rol": "responsable_estatal",
                "estado_id": self.estado.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["estado"], self.estado.id)
        self.assertEqual(data["estado_nombre"], "Test Estado")

    def test_create_usuario_estatal_without_estado(self):
        response = client.post(
            "/usuarios/",
            headers=self.headers,
            json={
                "email": "estatal@test.com",
                "password": "pass123",
                "first_name": "No",
                "last_name": "Estado",
                "rol": "responsable_estatal",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_create_usuario_invalid_estado(self):
        response = client.post(
            "/usuarios/",
            headers=self.headers,
            json={
                "email": "invalid@test.com",
                "password": "pass123",
                "first_name": "Invalid",
                "last_name": "Estado",
                "rol": "analista_nacional",
                "estado_id": 99999,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_create_usuario_duplicate_email(self):
        Usuario.objects.create_user(
            username="existing",
            email="dup@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        response = client.post(
            "/usuarios/",
            headers=self.headers,
            json={
                "username": "newuser",
                "email": "dup@test.com",
                "password": "pass123",
                "first_name": "New",
                "last_name": "User",
                "rol": "analista_nacional",
            },
        )
        self.assertEqual(response.status_code, 409)

    def test_update_usuario(self):
        user = Usuario.objects.create_user(
            username="updatable",
            email="update@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        response = client.put(
            f"/usuarios/{user.id}",
            headers=self.headers,
            json={"first_name": "Updated", "last_name": "User"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "Updated")
        self.assertEqual(data["last_name"], "User")

    def test_update_usuario_duplicate_email(self):
        user1 = Usuario.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        user2 = Usuario.objects.create_user(
            username="user2",
            email="user2@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        response = client.put(
            f"/usuarios/{user1.id}",
            headers=self.headers,
            json={"email": "user2@test.com"},
        )
        self.assertEqual(response.status_code, 409)

    def test_deactivate_usuario(self):
        user = Usuario.objects.create_user(
            username="delete_me",
            email="delete@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        response = client.delete(
            f"/usuarios/{user.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_non_gerente_cannot_list_usuarios(self):
        user = Usuario.objects.create_user(
            username="analista",
            email="analista@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "analista", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/usuarios/", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_access(self):
        response = client.get("/usuarios/")
        self.assertEqual(response.status_code, 401)
