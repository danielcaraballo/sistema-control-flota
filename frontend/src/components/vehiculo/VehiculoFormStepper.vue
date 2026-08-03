<script setup>
import { computed, ref, watch } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Select from 'primevue/select'
import Button from 'primevue/button'

const props = defineProps({
  form: { type: Object, required: true },
  submitted: { type: Boolean, default: false },
  activeIndex: { type: Number, default: 0 },
  isCreating: { type: Boolean, default: true },
  saving: { type: Boolean, default: false },
  marcas: { type: Array, default: () => [] },
  modelos: { type: Array, default: () => [] },
  tiposVehiculo: { type: Array, default: () => [] },
  tiposUso: { type: Array, default: () => [] },
  colores: { type: Array, default: () => [] },
  coloresPlaca: { type: Array, default: () => [] },
  estatusVehiculo: { type: Array, default: () => [] },
  estados: { type: Array, default: () => [] },
  gerencias: { type: Array, default: () => [] },
  centrosServicio: { type: Array, default: () => [] },
  clasesVehiculo: { type: Array, default: () => [] },
  tiposCombustible: { type: Array, default: () => [] },
})

const emit = defineEmits([
  'update:form',
  'update:activeIndex',
  'update:submitted',
  'save',
  'cancel',
])

const localForm = ref({ ...props.form })
watch(
  localForm,
  (val) => {
    emit('update:form', { ...val })
  },
  { deep: true },
)

watch(
  () => props.form,
  (newVal) => {
    if (JSON.stringify(newVal) !== JSON.stringify(localForm.value)) {
      localForm.value = { ...newVal }
    }
  },
  { deep: true },
)

const maxAnio = computed(() => new Date().getFullYear() + 1)

const filteredModelos = computed(() => {
  if (!localForm.value.marca_id) return []
  return props.modelos.filter((m) => m.marca === localForm.value.marca_id)
})

watch(
  () => localForm.value.marca_id,
  () => {
    localForm.value.modelo_id = null
  },
)

const SECCIONES = [
  { value: 0, label: 'Paso 1/3: Identificación', icon: 'pi pi-id-card' },
  { value: 1, label: 'Paso 2/3: Características', icon: 'pi pi-cog' },
  { value: 2, label: 'Paso 3/3: Asignación', icon: 'pi pi-map-marker' },
]

function prevStep() {
  if (props.activeIndex > 0) {
    emit('update:activeIndex', props.activeIndex - 1)
  }
}

function nextStep() {
  if (props.activeIndex < SECCIONES.length - 1) {
    emit('update:activeIndex', props.activeIndex + 1)
  }
}
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">
    <!-- Selector directo e indicador de paso para teléfonos móviles (< sm) -->
    <div class="sm:hidden flex flex-col gap-2 pb-2 mb-2 border-b border-card-border shrink-0">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-muted-color uppercase tracking-wider">
          Sección del vehículo
        </span>
        <span class="text-xs font-semibold text-primary">
          Paso {{ activeIndex + 1 }} de {{ SECCIONES.length }}
        </span>
      </div>
      <Select
        :modelValue="activeIndex"
        @update:modelValue="$emit('update:activeIndex', $event)"
        :options="SECCIONES"
        optionLabel="label"
        optionValue="value"
        class="w-full"
      >
        <template #value="{ value }">
          <div class="flex items-center gap-2">
            <i :class="SECCIONES[value]?.icon" class="text-[var(--p-primary-color)]" />
            <span class="font-semibold text-sm">{{ SECCIONES[value]?.label }}</span>
          </div>
        </template>
        <template #option="{ option }">
          <div class="flex items-center gap-2 py-0.5">
            <i :class="option.icon" class="text-[var(--p-primary-color)]" />
            <span>{{ option.label }}</span>
          </div>
        </template>
      </Select>
    </div>

    <!-- Renderizado directo de sección en teléfono (< sm) -->
    <div class="sm:hidden overflow-y-auto flex-1 min-h-0 py-1">
      <!-- Sección 1: Identificación -->
      <div v-if="activeIndex === 0" class="grid grid-cols-1 gap-y-3">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">
            Número económico <span class="text-red-500">*</span>
          </label>
          <InputText
            v-model="localForm.numero_economico"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.numero_economico }"
          />
          <small
            v-if="submitted && !localForm.numero_economico"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El número económico es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">
            Serial de carrocería <span class="text-red-500">*</span>
          </label>
          <InputText
            v-model="localForm.vin"
            class="w-full"
            maxlength="17"
            :class="{ 'p-invalid': submitted && !localForm.vin }"
          />
          <small v-if="submitted && !localForm.vin" class="text-xs text-red-500 dark:text-red-400">
            El serial de carrocería es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Placa</label>
          <InputText v-model="localForm.placa" class="w-full" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Color de placa</label>
          <Dropdown
            v-model="localForm.color_placa_id"
            :options="coloresPlaca"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Placa INTT</label>
          <InputText v-model="localForm.placa_intt" class="w-full" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Serial del motor</label>
          <InputText v-model="localForm.serial_motor" class="w-full" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">N° Unidad</label>
          <InputText v-model="localForm.numero_unidad" class="w-full" />
        </div>
      </div>

      <!-- Sección 2: Características -->
      <div v-else-if="activeIndex === 1" class="grid grid-cols-1 gap-y-3">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">
            Categoría <span class="text-red-500">*</span>
          </label>
          <Dropdown
            v-model="localForm.categoria_id"
            :options="tiposVehiculo"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.categoria_id }"
          />
          <small
            v-if="submitted && !localForm.categoria_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            La categoría es requerida
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Tipo de uso</label>
          <Dropdown
            v-model="localForm.tipo_uso_id"
            :options="tiposUso"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Clase <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.clase_id"
            :options="clasesVehiculo"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.clase_id }"
          />
          <small
            v-if="submitted && !localForm.clase_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            La clase es requerida
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">
            Tipo de combustible <span class="text-red-500">*</span>
          </label>
          <Dropdown
            v-model="localForm.tipo_combustible_id"
            :options="tiposCombustible"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.tipo_combustible_id }"
          />
          <small
            v-if="submitted && !localForm.tipo_combustible_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El tipo de combustible es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Marca <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.marca_id"
            :options="marcas"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.marca_id }"
          />
          <small
            v-if="submitted && !localForm.marca_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            La marca es requerida
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Modelo <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.modelo_id"
            :options="filteredModelos"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Primero selecciona una marca"
            class="w-full"
            :disabled="!localForm.marca_id"
            :class="{ 'p-invalid': submitted && !localForm.modelo_id }"
          />
          <small
            v-if="submitted && !localForm.modelo_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El modelo es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Año <span class="text-red-500">*</span></label>
          <InputNumber
            v-model="localForm.anio"
            fluid
            :useGrouping="false"
            :min="1900"
            :max="maxAnio"
            :invalid="submitted && !localForm.anio"
          />
          <small v-if="submitted && !localForm.anio" class="text-xs text-red-500 dark:text-red-400">
            El año es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Color</label>
          <Dropdown
            v-model="localForm.color_id"
            :options="colores"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Estatus <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.estatus_id"
            :options="estatusVehiculo"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.estatus_id }"
          />
          <small
            v-if="submitted && !localForm.estatus_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El estatus es requerido
          </small>
        </div>
      </div>

      <!-- Sección 3: Asignación -->
      <div v-else-if="activeIndex === 2" class="grid grid-cols-1 gap-y-3">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Estado <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.estado_id"
            :options="estados"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.estado_id }"
          />
          <small
            v-if="submitted && !localForm.estado_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El estado es requerido
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Gerencia <span class="text-red-500">*</span></label>
          <Dropdown
            v-model="localForm.gerencia_id"
            :options="gerencias"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.gerencia_id }"
          />
          <small
            v-if="submitted && !localForm.gerencia_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            La gerencia es requerida
          </small>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold">Unidad usuaria</label>
          <Dropdown
            v-model="localForm.unidad_usuaria_id"
            :options="gerencias"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            showClear
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-semibold"
            >Emplazamiento <span class="text-red-500">*</span></label
          >
          <Dropdown
            v-model="localForm.emplazamiento_id"
            :options="centrosServicio"
            optionLabel="nombre"
            optionValue="id"
            placeholder="Seleccionar"
            class="w-full"
            :class="{ 'p-invalid': submitted && !localForm.emplazamiento_id }"
          />
          <small
            v-if="submitted && !localForm.emplazamiento_id"
            class="text-xs text-red-500 dark:text-red-400"
          >
            El emplazamiento es requerido
          </small>
        </div>
      </div>
    </div>

    <!-- Navegación móvil asistida paso a paso (< sm) -->
    <div
      class="sm:hidden flex items-center justify-between gap-2 pt-2.5 mt-2 border-t border-card-border shrink-0"
    >
      <Button
        label="Anterior"
        icon="pi pi-arrow-left"
        severity="secondary"
        size="small"
        :disabled="activeIndex === 0"
        @click="prevStep"
      />
      <Button
        v-if="activeIndex < SECCIONES.length - 1"
        label="Siguiente"
        icon="pi pi-arrow-right"
        iconPos="right"
        severity="secondary"
        size="small"
        @click="nextStep"
      />
      <span
        v-else
        class="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1"
      >
        <i class="pi pi-check-circle text-sm" /> 3/3 Completado
      </span>
    </div>

    <!-- Vista de pestañas para escritorio/tablet (sm:flex) -->
    <TabView
      :activeIndex="activeIndex"
      @update:activeIndex="$emit('update:activeIndex', $event)"
      scrollable
      class="hidden sm:flex flex-1 flex-col min-h-0"
      :pt="{
        root: { class: 'flex-1 flex flex-col min-h-0 overflow-hidden' },
        panelContainer: { class: 'overflow-y-auto flex-1 min-h-0' },
      }"
    >
      <TabPanel>
        <template #header> <i class="pi pi-id-card mr-2" />Identificación </template>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 sm:gap-y-2">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Número económico <span class="text-red-500">*</span></label
            >
            <InputText
              v-model="localForm.numero_economico"
              class="w-full"
              :class="{ 'p-invalid': submitted && !localForm.numero_economico }"
            />
            <small
              v-if="submitted && !localForm.numero_economico"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El número económico es requerido
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Serial de carrocería <span class="text-red-500">*</span></label
            >
            <InputText
              v-model="localForm.vin"
              class="w-full"
              maxlength="17"
              :class="{ 'p-invalid': submitted && !localForm.vin }"
            />
            <small
              v-if="submitted && !localForm.vin"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El serial de carrocería es requerido
            </small>
          </div>
          <div
            class="col-span-1 sm:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-x-4 gap-y-3 sm:gap-y-2"
          >
            <div class="flex flex-col gap-1">
              <label class="text-sm font-semibold">Placa</label>
              <InputText v-model="localForm.placa" class="w-full" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-semibold">Color de placa</label>
              <Dropdown
                v-model="localForm.color_placa_id"
                :options="coloresPlaca"
                optionLabel="nombre"
                optionValue="id"
                placeholder="Seleccionar"
                class="w-full"
                showClear
              />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-semibold">Placa INTT</label>
              <InputText v-model="localForm.placa_intt" class="w-full" />
            </div>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Serial del motor</label>
            <InputText v-model="localForm.serial_motor" class="w-full" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">N° Unidad</label>
            <InputText v-model="localForm.numero_unidad" class="w-full" />
          </div>
        </div>
      </TabPanel>

      <TabPanel>
        <template #header> <i class="pi pi-cog mr-2" />Características </template>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 sm:gap-y-2">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Categoría <span class="text-red-500">*</span></label
            >
            <Dropdown
              v-model="localForm.categoria_id"
              :options="tiposVehiculo"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              :class="{ 'p-invalid': submitted && !localForm.categoria_id }"
            />
            <small
              v-if="submitted && !localForm.categoria_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              La categoría es requerida
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Tipo de uso</label>
            <Dropdown
              v-model="localForm.tipo_uso_id"
              :options="tiposUso"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              showClear
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Clase <span class="text-red-500">*</span></label>
            <Dropdown
              v-model="localForm.clase_id"
              :options="clasesVehiculo"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              :class="{ 'p-invalid': submitted && !localForm.clase_id }"
            />
            <small
              v-if="submitted && !localForm.clase_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              La clase es requerida
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Tipo de combustible <span class="text-red-500">*</span></label
            >
            <Dropdown
              v-model="localForm.tipo_combustible_id"
              :options="tiposCombustible"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              :class="{ 'p-invalid': submitted && !localForm.tipo_combustible_id }"
            />
            <small
              v-if="submitted && !localForm.tipo_combustible_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El tipo de combustible es requerido
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Marca <span class="text-red-500">*</span></label>
            <Dropdown
              v-model="localForm.marca_id"
              :options="marcas"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              :class="{ 'p-invalid': submitted && !localForm.marca_id }"
            />
            <small
              v-if="submitted && !localForm.marca_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              La marca es requerida
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Modelo <span class="text-red-500">*</span></label>
            <Dropdown
              v-model="localForm.modelo_id"
              :options="filteredModelos"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Primero selecciona una marca"
              class="w-full"
              :disabled="!localForm.marca_id"
              :class="{ 'p-invalid': submitted && !localForm.modelo_id }"
            />
            <small
              v-if="submitted && !localForm.modelo_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El modelo es requerido
            </small>
          </div>
          <div
            class="col-span-1 sm:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-x-4 gap-y-3 sm:gap-y-2"
          >
            <div class="flex flex-col gap-1 min-w-0">
              <label class="text-sm font-semibold">Año <span class="text-red-500">*</span></label>
              <InputNumber
                v-model="localForm.anio"
                fluid
                :useGrouping="false"
                :min="1900"
                :max="maxAnio"
                :invalid="submitted && !localForm.anio"
              />
              <small
                v-if="submitted && !localForm.anio"
                class="text-xs text-red-500 dark:text-red-400"
              >
                El año es requerido
              </small>
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-semibold">Color</label>
              <Dropdown
                v-model="localForm.color_id"
                :options="colores"
                optionLabel="nombre"
                optionValue="id"
                placeholder="Seleccionar"
                class="w-full"
                showClear
              />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-semibold"
                >Estatus <span class="text-red-500">*</span></label
              >
              <Dropdown
                v-model="localForm.estatus_id"
                :options="estatusVehiculo"
                optionLabel="nombre"
                optionValue="id"
                placeholder="Seleccionar"
                class="w-full"
                :class="{ 'p-invalid': submitted && !localForm.estatus_id }"
              />
              <small
                v-if="submitted && !localForm.estatus_id"
                class="text-xs text-red-500 dark:text-red-400"
              >
                El estatus es requerido
              </small>
            </div>
          </div>
        </div>
      </TabPanel>

      <TabPanel>
        <template #header> <i class="pi pi-map-marker mr-2" />Asignación </template>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 sm:gap-y-2">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Estado <span class="text-red-500">*</span></label>
            <Dropdown
              v-model="localForm.estado_id"
              :options="estados"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              panelClass="max-w-xs"
              :pt="{ item: { class: 'truncate' } }"
              :class="{ 'p-invalid': submitted && !localForm.estado_id }"
            />
            <small
              v-if="submitted && !localForm.estado_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El estado es requerido
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Gerencia <span class="text-red-500">*</span></label
            >
            <Dropdown
              v-model="localForm.gerencia_id"
              :options="gerencias"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              panelClass="max-w-xs"
              :pt="{ item: { class: 'truncate' } }"
              :class="{ 'p-invalid': submitted && !localForm.gerencia_id }"
            />
            <small
              v-if="submitted && !localForm.gerencia_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              La gerencia es requerida
            </small>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold">Unidad usuaria</label>
            <Dropdown
              v-model="localForm.unidad_usuaria_id"
              :options="gerencias"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              panelClass="max-w-xs"
              :pt="{ item: { class: 'truncate' } }"
              showClear
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-semibold"
              >Emplazamiento <span class="text-red-500">*</span></label
            >
            <Dropdown
              v-model="localForm.emplazamiento_id"
              :options="centrosServicio"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Seleccionar"
              class="w-full"
              panelClass="max-w-xs"
              :pt="{ item: { class: 'truncate' } }"
              :class="{ 'p-invalid': submitted && !localForm.emplazamiento_id }"
            />
            <small
              v-if="submitted && !localForm.emplazamiento_id"
              class="text-xs text-red-500 dark:text-red-400"
            >
              El emplazamiento es requerido
            </small>
          </div>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>
