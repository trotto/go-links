import { List, Map } from 'immutable';
import { browserHistory } from 'react-router';

const { detect } = require('detect-browser');
const browser = detect();


export function getServiceBaseUrl() {
  // TODO: Make this function actually service-sensitive again.

  if (window.location.host.indexOf('localhost') === 0) {
    return 'http://localhost:9095';
  }

  return 'https://' + window.location.host;  // for both prod and dev.trot.to
}


export function doesBrowserSupportExtension() {
  return browser.name === 'chrome' && !browser.mobile;
}


export const isTrottoHosted = () => location.hostname.slice(location.hostname.length - 7) === 'trot.to';
