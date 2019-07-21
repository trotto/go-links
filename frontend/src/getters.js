import { createSelector } from 'reselect';
import { Map, Set, List, fromJS, OrderedMap } from 'immutable';


var userInfo = state => state.get('userInfo');
var linkCreatedOnThisPageload = state => state.get('linkCreatedOnThisPageload');


export const userLoggedIn = createSelector(
    userInfo,
    (userInfo) => {
      return userInfo && userInfo.get('email');
    }
);
