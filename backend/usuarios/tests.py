from django.test import TestCase
from ninja.testing import TestClient

from config.api import api
from organizacion.models import Estado, Gerencia

from .models import Usuario

client = TestClient(api)


class TestAuth(TestCase):
    def setUp(self):
        self.gerencia = Gerencia.objects.create(nombre="Test Gerencia")
        self.estado = Estado.objects.create(nombre="Test Estado")
        self.user = Usuario.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            rol=Usuario.Rol.GERENTE_NACIONAL,
            gerencia=self.gerencia,
            estado=self.estado,
        )

    def test_login_success(self):
        response = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["username"], "testuser")

    def test_login_with_email(self):
        response = client.post(
            "/auth/login",
            json={"username": "test@example.com", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        response = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, 401)

    def test_me_endpoint(self):
        login_resp = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "testpass123"},
        )
        token = login_resp.json()["access"]

        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_me_unauthorized(self):
        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 401)

    def test_refresh_token(self):
        login_resp = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "testpass123"},
        )
        refresh_token = login_resp.json()["refresh"]

        response = client.post(
            "/auth/refresh",
            json={"refresh": refresh_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_refresh_invalid(self):
        response = client.post(
            "/auth/refresh",
            json={"refresh": "invalidtoken"},
        )
        self.assertEqual(response.status_code, 401)


class TestUsuariosAPI(TestCase):
    def setUp(self):
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
        self.token = login_resp.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_list_usuarios(self):
        response = client.get("/usuarios/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_usuario(self):
        Estado.objects.create(nombre="Test Estado", estatus_activo=True)
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

    def test_unauthorized_access(self):
        response = client.get("/usuarios/")
        self.assertEqual(response.status_code, 401)
