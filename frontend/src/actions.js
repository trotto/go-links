import { Map, List, fromJS } from 'immutable';
import { browserHistory } from 'react-router';
import fetch from 'isomorphic-fetch'
import {getServiceBaseUrl} from './utils';


const enhancedFetch = function(endpoint, fetchInit, dispatch) {

  if ((fetchInit.method || 'GET') !== 'GET') {
    fetchInit.headers = fetchInit.headers || {};
    fetchInit.headers['X-CSRFToken'] = window._trotto.csrfToken;
  }

  return fetch(endpoint, fetchInit)
      // TODO: handle 4xx and 5xx errors.
      .then((response) => response.text())
      .then((text) => !text ? {} : JSON.parse(text))
      .then(json => {
        if (json.error && json.error_type === 'error_bar') {
          dispatch(setErrorBarMessage(json.error));
          return Promise.reject(new Error(json.error));
        }

        dispatch(setErrorBarMessage(null));

        return json;
      })
};


export function setErrorBarMessage(errorMessage) {
  return {
    'type': 'SET_ERROR_BAR_ERROR_MESSAGE',
    errorMessage
  }
}


export function updateNewLinkField(fieldName, elem) {
  var fieldValue = elem.target.value.trim().replace(' ', '');
  if (fieldName == 'shortpath') {
    fieldValue = fieldValue.replace(/[^0-9a-zA-Z\-\/%]/g, '').toLowerCase();
    while (fieldValue[0] === '/') {
      fieldValue = fieldValue.slice(1)
    }
  }

  return {
    type: 'UPDATE_NEW_LINK_FIELD',
    fieldName,
    fieldValue
  }
}


export function updateNewLinkFieldWithString(fieldName, string) {
  return updateNewLinkField(fieldName, {target: {value: string}})
}


export function clearNewLinkData() {

  return {
    type: 'CLEAR_NEW_LINK_DATA'
  }
}


export function setLinkCreationMessage(messageType, html, tootsLink) {

  return function (dispatch, getState) {
    html = !getState().core.get('goSupportedInCurrentSession')
        ? html
        : html.replace('https://trot.to/', 'http://go/').replace('trot.to/', 'go/');

    dispatch({
      type: 'SET_LINK_CREATION_MESSAGE',
      messageType,
      html,
      tootsLink
    });
  };
}


export function updateLocalLink(linkId, linkData) {

  if (linkData.destination) {
    linkData.destination_url = linkData.destination;
    delete linkData.destination;
  }

  return {
    type: 'UPDATE_LOCAL_LINK',
    linkId,
    linkData
  }
}


export function setLinkCreatedOnThisPageload(linkData) {
  return {
    type: 'LINK_CREATED_ON_THIS_PAGELOAD',
    linkData
  }
}


export function receiveSaveResult(responseJson) {
  // could be:
  //   1) redirect
  //   2) error
  //   3) success
  return function (dispatch, getState) {

    if (responseJson.redirect_to) {
      window.location = responseJson.redirect_to;
    } else if (responseJson.error) {
      dispatch(setLinkCreationMessage('error', responseJson.error));
    } else {
      dispatch(receiveLinks([responseJson]));

      // surface any modifications made to the destination server-side to the user
      dispatch(updateNewLinkField('destination', {target: {value: responseJson.destination_url}}));

      dispatch(setLinkCreatedOnThisPageload(responseJson));

      var host = 'http://go';

      if (!getState().core.get('goSupportedInCurrentSession')) {
        host = host.replace('http://go', getServiceBaseUrl());
      }

      dispatch(setLinkCreationMessage(
          'good_news',
          'Success! New go link created:',
          host + '/' + responseJson.shortpath
      ));
    }
  }
}


export function saveLink() {

  return function (dispatch, getState) {
    const currentState = getState().core;

    var endpoint = '/_/api/links';

    var fetchInit = {
      credentials: 'include',
      method: 'POST',
      body: JSON.stringify(currentState.get('newLinkData').toJS()),
      headers: {'Content-Type': 'application/json'}
    };

    return enhancedFetch(endpoint, fetchInit, dispatch)
      .then(json => {
        dispatch(receiveSaveResult(json));
      })
      .catch(reason => {})
  }
}


export function updateLink(linkId, updates) {

  return function (dispatch, getState) {
    var endpoint = '/_/api/links/' + linkId;

    var fetchInit = {
      credentials: 'include',
      method: 'PUT',  // really we're using patch-type behavior here...
      body: JSON.stringify(updates),
      headers: {'Content-Type': 'application/json'}
    };

    const currentMatchingLink = getState().core.get('links', List()).find(link => link.get('id') === linkId);

    dispatch(updateLocalLink(linkId, updates));

    return enhancedFetch(endpoint, fetchInit, dispatch)
        .catch(reason => dispatch(updateLocalLink(linkId, currentMatchingLink)))
  }
}


export function deleteLink(linkId) {

  return function (dispatch, getState) {
    var endpoint = '/_/api/links/' + linkId;

    var fetchInit = {
      credentials: 'include',
      method: 'DELETE',
      headers: {}
    };

    dispatch({
      type: 'DELETE_LINK',
      linkId: linkId
    });

    enhancedFetch(endpoint, fetchInit, dispatch);
  }
}


export function takeOwnershipOfLink(transferToken) {

  return function (dispatch) {
    const endpoint = `/_/api/transfer_link/${transferToken}`;

    const fetchInit = {
      credentials: 'include',
      method: 'POST'
    };

    return enhancedFetch(endpoint, fetchInit, dispatch)
      .then(() => {
        dispatch(fetchLinks());
      })
      .catch(reason => {});
  }
}


export function receiveLinks(links) {
  return {
    type: 'RECEIVE_LINKS',
    links
  }
}


export function fetchLinks() {

  return function (dispatch, getState) {
    var endpoint = '/_/api/links';

    var fetchInit = {
      credentials: 'include',
      method: 'GET'
    };

    return enhancedFetch(endpoint, fetchInit, dispatch)
      .then(json => {
        dispatch(receiveLinks(json));
      })
      .catch(reason => {})
  }
}


export function toggleTermsOfServiceAcceptance() {

  return function (dispatch, getState) {
    dispatch({
      type: 'SET_TERMS_OF_SERVICE_ACCEPTANCE_STATUS',
      termsOfServiceAcceptanceStatus: getState().core.get('termsOfServiceAcceptanceStatus') === 'not_accepted'
          ? 'accepted' : 'not_accepted'
    });
  };
};


export function receiveUserInfo(userInfo) {

  return function (dispatch, getState) {

    userInfo = !userInfo || !userInfo.email ? null : userInfo;

    dispatch({
      type: 'RECEIVE_USER_INFO',
      userInfo
    });

    if (userInfo) {
      dispatch(fetchLinks());
    }
  }
}


export function updateUserInfo(userInfo) {

  return {
    type: 'UPDATE_USER_INFO',
    userInfo
  }
}


export function fetchUserInfo() {

  return function (dispatch, getState) {
    var endpoint = '/_/api/users/me';

    var fetchInit = {
      credentials: 'include',
      method: 'GET'
    };

    return enhancedFetch(endpoint, fetchInit, dispatch)
      .then(json => {

        if (json.redirect_to) {
          dispatch(receiveUserInfo(null));
        } else {
          dispatch(receiveUserInfo(json));
        }
      })
      .catch(reason => {
        dispatch(receiveUserInfo(null));
      });
  }
}


export function updateUser(userData) {

  return function (dispatch, getState) {
    var endpoint = '/_/api/users/me';

    var fetchInit = {
      credentials: 'include',
      method: 'PUT',
      body: JSON.stringify(userData),
      headers: {'Content-Type': 'application/json'}
    };

    enhancedFetch(endpoint, fetchInit, dispatch)
      .then(json => dispatch(receiveUserInfo(json)))
      .catch(reason => {});

    dispatch(updateUserInfo(userData));
  }
}


export function dismissNotification(notificationId) {

  return function (dispatch, getState) {
    var payload = {notifications: {}};
    payload.notifications[notificationId] = 'dismissed';

    dispatch(updateUser(payload));
  }
}


export function setDraftDestination(draftDestination) {

  if (draftDestination) {
    draftDestination = draftDestination.trim();
  }

  return {
    type: 'SET_DRAFT_DESTINATION',
    draftDestination
  }
}


export const setLinkEditingStatus = (state) => ({
  type: 'SET_LINK_EDITING_STATUS',
  state
});


export function updateComponentState(componentId, newState) {

  return function(dispatch, getState) {
    dispatch({
      type: 'UPDATE_COMPONENT_STATE',
      componentId,
      newState
    });
  };
}
