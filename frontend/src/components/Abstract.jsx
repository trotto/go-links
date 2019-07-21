import React from 'react';
import { browserHistory } from 'react-router';
import {fromJS} from 'immutable';


export class ReduxManagedStateComponent extends React.Component {

  componentWillUnmount() {
    this.clearState();
  }

  getState(key) {
    const state = this.props.getComponentState(this.state.componentId) || fromJS(this.state.defaults);

    return key ? state.get(key) : state;
  }

  updateState(updates) {
    this.props.updateComponentState(this.state.componentId, this.getState().mergeDeep(updates));
  }

  clearState(updates) {
    this.props.updateComponentState(this.state.componentId, undefined);
  }
}
