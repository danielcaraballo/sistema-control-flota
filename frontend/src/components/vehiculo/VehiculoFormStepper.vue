<script setup>
import { computed, ref, watch } from 'vue'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'
import Message from 'primevue/message'

const props = defineProps({
  form: { type: Object, required: true },
  submitted: { type: Boolean, default: false },
  activeStep: { type: Number, default: 1 },
  errorMessage: { type: String, default: '' },
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
})

const emit = defineEmits(['update:form', 'update:activeStep', 'update:submitted', 'save', 'cancel'])

const localForm = ref({ ...props.form })
watch(
  localForm,
  (val) => {
    emit('update:form', { ...val })
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

function validateStep(step) {
  const f = localForm.value
  if (step === 1) return f.numero_economico && f.vin
  if (step === 2) return f.categoria_id && f.marca_id && f.modelo_id && f.anio && f.estatus_id
  if (step === 3) return f.estado_id && f.gerencia_id && f.emplazamiento_id
  return true
}

function goToStep(step) {
  emit('update:submitted', true)
  if (!validateStep(props.activeStep)) return
  emit('update:activeStep', step)
}

function goBack() {
  emit('update:activeStep', props.activeStep - 1)
}

function label(id, list) {
  return list.find((i) => i.id === id)?.nombre ?? ''
}
</script>

<template>
  <div class="flex flex-col h-full">
    <Message v-if="errorMessage" severity="error" :closable="false" class="!mb-4 !text-xs">
      {{ errorMessage }}
    </Message>

    <Stepper
      :value="activeStep"
      :linear="isCreating"
      @update:value="!isCreating && $emit('update:activeStep', $event)"
      class="flex-1 flex flex-col min-h-0"
    >
      <div class="flex gap-4 flex-1 min-h-0">
        <StepList class="flex-col w-44 shrink-0 border-r border-card-border pr-4">
          <Step :value="1">Identificación</Step>
          <Step :value="2">Características</Step>
          <Step :value="3">Asignación</Step>
          <Step :value="4">Confirmar</Step>
        </StepList>
        <StepPanels class="flex-1">
          <StepPanel :value="1">
            <div class="grid grid-cols-2 gap-x-4 gap-y-2">
              <div class="flex flex-col gap-1 col-span-2">
                <label class="text-sm font-semibold">Número económico</label>
                <InputText
                  v-model="localForm.numero_economico"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.numero_economico }"
                />
                <small v-if="submitted && !localForm.numero_economico" class="text-xs text-red-500">
                  El número económico es requerido
                </small>
              </div>
              <div class="flex flex-col gap-1 col-span-2">
                <label class="text-sm font-semibold">Serial de carrocería</label>
                <InputText
                  v-model="localForm.vin"
                  class="w-full"
                  maxlength="17"
                  :class="{ 'p-invalid': submitted && !localForm.vin }"
                />
                <small v-if="submitted && !localForm.vin" class="text-xs text-red-500">
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
              <div class="flex flex-col gap-1 col-span-2">
                <label class="text-sm font-semibold">N° Unidad</label>
                <InputText v-model="localForm.numero_unidad" class="w-full" />
              </div>
            </div>
          </StepPanel>

          <StepPanel :value="2">
            <div class="grid grid-cols-2 gap-x-4 gap-y-2">
              <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold">Categoría</label>
                <Dropdown
                  v-model="localForm.categoria_id"
                  :options="tiposVehiculo"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.categoria_id }"
                />
                <small v-if="submitted && !localForm.categoria_id" class="text-xs text-red-500">
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
                <label class="text-sm font-semibold">Marca</label>
                <Dropdown
                  v-model="localForm.marca_id"
                  :options="marcas"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.marca_id }"
                />
                <small v-if="submitted && !localForm.marca_id" class="text-xs text-red-500">
                  La marca es requerida
                </small>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold">Modelo</label>
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
                <small v-if="submitted && !localForm.modelo_id" class="text-xs text-red-500">
                  El modelo es requerido
                </small>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold">Año</label>
                <InputNumber
                  v-model="localForm.anio"
                  class="w-full"
                  :useGrouping="false"
                  :min="1900"
                  :max="maxAnio"
                  :class="{ 'p-invalid': submitted && !localForm.anio }"
                />
                <small v-if="submitted && !localForm.anio" class="text-xs text-red-500">
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
                <label class="text-sm font-semibold">Estatus</label>
                <Dropdown
                  v-model="localForm.estatus_id"
                  :options="estatusVehiculo"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.estatus_id }"
                />
                <small v-if="submitted && !localForm.estatus_id" class="text-xs text-red-500">
                  El estatus es requerido
                </small>
              </div>
            </div>
          </StepPanel>

          <StepPanel :value="3">
            <div class="grid grid-cols-2 gap-x-4 gap-y-2">
              <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold">Estado</label>
                <Dropdown
                  v-model="localForm.estado_id"
                  :options="estados"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.estado_id }"
                />
                <small v-if="submitted && !localForm.estado_id" class="text-xs text-red-500">
                  El estado es requerido
                </small>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-sm font-semibold">Gerencia</label>
                <Dropdown
                  v-model="localForm.gerencia_id"
                  :options="gerencias"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.gerencia_id }"
                />
                <small v-if="submitted && !localForm.gerencia_id" class="text-xs text-red-500">
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
                <label class="text-sm font-semibold">Emplazamiento</label>
                <Dropdown
                  v-model="localForm.emplazamiento_id"
                  :options="centrosServicio"
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar"
                  class="w-full"
                  :class="{ 'p-invalid': submitted && !localForm.emplazamiento_id }"
                />
                <small v-if="submitted && !localForm.emplazamiento_id" class="text-xs text-red-500">
                  El emplazamiento es requerido
                </small>
              </div>
            </div>
          </StepPanel>

          <StepPanel :value="4">
            <div class="space-y-2">
              <p class="text-sm text-muted-color font-semibold mb-2">
                Revisa los datos antes de {{ isCreating ? 'crear' : 'guardar' }}:
              </p>

              <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                <i class="pi pi-id-card text-primary" /> Identificación
              </div>
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 mb-2">
                <span class="text-muted-color text-sm">N° Económico</span>
                <span class="text-sm font-medium">{{ localForm.numero_economico }}</span>
                <span class="text-muted-color text-sm">Serial carrocería</span>
                <span class="text-sm font-medium font-mono">{{ localForm.vin }}</span>
                <span class="text-muted-color text-sm">Placa</span>
                <span class="text-sm font-medium">{{ localForm.placa || '—' }}</span>
                <span class="text-muted-color text-sm">Color de placa</span>
                <span class="text-sm font-medium">{{
                  label(localForm.color_placa_id, coloresPlaca) || '—'
                }}</span>
                <span class="text-muted-color text-sm">Placa INTT</span>
                <span class="text-sm font-medium">{{ localForm.placa_intt || '—' }}</span>
                <span class="text-muted-color text-sm">Serial del motor</span>
                <span class="text-sm font-medium">{{ localForm.serial_motor || '—' }}</span>
                <span class="text-muted-color text-sm">N° Unidad</span>
                <span class="text-sm font-medium">{{ localForm.numero_unidad || '—' }}</span>
              </div>

              <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                <i class="pi pi-cog text-primary" /> Características
              </div>
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 mb-2">
                <span class="text-muted-color text-sm">Categoría</span>
                <span class="text-sm font-medium">{{
                  label(localForm.categoria_id, tiposVehiculo)
                }}</span>
                <span class="text-muted-color text-sm">Tipo de uso</span>
                <span class="text-sm font-medium">{{
                  label(localForm.tipo_uso_id, tiposUso) || '—'
                }}</span>
                <span class="text-muted-color text-sm">Marca</span>
                <span class="text-sm font-medium">{{ label(localForm.marca_id, marcas) }}</span>
                <span class="text-muted-color text-sm">Modelo</span>
                <span class="text-sm font-medium">{{ label(localForm.modelo_id, modelos) }}</span>
                <span class="text-muted-color text-sm">Año</span>
                <span class="text-sm font-medium">{{ localForm.anio }}</span>
                <span class="text-muted-color text-sm">Color</span>
                <span class="text-sm font-medium">{{
                  label(localForm.color_id, colores) || '—'
                }}</span>
                <span class="text-muted-color text-sm">Estatus</span>
                <span class="text-sm font-medium">{{
                  label(localForm.estatus_id, estatusVehiculo)
                }}</span>
              </div>

              <div class="text-sm font-semibold text-color mb-2 flex items-center gap-2">
                <i class="pi pi-map-marker text-primary" /> Asignación
              </div>
              <div class="grid grid-cols-2 gap-x-4 gap-y-1">
                <span class="text-muted-color text-sm">Estado</span>
                <span class="text-sm font-medium">{{ label(localForm.estado_id, estados) }}</span>
                <span class="text-muted-color text-sm">Gerencia</span>
                <span class="text-sm font-medium">{{
                  label(localForm.gerencia_id, gerencias)
                }}</span>
                <span class="text-muted-color text-sm">Unidad usuaria</span>
                <span class="text-sm font-medium">{{
                  label(localForm.unidad_usuaria_id, gerencias) || '—'
                }}</span>
                <span class="text-muted-color text-sm">Emplazamiento</span>
                <span class="text-sm font-medium">{{
                  label(localForm.emplazamiento_id, centrosServicio)
                }}</span>
              </div>
            </div>
          </StepPanel>
        </StepPanels>
      </div>
    </Stepper>

    <div class="flex justify-between w-full pt-4 mt-auto">
      <div>
        <Button
          v-if="activeStep > 1"
          label="Atrás"
          severity="secondary"
          icon="pi pi-arrow-left"
          @click="goBack"
        />
      </div>
      <div class="flex gap-2">
        <Button
          v-if="activeStep < 4"
          label="Cancelar"
          severity="secondary"
          @click="$emit('cancel')"
        />
        <Button
          v-if="activeStep < 4"
          label="Siguiente"
          icon="pi pi-arrow-right"
          iconPos="right"
          @click="goToStep(activeStep + 1)"
        />
        <Button
          v-if="activeStep === 4"
          :label="isCreating ? 'Crear vehículo' : 'Guardar cambios'"
          icon="pi pi-check"
          :loading="saving"
          :disabled="saving"
          @click="$emit('save')"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.p-steplist .p-step {
  justify-content: flex-start;
  text-align: left;
}
</style>
