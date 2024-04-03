<script setup lang="ts">
import HomeIcon from './components/icons/HomeIcon.vue'
import MeteoriteIcon from './components/icons/MeteoriteIcon.vue'
import SearchIcon from './components/icons/SearchIcon.vue'
import UploadIcon from './components/icons/UploadIcon.vue'
import {useNotificationStore} from "./stores/notifications";
import Notification from "./components/Notification.vue";

const routes = [
  {
    'label': 'Home',
    'url': '/',
    'icon': HomeIcon
  },
  {
    'label': 'Asteroids',
    'url': '/asteroids',
    'icon': MeteoriteIcon
  },
  {
    'label': 'Search asteroids',
    'url': '/asteroids/search',
    'icon': SearchIcon
  },
  {
    'label': 'Upload sighting',
    'url': '/upload',
    'icon': UploadIcon
  },
]

</script>
<template>
  <Notification></Notification>

  <div class="mx-auto max-w-7xl pt-8 lg:flex lg:gap-x-16 lg:px-8">
    <h1 class="sr-only">General Settings</h1>

    <aside class="hidden lg:block lg:w-64 lg:flex-none lg:border-0 lg:py-20">
      <nav class="flex-none px-4 sm:px-6 lg:px-0">
        <ul role="list" class="flex gap-x-3 gap-y-1 whitespace-nowrap lg:flex-col">

          <li class="mb-4 items-center flex">
            <h1 class="group flex gap-x-1 rounded-xl py-2 pl-2 pr-3 text-2xl leading-6 font-extrabold items-center">
              asteroid
              <span
                  class="inline-flex items-center rounded-md bg-blue-100 px-1.5 py-0.5 text-2xl font-medium text-blue-700">
                scan
              </span>
            </h1>
          </li>

          <li v-for="route in routes">
            <RouterLink :to="route.url"
                        active-class="active-link"
                        class="group flex gap-x-3 rounded-md py-2 pl-2 pr-3 text-sm leading-6 font-semibold text-gray-700"
            >
              <component :is="route.icon"></component>
              {{ route.label }}
            </RouterLink>
          </li>

        </ul>
      </nav>
    </aside>

    <main class="px-4 py-16 sm:px-6 lg:flex-auto lg:px-0 lg:py-20 space-y-6" id="hub-content">
      <router-view></router-view>
    </main>

  </div>

</template>

<style>
.active-link {
  background-color: #3B82F6;
  color: #FFFFFF;
}
</style>
