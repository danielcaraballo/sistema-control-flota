from django.test import TestCase
from ninja.testing import TestClient

from ninja_jwt.tokens import RefreshToken

from config.api import api
from usuarios.models import Usuario

from .models import CentroDeServicio, Estado, Gerencia

client = TestClient(api)


class TestOrganizacionAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado", estatus_activo=True)
        cls.gerencia = Gerencia.objects.create(nombre="Gerencia Test", estatus_activo=True)
        cls.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.refresh_token = str(refresh)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_list_estados(self):
        response = client.get("/organizacion/estados/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertNotEqual(len(data), 0)
        self.assertIn("Lara", [e["nombre"] for e in data])

    def test_list_estados_only_active(self):
        Estado.objects.create(nombre="Inactivo", estatus_activo=False)
        response = client.get("/organizacion/estados/", headers=self.headers)
        data = response.json()
        for estado in data:
            self.assertTrue(estado["estatus_activo"])
        self.assertNotIn("Inactivo", [e["nombre"] for e in data])

    def test_list_gerencias(self):
        response = client.get("/organizacion/gerencias/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("Gerencia Test", [e["nombre"] for e in data])

    def test_list_gerencias_only_active(self):
        Gerencia.objects.create(nombre="Inactiva", estatus_activo=False)
        response = client.get("/organizacion/gerencias/", headers=self.headers)
        data = response.json()
        for gerencia in data:
            self.assertTrue(gerencia["estatus_activo"])
        self.assertNotIn("Inactiva", [e["nombre"] for e in data])

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
            rol=Usuario.Rol.NACIONAL,
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
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado 2", estatus_activo=True)
        cls.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_list_usuarios(self):
        response = client.get("/usuarios/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        emails = [u["email"] for u in data]
        self.assertIn("admin@test.com", emails)

    def test_create_usuario(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "nuevo@test.com",
                "password": "pass123",
                "first_name": "Juan",
                "last_name": "Perez",
                "rol": "analista",
                "estado_id": self.estado.id,
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("password", data)
        self.assertEqual(data["user"]["email"], "nuevo@test.com")
        self.assertEqual(data["user"]["username"], "jperez")

    def test_create_usuario_with_estado(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "estatal@test.com",
                "password": "pass123",
                "first_name": "Maria",
                "last_name": "Garcia",
                "rol": "estatal",
                "estado_id": self.estado.id,
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user"]["estado"], self.estado.id)

    def test_create_usuario_duplicate_email(self):
        response = client.post(
            "/usuarios/",
            json={
                "email": "admin@test.com",
                "password": "pass123",
                "first_name": "Dup",
                "last_name": "User",
                "rol": "analista",
                "estado_id": self.estado.id,
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
                "rol": "estatal",
            },
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 400)

    def test_update_usuario(self):
        user = Usuario.objects.create_user(
            username="updatable",
            email="update@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA,
            estado=self.estado,
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
            rol=Usuario.Rol.ANALISTA,
            estado=self.estado,
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
            username="analista_user",
            email="analista@test.com",
            password="pass123",
            rol=Usuario.Rol.ANALISTA,
            estado=self.estado,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "analista_user", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/usuarios/", headers=headers)
        self.assertEqual(response.status_code, 403)


class TestEstadoCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado", estatus_activo=True)
        cls.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_get_estado(self):
        response = client.get(f"/organizacion/estados/{self.estado.id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Test Estado")

    def test_get_estado_not_found(self):
        response = client.get("/organizacion/estados/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_create_estado(self):
        response = client.post(
            "/organizacion/estados/",
            headers=self.headers,
            json={"nombre": "Nuevo Estado"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Nuevo Estado")

    def test_create_estado_duplicate(self):
        response = client.post(
            "/organizacion/estados/",
            headers=self.headers,
            json={"nombre": "Test Estado"},
        )
        self.assertEqual(response.status_code, 409)

    def test_update_estado(self):
        response = client.put(
            f"/organizacion/estados/{self.estado.id}",
            headers=self.headers,
            json={"nombre": "Estado Actualizado"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Estado Actualizado")

    def test_deactivate_estado(self):
        response = client.delete(
            f"/organizacion/estados/{self.estado.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.estado.refresh_from_db()
        self.assertFalse(self.estado.estatus_activo)

    def test_list_estados_incluir_inactivos(self):
        Estado.objects.create(nombre="Inactivo", estatus_activo=False)
        response = client.get("/organizacion/estados/?incluir_inactivos=true", headers=self.headers)
        nombres = [e["nombre"] for e in response.json()]
        self.assertIn("Inactivo", nombres)

    def test_non_nacional_cannot_create_estado(self):
        mecanico = Usuario.objects.create_user(
            username="mecanico_est",
            email="mecanico_est@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "mecanico_est", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/organizacion/estados/",
            headers=headers,
            json={"nombre": "No Permitido"},
        )
        self.assertEqual(response.status_code, 403)


class TestGerenciaCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gerencia = Gerencia.objects.create(nombre="Test Gerencia", estatus_activo=True)
        cls.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_get_gerencia(self):
        response = client.get(f"/organizacion/gerencias/{self.gerencia.id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Test Gerencia")

    def test_get_gerencia_not_found(self):
        response = client.get("/organizacion/gerencias/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_create_gerencia(self):
        response = client.post(
            "/organizacion/gerencias/",
            headers=self.headers,
            json={"nombre": "Nueva Gerencia"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Nueva Gerencia")

    def test_create_gerencia_duplicate(self):
        response = client.post(
            "/organizacion/gerencias/",
            headers=self.headers,
            json={"nombre": "Test Gerencia"},
        )
        self.assertEqual(response.status_code, 409)

    def test_update_gerencia(self):
        response = client.put(
            f"/organizacion/gerencias/{self.gerencia.id}",
            headers=self.headers,
            json={"nombre": "Gerencia Actualizada"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Gerencia Actualizada")

    def test_deactivate_gerencia(self):
        response = client.delete(
            f"/organizacion/gerencias/{self.gerencia.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.gerencia.refresh_from_db()
        self.assertFalse(self.gerencia.estatus_activo)


class TestCentroDeServicioCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado = Estado.objects.create(nombre="Test Estado CS", estatus_activo=True)
        cls.cs = CentroDeServicio.objects.create(
            nombre="Test Centro", estado=cls.estado, estatus_activo=True
        )
        cls.user = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_list_centros_servicio(self):
        response = client.get("/organizacion/centros-servicio/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        nombres = [c["nombre"] for c in response.json()]
        self.assertIn("Test Centro", nombres)

    def test_list_centros_servicio_only_active(self):
        CentroDeServicio.objects.create(nombre="Inactivo", estado=self.estado, estatus_activo=False)
        response = client.get("/organizacion/centros-servicio/", headers=self.headers)
        nombres = [c["nombre"] for c in response.json()]
        self.assertNotIn("Inactivo", nombres)

    def test_list_centros_servicio_incluir_inactivos(self):
        CentroDeServicio.objects.create(nombre="Inactivo", estado=self.estado, estatus_activo=False)
        response = client.get(
            "/organizacion/centros-servicio/?incluir_inactivos=true", headers=self.headers
        )
        nombres = [c["nombre"] for c in response.json()]
        self.assertIn("Inactivo", nombres)

    def test_get_centro_servicio(self):
        response = client.get(f"/organizacion/centros-servicio/{self.cs.id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Test Centro")
        self.assertEqual(response.json()["estado_nombre"], "Test Estado CS")

    def test_get_centro_servicio_not_found(self):
        response = client.get("/organizacion/centros-servicio/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_create_centro_servicio(self):
        response = client.post(
            "/organizacion/centros-servicio/",
            headers=self.headers,
            json={"nombre": "Nuevo Centro", "estado_id": self.estado.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Nuevo Centro")
        self.assertEqual(response.json()["estado_nombre"], "Test Estado CS")

    def test_create_centro_servicio_duplicate(self):
        response = client.post(
            "/organizacion/centros-servicio/",
            headers=self.headers,
            json={"nombre": "Test Centro", "estado_id": self.estado.id},
        )
        self.assertEqual(response.status_code, 409)

    def test_update_centro_servicio(self):
        response = client.put(
            f"/organizacion/centros-servicio/{self.cs.id}",
            headers=self.headers,
            json={"nombre": "Centro Actualizado"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Centro Actualizado")

    def test_deactivate_centro_servicio(self):
        response = client.delete(
            f"/organizacion/centros-servicio/{self.cs.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.cs.refresh_from_db()
        self.assertFalse(self.cs.estatus_activo)

    def test_non_nacional_cannot_create_centro_servicio(self):
        mecanico = Usuario.objects.create_user(
            username="mecanico_cs",
            email="mecanico_cs@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "mecanico_cs", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/organizacion/centros-servicio/",
            headers=headers,
            json={"nombre": "No Permitido", "estado_id": self.estado.id},
        )
        self.assertEqual(response.status_code, 403)

    def test_mecanico_can_list_centros_servicio(self):
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
        response = client.get("/organizacion/centros-servicio/", headers=headers)
        self.assertEqual(response.status_code, 200)
