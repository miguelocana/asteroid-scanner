<script setup>
import {ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import Card from "../components/Card.vue";
import Spinner from "../components/Spinner.vue";
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot,} from '@headlessui/vue'
import {ExclamationTriangleIcon} from '@heroicons/vue/20/solid'
import {useNotificationStore} from "../stores/notifications.ts";
import {api} from "../api";

const store = useNotificationStore()

const route = useRoute();
const router = useRouter();
const asteroid = ref(null)
const error = ref(null)
const loading = ref(false)
const open = ref(false)

watch(() => route.params.id, fetchData, {immediate: true})

async function fetchData(id) {
  error.value = asteroid.value = null
  loading.value = true

  try {
    asteroid.value = await fetch(`http://127.0.0.1:8000/api/asteroids/${id}`).then(response => response.json())

  } catch (err) {
    error.value = err.toString()
  } finally {
    loading.value = false
  }
}

const deleteAsteroid = async () => {
  api.deleteAsteroid(route.params.id)
      .then(data => {
        router.push({name: 'asteroid-list'});
        store.setNotification({
          message: 'Asteroid deleted',
          detail: 'Your asteroid and all its sightings have been deleted.',
          type: 'success'
        })
      })
      .catch(error => {
        store.setNotification({
          message: 'Something went wrong',
          detail: 'Failed to delete the asteroid.',
          type: 'error'
        })
      })
      .finally(() => {
        open.value = false;
      });
};

</script>


<template>
  <Card>
    <div v-if="loading" class="flex w-full justify-center">
      <Spinner></Spinner>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="asteroid" class="justify-center space-y-4 space-x-6  w-full">

      <div class="px-6 w-full border-b border-gray-400 pb-4">
        <div class="flex justify-between items-center">
          <div class="flex">
            <div class="mr-4 flex-shrink-0">
              <div v-for="(row, rowIndex) in asteroid.matrix" :key="`row-${rowIndex}`"
                   class="flex justify-start">
                <div v-for="(cell, colIndex) in row" :key="`cell-${rowIndex}-${colIndex}`"
                     :class="`flex w-3 h-3 border border-gray-400 ${cell === 1 ? 'bg-black' : 'bg-white'}`">
                </div>
              </div>
            </div>
            <div class="space-y-1">
              <h1 class="text-2xl font-light leading-6 text-gray-900">Asteroid <span
                  class="font-semibold">{{ asteroid.id.substring(0, 8) }}</span></h1>
              <span
                  class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-md font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">{{
                  asteroid.normalized_matrix
                }}</span>
            </div>
          </div>
          <button type="button" @click="open = true"
                  class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto">
            Delete
          </button>
        </div>
      </div>


      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-base font-semibold leading-6 text-gray-900">Sightings</h1>
        </div>
      </div>
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                    ID
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Datetime</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Observatory</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Device</th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">

                  </th>

                </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                <tr v-for="sighting in asteroid.sightings" :key="sighting.id">
                  <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                    {{ sighting.id.substring(0, 8) }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500 flex-col">
                    {{ sighting.date }}T{{ sighting.time }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ sighting.observatory.code }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ sighting.device.code }}</td>
                  <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <div v-for="(row, rowIndex) in sighting.fmt_matrix" :key="`row-${rowIndex}`"
                         class="flex justify-start">
                      <div v-for="(cell, colIndex) in row" :key="`cell-${rowIndex}-${colIndex}`"
                           :class="`flex w-6 h-6 border border-gray-400 ${cell === 1 ? 'bg-black' : 'bg-white'}`">
                      </div>
                    </div>
                  </td>
                </tr>

                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  </Card>

  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="relative z-10" @close="open = false">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100"
                       leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"/>
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300"
                           enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                           enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200"
                           leave-from="opacity-100 translate-y-0 sm:scale-100"
                           leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel
                class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                  <div
                      class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                    <ExclamationTriangleIcon class="h-6 w-6 text-red-600" aria-hidden="true"/>
                  </div>
                  <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">Delete asteroid
                    </DialogTitle>
                    <div class="mt-2">
                      <p class="text-sm text-gray-500">Are you sure you want to eliminate the asteroid? All related
                        sightings will be deleted.</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button type="submit" @click="deleteAsteroid"
                        class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
                >Delete
                </button>
                <button type="button"
                        class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                        @click="open = false" ref="cancelButtonRef">Cancel
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>

</template>
