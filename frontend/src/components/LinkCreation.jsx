import React from 'react';
import {connect} from 'react-redux';
import {CopyToClipboard} from 'react-copy-to-clipboard';
import * as actions from '../actions';
import * as getters from '../getters';
import { browserHistory } from 'react-router';
import {Map, List, Set, fromJS} from 'immutable';
import {getServiceBaseUrl} from '../utils';
import {ReduxManagedStateComponent} from './Abstract'


function mapStateToProps(state) {

  state = state.core;

  return {
    newLinkData: state.get('newLinkData'),
    linkCreationMessage: state.get('linkCreationMessage'),
    termsOfServiceAcceptanceStatus: state.get('termsOfServiceAcceptanceStatus'),
    links: state.get('links'),
    chromeExtensionInstalled: state.get('chromeExtensionInstalled'),
    linkCreatedOnThisPageload: state.get('linkCreatedOnThisPageload'),
    goSupportedInCurrentSession: state.get('goSupportedInCurrentSession'),
    userLoggedIn: getters.userLoggedIn(state),
    userInfo: state.get('userInfo')
  };
}




export class NewUserIntro extends ReduxManagedStateComponent {

  constructor(props) {
    super(props);

    this.state = {
      componentId: 'newUserIntro',
      defaults: {}
    };
  }

  render() {
    return (
        <div className="container" style={{marginTop: '-40px'}}>
          <div className="row">
            <div className="col-md-10 col-md-offset-1 text-center">
              <h3><b>Welcome back!</b></h3>
            </div>
          </div>
          <div className="row" style={{marginTop: '30px', marginBottom: '80px'}}>
            <div
                className="col-md-6 col-md-offset-3"
                style={{}}
            >
              Getting to any resource you need to access&mdash;docs, dashboards, reports, and more&mdash;is just
              as simple. Create your own go link now:
            </div>
          </div>
        </div>
    )
  }
}


export const NewUserIntroContainer = connect(
    mapStateToProps,
    actions
)(NewUserIntro);


export const LinkForm = React.createClass({

  getInitialState: function () {
     return {
       value: '',
       copied: false,
     }
   },

  componentDidMount: function() {
    if (this.props.newLinkData && this.props.newLinkData.get('shortpath')) {  // shortpath already provided by redirect
      this.destinationInput.focus();
    } else {
      this.shortlinkInput.focus();
    }
  },

  save() {
    this.props.saveLink();
  },

  _handleKeyPress: function(e) {
    if (e.key === 'Enter') {
      document.getElementById('link-submit-button').click();
    }
  },

  _setCopied: function() {
    const setState = this.setState.bind(this);

    this.setState({copied: true});

    setTimeout(function() {
      setState({copied: false});
    }, 1000);
  },

  render: function() {

    if (!this.props.linkCreationMessage) {
      var messageText = '';
    } else {
      var messageText = this.props.linkCreationMessage.get('html');
    }

    var messageColor = '#4F8A10';
    if (this.props.linkCreationMessage && this.props.linkCreationMessage.get('type') === 'error') {
      messageColor = '#ff0033';
    }

    return (
        <div className="container" id="link-form">
          {'/create' !== this.props.location.pathname ? null : <NewUserIntroContainer />}
          <div className="row">
            <div className="col-md-3 col-md-offset-2">
              <div style={{width: '100%', display: 'flex', alignItems: 'center'}}>
                 <div style={{paddingRight: '5px'}}>
                   <div>
                     go/
                   </div>
                 </div>
                 <input
                     className="form-control"
                     ref={(input) => { this.shortlinkInput = input; }}
                     style={{width: '0px', flexGrow: '1'}}
                     type="text" id="shortpath" placeholder="keyword"
                     data-test-id="shortlink-shortpath-input"
                     value={this.props.newLinkData.get('shortpath')}
                     onChange={this.props.updateNewLinkField.bind(this, 'shortpath')}
                     onKeyPress={this._handleKeyPress}
                 />
              </div>
            </div>
            <div className="col-md-1 text-center" style={{height: '34px', lineHeight: '34px'}}>
                <b>&#8594;</b>
            </div>
            <div className="col-md-4">
                <div style={{width: '100%', display: 'flex'}}>
                  <input
                     className="form-control"
                     ref={(input) => { this.destinationInput = input; }}
                     style={{width: '0px', flexGrow: '1'}}
                     type="text" id="destination" placeholder="Paste the link to a resource here"
                     data-test-id="shortlink-destination-input"
                     value={this.props.newLinkData.get('destination')}
                     onChange={this.props.updateNewLinkField.bind(this, 'destination')}
                     onKeyPress={this._handleKeyPress}
                 />
                </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-8 col-md-offset-2"
                 style={{marginTop: '10px', display: 'flex', flexDirection: 'column', alignItems: 'flex-start'}}>
              <div style={{width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-evenly'}}>
                <div style={{display: 'flex', alignItems: 'baseline', flexWrap: 'wrap', flexGrow: '1'}}>
                  <div className="text-center" style={{fontSize: '0.9em', color: messageColor}}>
                    {messageText}
                  </div>
                  <div>
                    <a href={!this.props.linkCreationMessage ? '' : this.props.linkCreationMessage.get('tootsLink')}
                       data-test-id="new-shortlink-anchor-tag"
                       target="_blank"
                       style={{display: !this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink') ? 'none' : 'block',marginLeft:'5px',marginRight:'5px',color:'#f27e8f',fontWeight:'bold'}}
                    >
                    {!this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink')
                        ? '' : this.props.linkCreationMessage.get('tootsLink').split('://')[1]}
                    </a>
                  </div>
                  {!this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink') ? null :
                    <div style={{display: 'flex', alignItems: 'center'}}>
                      <CopyToClipboard text={this.props.linkCreationMessage.get('tootsLink')} onCopy={() => this._setCopied()}>
                        {!this.state.copied ?
                          <button type="button" className="btn btn-outline-success btn-xs" style={{marginLeft: '5px'}}>copy</button>
                        :
                          <button type="button" className="btn btn-outline-success btn-xs" style={{marginLeft: '5px'}}>copied</button>
                        }
                      </CopyToClipboard>
                    </div>
                  }
                </div>
                <div>
                  <button
                      id="link-submit-button"
                      data-test-id="shortlink-submit-button"
                      type="submit" className="btn btn-default"
                      style={{float: 'right'}}
                      onClick={this.save}
                  >
                    Create
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

    )
  }
});


export const LinkFormContainer = connect(
    mapStateToProps,
    actions
)(LinkForm);
