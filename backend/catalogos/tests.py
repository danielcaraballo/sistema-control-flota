from django.test import TestCase
from ninja.testing import TestClient

from config.api import api
from usuarios.models import Usuario

from .models import (
    Color,
    Marca,
    Modelo,
    SistemaAfectado,
    TipoFalla,
    TipoUso,
    TipoVehiculo,
)

client = TestClient(api)


class TestCatalogosAPI(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(nombre="Test Marca")
        self.modelo = Modelo.objects.create(
            nombre="Test Modelo", marca=self.marca)
        self.tv = TipoVehiculo.objects.create(nombre="Test Tipo Vehiculo")
        self.tu = TipoUso.objects.create(nombre="Test Tipo Uso")
        self.color = Color.objects.create(nombre="Test Color")
        self.sa = SistemaAfectado.objects.create(nombre="Test Sistema")
        self.tf = TipoFalla.objects.create(
            descripcion="Test Falla", sistema_afectado=self.sa)

        self.admin = Usuario.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            rol=Usuario.Rol.NACIONAL,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(login_resp.status_code, 200, "Login falló en setUp")
        self.token = login_resp.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    # ─── Marcas ───────────────────────────────────────────────────────────

    def test_list_marcas(self):
        response = client.get("/catalogos/marcas/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        nombres = [m["nombre"] for m in response.json()]
        self.assertIn("Test Marca", nombres)

    def test_list_marcas_only_active(self):
        Marca.objects.create(nombre="Inactiva", estatus_activo=False)
        response = client.get("/catalogos/marcas/", headers=self.headers)
        nombres = [m["nombre"] for m in response.json()]
        self.assertNotIn("Inactiva", nombres)

    def test_list_marcas_incluir_inactivos(self):
        Marca.objects.create(nombre="Inactiva", estatus_activo=False)
        response = client.get(
            "/catalogos/marcas/?incluir_inactivos=true", headers=self.headers)
        nombres = [m["nombre"] for m in response.json()]
        self.assertIn("Inactiva", nombres)

    def test_create_marca(self):
        response = client.post(
            "/catalogos/marcas/",
            headers=self.headers,
            json={"nombre": "ZZ Test Marca Nueva"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "ZZ Test Marca Nueva")

    def test_create_marca_duplicate(self):
        response = client.post(
            "/catalogos/marcas/",
            headers=self.headers,
            json={"nombre": "Test Marca"},
        )
        self.assertEqual(response.status_code, 409)

    def test_update_marca(self):
        response = client.put(
            f"/catalogos/marcas/{self.marca.id}",
            headers=self.headers,
            json={"nombre": "Toyota Actualizada"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Toyota Actualizada")

    def test_deactivate_marca(self):
        response = client.delete(
            f"/catalogos/marcas/{self.marca.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.marca.refresh_from_db()
        self.assertFalse(self.marca.estatus_activo)

    def test_get_marca(self):
        response = client.get(
            f"/catalogos/marcas/{self.marca.id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Test Marca")

    def test_get_marca_not_found(self):
        response = client.get("/catalogos/marcas/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    # ─── Modelos ──────────────────────────────────────────────────────────

    def test_list_modelos(self):
        response = client.get("/catalogos/modelos/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("marca_nombre", data[0])

    def test_create_modelo(self):
        response = client.post(
            "/catalogos/modelos/",
            headers=self.headers,
            json={"nombre": "Corolla", "marca_id": self.marca.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Corolla")

    def test_create_modelo_invalid_marca(self):
        response = client.post(
            "/catalogos/modelos/",
            headers=self.headers,
            json={"nombre": "X", "marca_id": 99999},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_modelo_duplicate(self):
        response = client.post(
            "/catalogos/modelos/",
            headers=self.headers,
            json={"nombre": "Test Modelo", "marca_id": self.marca.id},
        )
        self.assertEqual(response.status_code, 409)

    def test_update_modelo(self):
        response = client.put(
            f"/catalogos/modelos/{self.modelo.id}",
            headers=self.headers,
            json={"nombre": "Tacoma"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "Tacoma")

    def test_deactivate_modelo(self):
        response = client.delete(
            f"/catalogos/modelos/{self.modelo.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.modelo.refresh_from_db()
        self.assertFalse(self.modelo.estatus_activo)

    # ─── Tipos de Vehículo ────────────────────────────────────────────────

    def test_list_tipos_vehiculo(self):
        response = client.get(
            "/catalogos/tipos-vehiculo/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        nombres = [tv["nombre"] for tv in response.json()]
        self.assertIn("Test Tipo Vehiculo", nombres)

    def test_create_tipo_vehiculo(self):
        response = client.post(
            "/catalogos/tipos-vehiculo/",
            headers=self.headers,
            json={"nombre": "ZZ Test Tipo Vehiculo Nuevo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"],
                         "ZZ Test Tipo Vehiculo Nuevo")

    def test_deactivate_tipo_vehiculo(self):
        response = client.delete(
            f"/catalogos/tipos-vehiculo/{self.tv.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.tv.refresh_from_db()
        self.assertFalse(self.tv.estatus_activo)

    # ─── Tipos de Uso ─────────────────────────────────────────────────────

    def test_list_tipos_uso(self):
        response = client.get("/catalogos/tipos-uso/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        nombres = [tu["nombre"] for tu in response.json()]
        self.assertIn("Test Tipo Uso", nombres)

    def test_create_tipo_uso(self):
        response = client.post(
            "/catalogos/tipos-uso/",
            headers=self.headers,
            json={"nombre": "8h Administrativo"},
        )
        self.assertEqual(response.status_code, 200)

    def test_deactivate_tipo_uso(self):
        response = client.delete(
            f"/catalogos/tipos-uso/{self.tu.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.tu.refresh_from_db()
        self.assertFalse(self.tu.estatus_activo)

    # ─── Colores ──────────────────────────────────────────────────────────

    def test_list_colores(self):
        response = client.get("/catalogos/colores/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        nombres = [c["nombre"] for c in response.json()]
        self.assertIn("Test Color", nombres)

    def test_create_color(self):
        response = client.post(
            "/catalogos/colores/",
            headers=self.headers,
            json={"nombre": "ZZ Test Color Nuevo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], "ZZ Test Color Nuevo")

    def test_deactivate_color(self):
        response = client.delete(
            f"/catalogos/colores/{self.color.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.color.refresh_from_db()
        self.assertFalse(self.color.estatus_activo)

    # ─── Sistemas Afectados ───────────────────────────────────────────────

    def test_list_sistemas_afectados(self):
        response = client.get(
            "/catalogos/sistemas-afectados/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        nombres = [sa["nombre"] for sa in response.json()]
        self.assertIn("Test Sistema", nombres)

    def test_create_sistema_afectado(self):
        response = client.post(
            "/catalogos/sistemas-afectados/",
            headers=self.headers,
            json={"nombre": "ZZ Test Sistema Nuevo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"],
                         "ZZ Test Sistema Nuevo")

    def test_deactivate_sistema_afectado(self):
        response = client.delete(
            f"/catalogos/sistemas-afectados/{self.sa.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.sa.refresh_from_db()
        self.assertFalse(self.sa.estatus_activo)

    # ─── Tipos de Falla ───────────────────────────────────────────────────

    def test_list_tipos_falla(self):
        response = client.get("/catalogos/tipos-falla/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        descs = [tf["descripcion"] for tf in response.json()]
        self.assertIn("Test Falla", descs)
        self.assertIn("sistema_afectado_nombre", response.json()[0])

    def test_create_tipo_falla(self):
        response = client.post(
            "/catalogos/tipos-falla/",
            headers=self.headers,
            json={
                "descripcion": "ZZ Test Falla Nueva",
                "sistema_afectado_id": self.sa.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["descripcion"],
                         "ZZ Test Falla Nueva")
        self.assertEqual(response.json()["sistema_afectado"], self.sa.id)
        self.assertEqual(response.json()["sistema_afectado_nombre"],
                         "Test Sistema")

    def test_create_tipo_falla_invalid_sa(self):
        response = client.post(
            "/catalogos/tipos-falla/",
            headers=self.headers,
            json={
                "descripcion": "ZZ Otra Falla",
                "sistema_afectado_id": 99999,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_update_tipo_falla(self):
        new_sa = SistemaAfectado.objects.create(nombre="Otro Sistema")
        response = client.put(
            f"/catalogos/tipos-falla/{self.tf.id}",
            headers=self.headers,
            json={
                "descripcion": "Falla Actualizada",
                "sistema_afectado_id": new_sa.id,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["descripcion"], "Falla Actualizada")
        self.assertEqual(response.json()["sistema_afectado"], new_sa.id)

    def test_deactivate_tipo_falla(self):
        response = client.delete(
            f"/catalogos/tipos-falla/{self.tf.id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
        self.tf.refresh_from_db()
        self.assertFalse(self.tf.estatus_activo)

    # ─── RBAC ─────────────────────────────────────────────────────────────

    def test_non_nacional_cannot_create(self):
        mecanico = Usuario.objects.create_user(
            username="mecanico",
            email="mecanico@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
        )
        login_resp = client.post(
            "/auth/login",
            json={"username": "mecanico", "password": "pass123"},
        )
        token = login_resp.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/catalogos/marcas/",
            headers=headers,
            json={"nombre": "Ford"},
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

        response = client.get("/catalogos/marcas/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        response = client.get("/catalogos/marcas/")
        self.assertEqual(response.status_code, 401)
