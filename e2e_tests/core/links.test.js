const expect = require('expect');

const {
  testInstanceBase,
  testDomains
} = require('../constants');
const {
  getBrowser,
  goToPath,
  signIn,
  createGoLink,
  getPrettyUniqueEmail,
  getPrettyUniqueString,
  TEST_INSTANCE_BASE
} = require('../utils');


let browser;
let context;
let page;


beforeAll(async () => {
  jest.setTimeout(60 * 1000);

  browser = await getBrowser();
});


afterAll(async () => {
  await browser.close();
});


beforeEach(async () => {
  context = await browser.newContext()
  context.setDefaultTimeout(60 * 1000);

  page = await context.newPage();
});


afterEach(async () => {
  await page.close();
});


describe('links', () => {
  const testDestination = 'https://www.trot.to/?q=' + getPrettyUniqueString();

  test('an unauthenticated user should be sent to signin when requesting a go link', async () => {
    const response = await goToPath(page, '/links');

    const pageUrl = await page.url();

    // this behavior varies depending on the number of auth methods configured
    expect(pageUrl.startsWith('https://accounts.google.com') || pageUrl.startsWith(`${TEST_INSTANCE_BASE}/_/auth/login`))
        .toBe(true);
    expect(response.status()).toEqual(200);
  });

  test('a user should be able to follow a go link created before this test run', async () => {
    await signIn(page, getPrettyUniqueEmail(testDomains.primary));

    const linksResponse = await goToPath(page, '/_/api/links');

    const simpleLinks = (await linksResponse.json()).filter((link) => !link.shortpath.includes('%s'));

    if (simpleLinks.length > 0) {
      const link = simpleLinks[0];

      await goToPath(page, `/${link.shortpath}`);

      expect(await page.url()).toEqual(link.destination_url);
    }
  });

  test('a user should be able to create and follow a go link', async () => {
    const shortlink = getPrettyUniqueString();

    const userEmail = getPrettyUniqueEmail(testDomains.primary);

    await createGoLink(page, userEmail, shortlink, testDestination);

    await goToPath(page, `/${shortlink}`);

    expect(await page.url()).toEqual(testDestination);
  });

  test('a user should be able to follow a go link created by another user in the same org', async () => {
    const shortlink = getPrettyUniqueString();

    await createGoLink(page, getPrettyUniqueEmail(testDomains.primary), shortlink, testDestination);

    const userEmail = getPrettyUniqueEmail(testDomains.primary);

    await signIn(page, userEmail);

    await goToPath(page, `/${shortlink}`);

    expect(await page.url()).toEqual(testDestination);
  });

  test('a user should be able to fetch a list of go links in their organization', async () => {
    const shortlink = getPrettyUniqueString();

    await createGoLink(page, getPrettyUniqueEmail(testDomains.primary), shortlink, testDestination);

    await signIn(page, getPrettyUniqueEmail(testDomains.primary));

    const linksResponse = await goToPath(page, '/_/api/links');

    expect((await linksResponse.json()).map((link) => link.shortpath))
        .toEqual(expect.arrayContaining([shortlink]));
  });

  test('a user should not be able to access go links from another organization', async () => {
    const shortlink = getPrettyUniqueString();

    await createGoLink(page, getPrettyUniqueEmail(testDomains.primary), shortlink, testDestination);

    const userEmail = getPrettyUniqueEmail(testDomains.secondary);

    await signIn(page, userEmail);

    await goToPath(page, `/${shortlink}`);

    // TODO: Eliminate special handling for local environment.
    const expectedPrefix = testInstanceBase === 'http://localhost:9095' ? 'http://localhost:5007': testInstanceBase;
    expect((await page.url()).startsWith(expectedPrefix)).toBe(true);

    const linksResponse = await goToPath(page, '/_/api/links');

    expect((await linksResponse.json()).map((link) => link.shortpath))
        .toEqual(expect.not.arrayContaining([shortlink]));
  });
});
