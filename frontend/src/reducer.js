import { Map, List, Set, fromJS } from 'immutable';

function setState(state, newState) {
  state = state.merge(newState);

  return state;
}

export default function (state = Map(), action) {
  switch (action.type) {

    case 'SET_STATE':
      return setState(state, action.state);

    case 'UPDATE_NEW_LINK_FIELD':
      return state.setIn(['newLinkData', action.fieldName], action.fieldValue);

    case 'CLEAR_NEW_LINK_DATA':
      return state.update('newLinkData', newLinkData => newLinkData.map(val => ''));

    case 'SET_LINK_CREATION_MESSAGE':
      return state.set(
          'linkCreationMessage',
          fromJS({
            type: action.messageType,
            html: action.html,
            tootsLink: action.tootsLink
          })
      );

    case 'SET_TERMS_OF_SERVICE_ACCEPTANCE_STATUS':
      return state.set('termsOfServiceAcceptanceStatus', action.termsOfServiceAcceptanceStatus);

    case 'RECEIVE_LINKS':
      return state.update('links', lst => {
        if (!lst) {
          return fromJS(action.links);
        }

        return fromJS(action.links).reduce((lst, receivedLink) => {
          const linkIndex = lst.findIndex(otherLink => otherLink.get('shortpath') === receivedLink.get('shortpath'));

          if (linkIndex !== -1) {
            return lst.set(linkIndex, receivedLink);
          }

          return lst.push(receivedLink);
        }, lst);
      });

    case 'SET_SHOWN_SUBSECTION':
      return state.set('shownSubsection', action.subsection);

    case 'SET_ERROR_BAR_ERROR_MESSAGE':
      return state.set('errorBarMessage', action.errorMessage);

    case 'SET_DEFAULT_LINK_SEARCH_TERM':
      return state.set('defaultLinkSearchTerm', action.defaultLinkSearchTerm);

    case 'RECEIVE_USER_INFO':
      return state.set('userInfo', fromJS(action.userInfo));

    case 'UPDATE_USER_INFO':
      return state.mergeIn(['userInfo'], action.userInfo);

    case 'SET_DRAFT_DESTINATION':
      return state.setIn(['editing', 'draftDestination'], action.draftDestination);

    case 'UPDATE_LOCAL_LINK':
      const linkIndex = state.get('links', List()).findIndex(link => link.get('id') === action.linkId);

      if (linkIndex == -1) {
        return state.update('links', links => links.push(fromJS(action.linkData)));
      }

      return state.updateIn(['links', linkIndex], link => link.merge(action.linkData));

    case 'DELETE_LINK':
      return state.update('links', links => links.filter(link => link.get('id') !== action.linkId));

    case 'LINK_CREATED_ON_THIS_PAGELOAD':
      return state.set('linkCreatedOnThisPageload', fromJS(action.linkData));

    case 'SET_LINK_EDITING_STATUS':
      return state.set('linkEditingStatus', fromJS(action.state || {}));

    case 'UPDATE_OPEN_MODAL':
      return state.merge({'modalShown': action.modalId, 'modalInputs': action.modalInputs});

    case 'UPDATE_COMPONENT_STATE':
      // TODO: Look more deeply into existing solutions for this. The implementations mentioned in
      //       https://redux.js.org/docs/faq/OrganizingState.html seem to be poorly maintained.
      return state.setIn(['_components', action.componentId], action.newState);

  }

  return state;
}
