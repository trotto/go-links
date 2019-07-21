import {List} from 'immutable';

const { detect } = require('detect-browser');
const browser = detect();


var crxInstalledTag = document.getElementsByName('trotto:crxInstalled');
const extensionIsInstalled = crxInstalledTag.length > 0 && crxInstalledTag[0].content === 'true';
if (window.location.search.indexOf('autoclose=true') !== -1) {
  window.close();
}


export const INIT_STATE = {
  userInfo: undefined,
  newLinkData: {
    shortpath: '',
    destination: ''
  },
  termsOfServiceAcceptanceStatus: (window._trotto && window._trotto.alreadyAcceptedTerms === 'true') ? 'previously_accepted' : 'not_accepted',
  chromeExtensionInstalled: extensionIsInstalled,
  linkCreatedOnThisPageload: undefined,
  goSupportedInCurrentSession: extensionIsInstalled,
  modalShown: undefined,
  browserName: browser.name,
  '_components': {}
};


export const copyInitState = () => jQuery.extend(true, {}, INIT_STATE);
