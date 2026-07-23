from django.test import TestCase
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken

from config.api import api
from catalogos.models import EstatusVehiculo
from organizacion.models import Estado
from usuarios.models import Usuario
from vehiculos.models import Vehiculo

client = TestClient(api)


class TestDashboardKPIs(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estado_a = Estado.objects.create(nombre="Estado A", estatus_activo=True)
        cls.estado_b = Estado.objects.create(nombre="Estado B", estatus_activo=True)

        cls.estatus_op = EstatusVehiculo.objects.create(nombre="Operativo", estatus_activo=True)
        cls.estatus_taller = EstatusVehiculo.objects.create(
            nombre="En reparacion", es_operativo=False, estatus_activo=True
        )
        cls.estatus_inac = EstatusVehiculo.objects.create(
            nombre="Inoperativo", es_operativo=False, estatus_activo=True
        )

        cls.nacional = Usuario.objects.create_user(
            username="nacional",
            email="nacional@test.com",
            password="pass123",
            rol=Usuario.Rol.NACIONAL,
        )
        cls.estatal = Usuario.objects.create_user(
            username="estatal",
            email="estatal@test.com",
            password="pass123",
            rol=Usuario.Rol.ESTATAL,
            estado=cls.estado_a,
        )
        cls.mecanico = Usuario.objects.create_user(
            username="mecanico",
            email="mecanico@test.com",
            password="pass123",
            rol=Usuario.Rol.MECANICO,
            estado=cls.estado_a,
        )

        refresh = RefreshToken.for_user(cls.nacional)
        cls.nac_token = str(refresh.access_token)
        cls.nac_headers = {"Authorization": f"Bearer {cls.nac_token}"}

        refresh = RefreshToken.for_user(cls.estatal)
        cls.est_token = str(refresh.access_token)
        cls.est_headers = {"Authorization": f"Bearer {cls.est_token}"}

        refresh = RefreshToken.for_user(cls.mecanico)
        cls.mec_token = str(refresh.access_token)
        cls.mec_headers = {"Authorization": f"Bearer {cls.mec_token}"}

    _counter = 0

    @classmethod
    def _crear_vehiculo(cls, estado, estatus, activo=True):
        from organizacion.models import CentroDeServicio, Gerencia
        from catalogos.models import Marca, Modelo, TipoVehiculo, ClaseVehiculo, TipoCombustible

        cls._counter += 1
        suf = cls._counter
        gerencia = Gerencia.objects.create(nombre=f"Gerencia {suf}", estatus_activo=True)
        centro = CentroDeServicio.objects.create(
            nombre=f"Centro {suf}", estado=estado, estatus_activo=True
        )
        marca = Marca.objects.create(nombre=f"Marca {suf}", estatus_activo=True)
        modelo = Modelo.objects.create(nombre=f"Modelo {suf}", marca=marca, estatus_activo=True)
        tipo = TipoVehiculo.objects.create(nombre=f"Tipo {suf}", estatus_activo=True)
        clase = ClaseVehiculo.objects.create(nombre=f"Clase {suf}", estatus_activo=True)
        tipo_comb = TipoCombustible.objects.create(nombre=f"Combustible {suf}", estatus_activo=True)

        Vehiculo.objects.create(
            numero_economico=f"ECO-{estado.id}-{estatus.id}-{suf}",
            vin=f"VIN{estado.id}{estatus.id}{activo}{suf}",
            numero_unidad=f"UN{estado.id}{estatus.id}{suf}",
            estado=estado,
            estatus=estatus,
            gerencia=gerencia,
            emplazamiento=centro,
            marca=marca,
            modelo=modelo,
            categoria=tipo,
            clase=clase,
            tipo_combustible=tipo_comb,
            anio=2024,
            estatus_activo=activo,
        )

    def setUp(self):
        Vehiculo.objects.all().delete()

    def _crear_data_basica(self):
        # Estado A: 3 activos, 1 inactivo
        self._crear_vehiculo(self.estado_a, self.estatus_op, activo=True)
        self._crear_vehiculo(self.estado_a, self.estatus_op, activo=True)
        self._crear_vehiculo(self.estado_a, self.estatus_taller, activo=True)
        self._crear_vehiculo(self.estado_a, self.estatus_inac, activo=False)
        # Estado B: 1 activo, 1 inactivo
        self._crear_vehiculo(self.estado_b, self.estatus_op, activo=True)
        self._crear_vehiculo(self.estado_b, self.estatus_inac, activo=False)

    # --- auth ---

    def test_kpis_unauthenticated(self):
        response = client.get("/dashboard/kpis")
        self.assertEqual(response.status_code, 401)

    def test_charts_unauthenticated(self):
        response = client.get("/dashboard/charts")
        self.assertEqual(response.status_code, 401)

    def test_nacional_unauthenticated(self):
        response = client.get("/dashboard/nacional")
        self.assertEqual(response.status_code, 401)

    # --- kpis ---

    def test_kpis_nacional_sees_all(self):
        self._crear_data_basica()
        response = client.get("/dashboard/kpis", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 6)
        self.assertEqual(data["porcentaje_operatividad"], 50.0)
        self.assertEqual(data["operativos"], 3)
        self.assertEqual(data["inactivos"], 3)
        self.assertEqual(data["completitud_promedio"], 65.0)
        statuses = {s["nombre"]: s["cantidad"] for s in data["estatus"]}
        self.assertEqual(statuses["Operativo"], 3)
        self.assertEqual(statuses["En reparacion"], 1)
        self.assertEqual(statuses["Inoperativo"], 2)
    def test_kpis_estatal_scoped(self):
        self._crear_data_basica()
        response = client.get("/dashboard/kpis", headers=self.est_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 4)
        self.assertIn("completitud_promedio", data)

    def test_kpis_mecanico_has_access(self):
        self._crear_data_basica()
        response = client.get("/dashboard/kpis", headers=self.mec_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 4)

    def test_kpis_empty(self):
        response = client.get("/dashboard/kpis", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 0)
        self.assertEqual(data["porcentaje_operatividad"], 0.0)
        self.assertEqual(data["operativos"], 0)
        self.assertEqual(data["inactivos"], 0)
        self.assertEqual(data["completitud_promedio"], 0.0)
        self.assertEqual(data["estatus"], [])

    # --- charts ---

    def test_charts_nacional(self):
        self._crear_data_basica()
        response = client.get("/dashboard/charts", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        estados = {e["estado_nombre"]: e for e in data["por_estado"]}
        self.assertEqual(estados["Estado A"]["total"], 4)
        self.assertEqual(estados["Estado A"]["activos"], 2)
        self.assertEqual(estados["Estado A"]["inactivos"], 2)
        self.assertEqual(estados["Estado A"]["operatividad"], 50.0)
        self.assertEqual(estados["Estado B"]["total"], 2)
        self.assertEqual(estados["Estado B"]["activos"], 1)
        self.assertEqual(estados["Estado B"]["inactivos"], 1)
        self.assertEqual(estados["Estado B"]["operatividad"], 50.0)
        # ordered by total desc
        self.assertEqual(data["por_estado"][0]["estado_nombre"], "Estado A")
        # new chart data
        self.assertEqual(len(data["por_marca"]), 6)
        self.assertEqual(len(data["por_anio"]), 1)
        self.assertEqual(data["por_anio"][0]["anio"], 2024)
        self.assertEqual(data["por_anio"][0]["cantidad"], 6)

    def test_charts_estatal_scoped(self):
        self._crear_data_basica()
        response = client.get("/dashboard/charts", headers=self.est_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["por_estado"]), 1)
        self.assertEqual(data["por_estado"][0]["estado_nombre"], "Estado A")
        self.assertEqual(data["por_estado"][0]["total"], 4)
        self.assertIn("por_marca", data)
        self.assertIn("por_anio", data)

    def test_charts_empty(self):
        response = client.get("/dashboard/charts", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["por_estado"], [])
        self.assertEqual(data["por_marca"], [])
        self.assertEqual(data["por_anio"], [])

    # --- nacional ---

    def test_nacional_estatal_forbidden(self):
        self._crear_data_basica()
        response = client.get("/dashboard/nacional", headers=self.est_headers)
        self.assertEqual(response.status_code, 403)

    def test_nacional_returns_data(self):
        self._crear_data_basica()
        response = client.get("/dashboard/nacional", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 6)
        self.assertEqual(data["total_estados_con_vehiculos"], 2)
        self.assertEqual(len(data["resumen_estados"]), 2)

        estados = {r["estado_nombre"]: r for r in data["resumen_estados"]}
        # Estado A: 4 total, 2 operativos, 2 inactivos, 50%
        self.assertEqual(estados["Estado A"]["total"], 4)
        self.assertEqual(estados["Estado A"]["activos"], 2)
        self.assertEqual(estados["Estado A"]["inactivos"], 2)
        self.assertEqual(estados["Estado A"]["operatividad"], 50.0)
        self.assertEqual(
            {s["nombre"] for s in estados["Estado A"]["estatus"]},
            {"Operativo", "En reparacion", "Inoperativo"},
        )
        # Estado B: 2 total, 1 activo, 1 inactivo, 50%
        self.assertEqual(estados["Estado B"]["total"], 2)
        self.assertEqual(estados["Estado B"]["activos"], 1)
        self.assertEqual(estados["Estado B"]["inactivos"], 1)
        self.assertEqual(estados["Estado B"]["operatividad"], 50.0)
        self.assertEqual(
            {s["nombre"] for s in estados["Estado B"]["estatus"]},
            {"Operativo", "Inoperativo"},
        )
        # mejor / peor (both at 50.0, Estado A is first in order)
        self.assertEqual(data["mejor_operatividad"]["estado_nombre"], "Estado A")
        self.assertEqual(data["mejor_operatividad"]["operatividad"], 50.0)
        self.assertEqual(data["peor_operatividad"]["estado_nombre"], "Estado A")
        self.assertEqual(data["peor_operatividad"]["operatividad"], 50.0)

    def test_nacional_empty(self):
        response = client.get("/dashboard/nacional", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 0)
        self.assertEqual(data["total_estados_con_vehiculos"], 0)
        self.assertEqual(data["resumen_estados"], [])
        self.assertIsNone(data["mejor_operatividad"])
        self.assertIsNone(data["peor_operatividad"])

    def test_nacional_single_state(self):
        self._crear_vehiculo(self.estado_a, self.estatus_op, activo=True)
        self._crear_vehiculo(self.estado_a, self.estatus_inac, activo=False)
        response = client.get("/dashboard/nacional", headers=self.nac_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_vehiculos"], 2)
        self.assertEqual(data["total_estados_con_vehiculos"], 1)
        self.assertEqual(len(data["resumen_estados"]), 1)
        # same state is both best and worst
        self.assertEqual(
            data["mejor_operatividad"]["estado_nombre"],
            data["peor_operatividad"]["estado_nombre"],
        )
