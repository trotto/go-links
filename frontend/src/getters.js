import { createSelector } from 'reselect';
import { Map, Set, List, fromJS, OrderedMap } from 'immutable';


const links = state => state.get('links');
const userInfo = state => state.get('userInfo');


export const userLoggedIn = createSelector(
    userInfo,
    (userInfo) => {
      return userInfo && userInfo.get('email');
    }
);


export const linksById = createSelector(
    links,
    (links) => {
      if (links === undefined)
        return undefined;

      return links.reduce(
          (byId, link) => byId.set(link.get('id'), link),
          Map()
      );
    }
);
