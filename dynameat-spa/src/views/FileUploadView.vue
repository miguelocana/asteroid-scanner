<script setup lang="ts">
import Card from "../components/Card.vue";
import {ref} from "vue";
import Spinner from "../components/Spinner.vue";
import {useNotificationStore} from "../stores/notifications";
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {api} from "../api";

const store = useNotificationStore()
const selectedFile = ref(null);
let loading = ref(null)
const open = ref(false)
const sighting = ref({
  'date': '',
  'time': '',
  'observatory_code': '',
  'device_code': '',
  'device_resolution': '',
  'device_matrix': ''
})

function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files?.length) {
    return;
  }
  selectedFile.value = input.files[0];
  uploadFile();
}

function uploadFile() {
  if (!selectedFile.value) {
    alert('No file selected.');
    return;
  }

  loading.value = true;

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  api.uploadFile(formData)
      .then(data => {
        store.setNotification({
          message: 'File upload successful',
          detail: 'Your file has been uploaded and processed.',
          type: 'success'
        });
      })
      .catch(error => {
        store.setNotification({
          message: 'Something went wrong',
          detail: error,
          type: 'error'
        });
      })
      .finally(() => {
        loading.value = false;
      });
}

const submitForm = async () => {
  try {
    await api.createSighting(sighting.value);
    store.setNotification({
      message: 'Sighting submitted successfully',
      detail: 'Your sighting has been uploaded and processed.',
      type: 'success'
    });

    sighting.value = {};
    open.value = false;
  } catch (error) {
    store.setNotification({
      message: 'Failed to submit sighting',
      detail: error,
      type: 'error'
    });
  }
};


</script>

<template>

  <Card>
    <div class="bg-white">
      <div class="-ml-4 -mt-4 flex flex-wrap items-center justify-between sm:flex-nowrap">
        <div class="ml-4 mt-4">
          <h3 class="text-xl font-semibold leading-6 text-gray-900">Upload sightings file</h3>
          <p class="mt-1 text-sm text-gray-500">Every time you upload a file or a sighting, our algorithm automatically classifies the asteroid and identifies it if it already exists in the database. You can see the results in the <RouterLink to="/asteroids" class="cursor-pointer text-blue-500">asteroids section</RouterLink>.</p>

        </div>
        <div class="ml-4 mt-4 flex-shrink-0">
          <button type="button" @click="open = true"
                  class="relative inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                 stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15"/>
            </svg>
            Add manually
          </button>
        </div>
      </div>
    </div>
    <div class="col-span-full mt-10">
      <div class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
        <div v-if="!loading" class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd"
                  d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z"
                  clip-rule="evenodd"/>
          </svg>
          <div class="mt-4 flex text-sm leading-6 text-gray-600">
            <label for="file-upload"
                   class="relative cursor-pointer rounded-md bg-white font-semibold text-blue-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-blue-600 focus-within:ring-offset-2 hover:text-blue-500">
              <span>Upload a file</span>
              <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="handleFileUpload">
            </label>
          </div>
          <p class="text-xs leading-5 text-gray-600">Only CSV files</p>
        </div>
        <div v-if="loading" class="text-center">
          <Spinner></Spinner>
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
              <form @submit.prevent="submitForm">
                <div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                  <div class="sm:flex sm:items-start">
                    <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">Add sighting
                      </DialogTitle>
                      <div class="max-w-xl mx-auto mt-10">
                        <div class="mb-6">
                          <label for="date" class="block mb-2 text-sm font-medium text-gray-900">Date</label>
                          <input type="date" id="date" v-model="sighting.date"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                        <div class="mb-6">
                          <label for="time" class="block mb-2 text-sm font-medium text-gray-900">Time</label>
                          <input type="time" id="time" v-model="sighting.time"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                        <div class="mb-6">
                          <label for="text" class="block mb-2 text-sm font-medium text-gray-900">Observatory
                            Code</label>
                          <input type="text" id="observatory_code" v-model="sighting.observatory_code"
                                 placeholder="ob_012345"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                        <div class="mb-6">
                          <label for="text" class="block mb-2 text-sm font-medium text-gray-900">Device Code</label>
                          <input type="text" id="device_code" v-model="sighting.device_code" placeholder="de_012345"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                        <div class="mb-6">
                          <label for="text" class="block mb-2 text-sm font-medium text-gray-900">Device
                            Resolution</label>
                          <input type="text" id="device_resolution" v-model="sighting.device_resolution"
                                 placeholder="3x7"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                        <div class="mb-6">
                          <label for="text" class="block mb-2 text-sm font-medium text-gray-900">Device Matrix</label>
                          <input type="text" id="device_matrix" v-model="sighting.device_matrix"
                                 placeholder="00100110010100100"
                                 class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                 required>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                  <button type="submit"
                          class="inline-flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 sm:ml-3 sm:w-auto"
                  >Add
                  </button>
                  <button type="button"
                          class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                          @click="open = false" ref="cancelButtonRef">Cancel
                  </button>
                </div>
              </form>

            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
