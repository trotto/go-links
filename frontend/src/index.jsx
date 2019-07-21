import React from 'react';
import { render } from 'react-dom'
import {Provider} from 'react-redux';
import { Router, Route, Redirect, IndexRoute, hashHistory } from 'react-router';
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'
import {createStore, applyMiddleware, combineReducers} from 'redux';
import reducer from './reducer';
import {App} from './components/App';
import {MainLayoutContainer} from './components/Layout';
import {LinksTableContainer} from './components/LinkList';
import {receiveSaveResult, updateNewLinkFieldWithString,
        setLinkCreationMessage, fetchUserInfo, receiveUserInfo} from './actions';
import {INIT_STATE} from './init_state';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';
import {Map, List, Set, fromJS} from 'immutable';

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

// handle responses for requests processed right after login
if (location.search.indexOf('r=') !== -1) {
  var b64Encoded = location.search.split('r=', 2)[1].replace(/_/g, '/').replace(/-/g, '+');  // was URL-safe encoded
  store.dispatch(receiveSaveResult(JSON.parse(atob(b64Encoded))));
  history.replaceState({}, '', '/');
} else if (location.search.indexOf('sp=') !== -1) {
  // TODO: Group all this into an action.
  var queryParams = qs.parse(location.search.slice(1));

  const shortpath = queryParams.sp;

  store.dispatch(updateNewLinkFieldWithString('shortpath', shortpath));

  history.replaceState({}, '', '/');

  store.dispatch(setLinkCreationMessage('error', '"go/' + shortpath + '" doesn\'t exist yet. You can create it now!'));
}


if (document.cookie.indexOf('session=') !== -1) {
  store.dispatch(fetchUserInfo());
} else {
  store.dispatch(receiveUserInfo(null));
}

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
    <Provider store={store}>
      <Router history={hashHistory}>
        <Route component={App}>
          <Route component={MainLayoutContainer}>
            <Route path="/" component={null} />
            <Route path="/create" component={null} />
            <Route path="/directory" component={LinksTableContainer} />
          </Route>
        </Route>
      </Router>
    </Provider>
), document.getElementById('app'));
