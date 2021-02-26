const fs = require('fs');

const { chromium } = require('playwright');
const jwt = require('jsonwebtoken');
const yaml = require('yaml');

const {
  TEST_MODE,
  TEST_INSTANCE_BASE
} = process.env;


const getBrowser = async () => await chromium.launch(TEST_MODE !== 'debug' ? {} : {
  headless: false,
  slowMo: 500
});


const goToPath = async (page, path) => await page.goto(`${TEST_INSTANCE_BASE}${path}`);


const signIn = async (page, userEmail) => {
  const {
    testing: {
      secret: testTokenSecret
    }
  } = yaml.parse(fs.readFileSync('../server/src/config/app.yml', 'utf8'));

  const testToken = jwt.sign({
    user_email: userEmail,
    exp: Math.floor(Date.now() / 1000) + 60
  }, testTokenSecret, { algorithm: 'HS256' });

  await goToPath(page, `/_/auth/oauth2_callback?test_token=${testToken}`);
};


const createGoLink = async (page, userEmail, shortlink, destination) => {
  await signIn(page, userEmail);

  await page.fill('input[data-test-id="shortlink-shortpath-input"]', shortlink);

  await page.fill('input[data-test-id="shortlink-destination-input"]', destination);

  await page.click('button[data-test-id="shortlink-submit-button"]');

  await page.waitForSelector('[data-test-id="new-shortlink-anchor-tag"]');
};


const getPrettyUniqueString = () => `${Math.random().toString().slice(2)}-${Date.now()}`;


const getPrettyUniqueEmail = (domain) => `${getPrettyUniqueString()}@${domain}`;


module.exports = {
  getBrowser,
  goToPath,
  signIn,
  createGoLink,
  getPrettyUniqueString,
  getPrettyUniqueEmail,
  TEST_INSTANCE_BASE
};
