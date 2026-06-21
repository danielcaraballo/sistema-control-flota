from django.test import TestCase
from ninja.testing import TestClient

from config.api import api
from usuarios.models import Usuario

from .models import Estado, Gerencia

client = TestClient(api)


class TestOrganizacionAPI(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nombre="Lara", estatus_activo=True)
        self.gerencia = Gerencia.objects.create(
            nombre="Gerencia Test", estatus_activo=True)
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
        self.assertEqual(login_resp.status_code, 200, "Login falló en setUp")
        self.token = login_resp.json()["access"]
        self.refresh_token = login_resp.json()["refresh"]
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

    def test_list_gerencias_only_active(self):
        Gerencia.objects.create(nombre="Inactiva", estatus_activo=False)
        response = client.get("/organizacion/gerencias/", headers=self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_unauthorized(self):
        response = client.get("/organizacion/estados/")
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn("detail", data)


class TestAuthAPI(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.GERENTE_NACIONAL,
        )

    def test_login_success(self):
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["username"], "admin")

    def test_login_invalid_credentials(self):
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 401)

    def test_login_by_email(self):
        response = client.post(
            "/auth/login",
            json={"username": "admin@test.com", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_refresh_token(self):
        login_resp = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        refresh = login_resp.json()["refresh"]

        response = client.post(
            "/auth/refresh",
            json={"refresh": refresh},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_refresh_token_invalid(self):
        response = client.post(
            "/auth/refresh",
            json={"refresh": "invalid_token"},
        )
        self.assertEqual(response.status_code, 401)

    def test_me(self):
        login_resp = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "admin")
        self.assertEqual(data["email"], "admin@test.com")

    def test_me_unauthorized(self):
        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 401)


class TestUsuariosAPI(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nombre="Lara", estatus_activo=True)
        self.gerencia = Gerencia.objects.create(
            nombre="Gerencia Test", estatus_activo=True)
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
        self.assertEqual(login_resp.status_code, 200, "Login falló en setUp")
        self.token = login_resp.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_list_usuarios(self):
        response = client.get("/usuarios/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_create_usuario(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "nuevo@test.com",
                "password": "pass123",
                "first_name": "Juan",
                "last_name": "Perez",
                "rol": "analista_nacional",
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], "nuevo@test.com")
        self.assertEqual(data["username"], "jperez")

    def test_create_usuario_with_estado(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "estatal@test.com",
                "password": "pass123",
                "first_name": "Maria",
                "last_name": "Garcia",
                "rol": "responsable_estatal",
                "estado_id": self.estado.id,
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["estado"], self.estado.id)

    def test_create_usuario_duplicate_email(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "admin@test.com",
                "password": "pass123",
                "first_name": "Dup",
                "last_name": "User",
                "rol": "analista_nacional",
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 409)

    def test_create_usuario_estatal_without_estado(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "estatal@test.com",
                "password": "pass123",
                "first_name": "No",
                "last_name": "Estado",
                "rol": "responsable_estatal",
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)

    def test_update_usuario(self):
        user = Usuario.objects.create_user(
            username="updatable",
            email="update@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA_NACIONAL,
        )
        response = client.put(
            f"/usuarios/{user.id}",
            json={"first_name": "Updated"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["first_name"], "Updated")

    def test_deactivate_usuario(self):
        user = Usuario.objects.create_user(
            username="deactivatable",
            email="deactivate@test.com",
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
