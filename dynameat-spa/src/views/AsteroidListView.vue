<script setup>
import {ref} from 'vue';
import Card from "../components/Card.vue";
import Spinner from "../components/Spinner.vue";

const asteroids = ref(null);
const isLoading = ref(true)

fetch('http://127.0.0.1:8000/api/asteroids/')
    .then(response => response.json())
    .then(data => {
      asteroids.value = data;
      isLoading.value = false;
    });
</script>

<template>
  <Card>
    <div v-if="isLoading" class="flex w-full justify-center">
      <Spinner></Spinner>
    </div>

    <div v-else>
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto ">
          <h1 class="text-xl font-semibold leading-6 text-gray-900">Asteroids overview</h1>
          <p class="mt-1 text-sm text-gray-500">
            A complete view of all the asteroids that our algorithm has managed to classify from the scanner sightings.
          </p>
        </div>
      </div>
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="pl-8 py-3.5 text-left text-sm font-semibold text-gray-900"></th>
                  <th scope="col" class="py-3.5 px-3 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">ID
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Last sighting</th>
                </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                <tr v-for="asteroid in asteroids" :key="asteroid.id">
                  <td class="whitespace-nowrap pl-8 py-4 text-sm text-gray-500">
                    <div v-for="(row, rowIndex) in asteroid.matrix" :key="`row-${rowIndex}`" class="flex h-3">
                      <div v-for="(cell, colIndex) in row" :key="`cell-${rowIndex}-${colIndex}`"
                           :class="`flex w-3 h-3 border border-gray-400 ${cell === 1 ? 'bg-black' : 'bg-white'}`">
                      </div>
                    </div>
                  </td>
                  <td class="whitespace-nowrap py-4 px-3 text-sm font-medium text-gray-900 sm:pl-6">
                    <RouterLink :to="`/asteroids/${asteroid.id}`" class="text-blue-600 hover:text-blue-900">
                      {{ asteroid.id.substring(0, 8) }}
                    </RouterLink>
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {{ asteroid.sightings[0].date }}T{{ asteroid.sightings[0].time }}
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