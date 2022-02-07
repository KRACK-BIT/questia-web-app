import { defineNuxtConfig } from '@nuxt/bridge'

export default defineNuxtConfig({
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Questia',
  },

  // @ts-ignore-next-line
  loading: false,

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/buefy
    'nuxt-buefy',
    ['@nuxtjs/proxy', ['http://localhost:5000/api']],
    // https://go.nuxtjs.dev/axios
    [
      '@nuxtjs/axios',
      {
        baseURL: 'http://localhost:5000/',
      },
    ],
    // https://go.nuxtjs.dev/pwa
    [
      '@nuxtjs/pwa',
      {
        manifest: {
          lang: 'en',
        },
      },
    ],
  ],

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  bridge: {
    vite: true,
  },
})
