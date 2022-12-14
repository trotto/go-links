import React from 'react';
import { render } from 'react-dom'
import {Provider} from 'react-redux';
import {createStore, applyMiddleware, combineReducers} from 'redux';
import reducer from './reducer';
import TrottoRouter from './router';
import {receiveSaveResult, updateNewLinkFieldWithString,
        setLinkCreationMessage, fetchUserInfo, setLinkEditingStatus, fetchSuggestedLinks} from './actions';
import {INIT_STATE} from './init_state';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';
import { DEFAULT_NAMESPACE } from './config';
import { TrottoThemeProvider } from "./config/theme";

var qs = require('qs');


let middleware = [thunkMiddleware];
if (process.env.NODE_ENV !== 'production') {
  const loggerMiddleware = createLogger();
  middleware.push(loggerMiddleware);
}


const store = createStore(
    combineReducers({
      core: reducer
    }),
    applyMiddleware(...middleware)
);

store.dispatch({
  type: 'SET_STATE',
  state: INIT_STATE
});

const queryParams = qs.parse(location.search.slice(1));

// handle responses for requests processed right after login
if (queryParams.r) {
  var b64Encoded = location.search.split('r=', 2)[1].replace(/_/g, '/').replace(/-/g, '+');  // was URL-safe encoded
  store.dispatch(receiveSaveResult(JSON.parse(atob(b64Encoded))));
  history.replaceState({}, '', '/');
} else if (queryParams.sp) {
  // TODO: Group all this into an action.
  const shortpath = queryParams.sp;
  const namespace = queryParams.ns || DEFAULT_NAMESPACE;

  store.dispatch(updateNewLinkFieldWithString('namespace', namespace));
  store.dispatch(updateNewLinkFieldWithString('shortpath', shortpath));

  history.replaceState({}, '', '/');

  store.dispatch(setLinkCreationMessage('error', `${namespace}/${shortpath} doesn't exist yet. You can create it now!`));
  store.dispatch(fetchSuggestedLinks(shortpath));
} else if (queryParams.transfer) {
  history.replaceState({}, '', '/');

  store.dispatch(setLinkEditingStatus({completeTransfer: queryParams.transfer}));
}


store.dispatch(fetchUserInfo());

// necessary because fragment is already used for nav... very hacky.
(function() {
  var { search } = window.location;
  search = search.replace('?', '');
  if (search.indexOf('section=') === 0) {
    // Push onto callback queue so it runs after the DOM is updated,
    // this is required when navigating from a different page so that
    // the element is rendered on the page before trying to getElementById.
    setTimeout(() => {
      const id = search.replace('section=', '');
      const element = document.getElementById(id);
      if (element) {
        element.click();
        element.scrollIntoView();
      }
    }, 0);
  }
})();


render((
    <TrottoThemeProvider>
      <Provider store={store}>
        <TrottoRouter/>
      </Provider>
    </TrottoThemeProvider>
), document.getElementById('app'));
