<script setup lang="ts">
import {MagnifyingGlassIcon} from '@heroicons/vue/24/solid'
import Card from "../components/Card.vue"
import {ref} from "vue";
import Spinner from "../components/Spinner.vue";
import {api} from "../api";

let searchTerm = ref('')
let results = ref([])
let loading = ref(false)

const search = () => {
  if (searchTerm.value.length >= 1) {
    loading.value = true;
    api.searchSightings(searchTerm.value)
        .then(data => {
          results.value = data;
        })
        .catch(error => {})
        .finally(() => {
          loading.value = false
        })
  } else {
    results.value = [];
  }
};
</script>

<template>
  <Card>
    <div class="flex flex-col space-y-6">
      <div class="-ml-4 -mt-4 flex flex-wrap items-center justify-between sm:flex-nowrap">
        <div class="ml-4 mt-4">
          <h3 class="text-xl font-semibold leading-6 text-gray-900">Search asteroid sightings</h3>
          <p class="mt-1 text-sm text-gray-500">From here you can search for asteroid sightings from its matrix,
            observatory, device,...
          </p>
        </div>
        <div v-if="loading">
          <Spinner></Spinner>
        </div>
      </div>
      <form class="space-y-2">
        <div class="relative mt-2 rounded-md shadow-sm">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" aria-hidden="true"/>
          </div>
          <input type="text" name="search" id="search" v-model="searchTerm" @input="search"
                 class="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6"
                 placeholder="000110001100, de_0123, ..."/>
        </div>
      </form>

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
                <tbody v-if="results.length >= 1 && !loading" class="divide-y divide-gray-200 bg-white">
                <tr v-for="sighting in results" :key="sighting.id">
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
</template>

<style scoped>

</style>