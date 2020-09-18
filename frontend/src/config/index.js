import {fromJS, List} from 'immutable';

const CUSTOM_CONFIG = window._trotto.layout;

const DEFAULT_CONFIG = {
  palette: {
    primary: '#f27e8f',
    secondary: '#7e8ff2',
    success: '#4f8a10',
    error: '#ff0033'
  },
  page: {
    title: 'Trotto Go Links',
    favicon: '/favicon.ico'
  },
  header: {
    title: 'Trotto',
    logo: {
      url: '/_images/snout.png',
      css: {
        height: '1.6em'
      }
    },
    links: [
      'directory',
      'howItWorks'
    ]
  },
  footer: {
    showSourceLink: true,
    links: []
  }
};

const DEFAULT_NAV_ITEMS = {
  directory: {
    text: 'Directory',
    url: '#/directory'
  },
  howItWorks: {
    text: 'How It Works',
    url: 'https://www.trot.to/how-it-works',
    openInNewTab: true
  }
};

let config = fromJS(DEFAULT_CONFIG).mergeDeep(fromJS(CUSTOM_CONFIG));
config = config.updateIn(['header', 'links'], (links) => links.reduce((fullLinks, link) => {
  if (typeof link === 'string') {
    if (!DEFAULT_NAV_ITEMS[link]) {
      console.error('Skipping invalid link ID: ', link);

      return fullLinks;
    }
    return fullLinks.push(fromJS(Object.assign({id: link}, DEFAULT_NAV_ITEMS[link])));
  }

  return fullLinks.push(link);
}, List()));

export const getConfig = (keyPath) => config.getIn(keyPath.split('.'))

const setTitleAndFavicon = () => {
  const favicon = document.createElement('link');
  favicon.rel = 'shortcut icon';
  favicon.href = getConfig('page.favicon');
  document.getElementsByTagName('head')[0].appendChild(favicon);

  document.title = getConfig('page.title');
};

setTitleAndFavicon();
