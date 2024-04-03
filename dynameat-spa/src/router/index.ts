import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/HomeView.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/upload',
        component: () => import('../views/FileUploadView.vue')
    },
    {
        path: '/asteroids',
        name: 'asteroid-list',
        component: () => import('../views/AsteroidListView.vue')
    },
    {
        path: '/asteroids/:id',
        name: 'asteroid-detail',
        component: () => import('../views/AsteroidDetailView.vue')
    },
    {
        path: '/asteroids/search',
        component: () => import('../views/AsteroidSearchView.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
