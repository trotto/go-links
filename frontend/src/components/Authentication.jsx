import React from 'react';
import {connect} from 'react-redux';
import {Map, List, Set, fromJS} from 'immutable';


function mapStateToProps(state) {

  state = state.core;

  return {
    modalInputs: state.get('modalInputs')
  };
}


export class GoogleLoginButton extends React.Component {

  render() {
    return <a href={this.props.loginURL} style={this.props.style || {}}>
             <img height="60" src="/_images/auth/google_signin_button.png" />
            </a>
  }
}
