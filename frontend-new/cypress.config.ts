import { defineConfig } from 'cypress'

module.exports = defineConfig({
  viewportWidth: 1440,
  viewportHeight: 900,
  // TODO: Enable video when issues with Cypress hanging is fixed
  video: false,
  retries: {
    runMode: 2,
    openMode: 0,
  },
  blockHosts: ['*.sentry.io'],
  e2e: {
    baseUrl: 'http://localhost:3000',
  },
})
