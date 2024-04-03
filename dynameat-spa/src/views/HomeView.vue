<script setup>
import Card from "../components/Card.vue";
import {
  AcademicCapIcon,
  BanknotesIcon,
  CheckBadgeIcon,
  ClockIcon,
  ReceiptRefundIcon,
  UsersIcon,
} from '@heroicons/vue/24/outline'

const actions = [
  {
    title: 'Request time off',
    href: '#',
    icon: ClockIcon,
    iconForeground: 'text-teal-700',
    iconBackground: 'bg-teal-50',
  },
  {
    title: 'Benefits',
    href: '#',
    icon: CheckBadgeIcon,
    iconForeground: 'text-purple-700',
    iconBackground: 'bg-purple-50',
  },
  {
    title: 'Schedule a one-on-one',
    href: '#',
    icon: UsersIcon,
    iconForeground: 'text-sky-700',
    iconBackground: 'bg-sky-50',
  },
  {
    title: 'Payroll',
    href: '#',
    icon: BanknotesIcon,
    iconForeground: 'text-yellow-700',
    iconBackground: 'bg-yellow-50',
  },
  {
    title: 'Submit an expense',
    href: '#',
    icon: ReceiptRefundIcon,
    iconForeground: 'text-rose-700',
    iconBackground: 'bg-rose-50',
  },
  {
    title: 'Training',
    href: '#',
    icon: AcademicCapIcon,
    iconForeground: 'text-indigo-700',
    iconBackground: 'bg-indigo-50',
  },
]
</script>

<template>
  <Card>
    <div class="p-6">
      <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-4xl">Welcome to Asteroid Scan</h1>
      <p class="mt-6 text-lg leading-8 text-gray-600"> Explore the vastness of space and discover the wonders of
        asteroids from the comfort of your screen. Asteroid Scan offers you a unique window into the cosmos, enabling
        you to identify, analyze, and track asteroids. With our state-of-the-art scanning technology and comprehensive
        database, you’re just a click away from uncovering the secrets of these fascinating celestial bodies. Have
        fun!</p>
    </div>
  </Card>
</template>
