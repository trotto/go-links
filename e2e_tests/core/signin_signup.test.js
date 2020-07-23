const expect = require('expect');

const {
  testDomains
} = require('../constants');
const {
  getBrowser,
  goToPath,
  signIn,
  getPrettyUniqueEmail
} = require('../utils');


let browser;
let page;


beforeAll(async () => {
  jest.setTimeout(30 * 1000);

  browser = await getBrowser();
});


afterAll(async () => {
  await browser.close();
});


beforeEach(async () => {
  context = await browser.newContext()
  context.setDefaultTimeout(30 * 1000);

  page = await context.newPage();
});


afterEach(async () => {
  await page.close();
});


describe('signin', () => {
  let userEmail;

  test('Google OAuth handler should redirect to Google', async () => {
    const response = await goToPath(page, '/_/auth/login/google');

    expect((await page.url()).startsWith('https://accounts.google.com')).toBe(true);
    expect(response.status()).toEqual(200);
  });

  test('New users should be able to sign in and view their info', async () => {
    userEmail = getPrettyUniqueEmail(testDomains.primary);

    await signIn(page, userEmail);

    const userInfoResponse = await goToPath(page, '/_/api/users/me');

    expect((await userInfoResponse.json()).email).toEqual(userEmail);
  });

  test('Existing users should be able to sign in and view their info', async () => {
    userEmail = getPrettyUniqueEmail(testDomains.primary);

    await signIn(page, userEmail);

    context.clearCookies();

    await signIn(page, userEmail);

    const userInfoResponse = await goToPath(page, '/_/api/users/me');

    expect((await userInfoResponse.json()).email).toEqual(userEmail);
  });
});
