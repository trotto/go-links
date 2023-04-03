export const navigationLinks = {
  ROOT: '/',
  PRICING: 'https://www.trot.to/pricing',
  PRIVACY: 'https://www.trot.to/privacy',
  TERMS: 'https://www.trot.to/terms',
  CONTACT: 'https://www.trot.to/contact',
  SHARE_FEEDBACK: (email: string) => `https://7kgyyjm8iyj.typeform.com/to/CIwBEGSN#email=${email}`,
  GITHUB: 'https://github.com/trotto/go-links',
  DOCUMENTATION: 'https://www.trot.to/docs/use/creating-a-go-link',
  LOGIN_GOOGLE: '/_/auth/login/google?redirect_to=https%3A%2F%2Ftrot.to',
  LOGIN_MICROSOFT: 'https://id.trot.to/sso/o365?redirect_to=https%3A%2F%2Ftrot.to',
  LOGOUT: '/_/auth/logout',
  EXTENSION:
    'https://chrome.google.com/webstore/detail/trotto-go-links/nkeoojidblilnkcbbmfhaeebndapehjk',
}
