import React from 'react';
import {connect} from 'react-redux';
import Alert from '@material-ui/lab/Alert';
import {CopyToClipboard} from 'react-copy-to-clipboard';
import * as actions from '../actions';
import * as getters from '../getters';
import Select from 'react-select';
import {ReduxManagedStateComponent} from './Abstract'
import {PrimaryButton, SecondaryButton} from './shared/Buttons';
import {SuccessMessage, ErrorMessage} from './shared/Messages';
import { DEFAULT_NAMESPACE } from '../config';


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
    userInfo: state.get('userInfo'),
    readOnlyMode: getters.readOnlyMode(state),
    namespaces: state.get('namespaces')
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


export class NamespaceSelector extends ReduxManagedStateComponent {

  constructor(props) {
    super(props);

    this.state = {
      componentId: 'namespaceSelector',
      defaults: {}
    };
  }

  handleSelectChange(selectedOption) {
    this.props.updateNewLinkFieldWithString('namespace', selectedOption.value);

    this.props.shortlinkInput.focus();
  }

  render() {
    var widthInEm = 0.65 * Math.max(...this.props.namespaces.map(ns => ns.length));
    var style = {display: 'flex', alignItems: 'center', textAlign: 'right'};

    return (
        <div style={style}>
          <div id="ns-selector" style={{width: widthInEm + 'em'}}>
            <Select
              name="ns"
              value={this.props.newLinkData.get('namespace') || DEFAULT_NAMESPACE}
              onChange={this.handleSelectChange.bind(this)}
              options={this.props.namespaces.toArray().map((namespace) =>  ({value: namespace, label: namespace }))}
              searchable={true}
              noResultsText={null}
              clearable={false}
              arrowRenderer={() => <span style={{width: '0'}}></span>}
              style={{cursor: 'pointer'}}
            />
          </div>
          <div style={{padding: '0 3px 0 7px'}}>
            /
          </div>
        </div>
    )
  }
}
export const NamespaceSelectorContainer = connect(
    mapStateToProps,
    actions
)(NamespaceSelector);


export class LinkForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      value: '',
      copied: false,
    }
  }

  componentDidMount() {
    if (this.props.newLinkData && this.props.newLinkData.get('shortpath')) {  // shortpath already provided by redirect
      this.destinationInput.focus();
    } else {
      this.shortlinkInput.focus();
    }
  }

  save() {
    this.props.saveLink();
  }

  _handleKeyPress(e) {
    if (e.key === 'Enter') {
      document.getElementById('link-submit-button').click();
    }
  }

  _setCopied() {
    const setState = this.setState.bind(this);

    this.setState({copied: true});

    setTimeout(function() {
      setState({copied: false});
    }, 1000);
  }

  render() {

    if (!this.props.linkCreationMessage) {
      var messageText = '';
    } else {
      var messageText = this.props.linkCreationMessage.get('html');
    }

    let messageComponent;
    if (this.props.linkCreationMessage && this.props.linkCreationMessage.get('type') === 'error') {
      messageComponent = <ErrorMessage>{messageText}</ErrorMessage>;
    } else {
      messageComponent = <SuccessMessage>{messageText}</SuccessMessage>;
    }

    const infoBar = this.props.userInfo && this.props.userInfo.get('info_bar');

    return (
        <div className="container" id="link-form">
          {infoBar && (
            <div className="row" style={{marginTop: '-60px', marginBottom: '30px'}}>
              <div className="col-md-8 col-md-offset-2">
                <Alert severity="info" icon={false}>
                  <div style={{fontSize: '1.5rem'}} dangerouslySetInnerHTML={{__html: infoBar}}>
                  </div>
                </Alert>
              </div>
            </div>
          )}
          {'/create' !== this.props.location.pathname ? null : <NewUserIntroContainer />}
          <div className="row">
            <div className="col-md-3 col-md-offset-2">
              <div style={{width: '100%', display: 'flex', alignItems: 'center'}}>
                 <div style={{paddingRight: '5px'}}>
                   {this.props.namespaces.size === 1 ?
                       <div>{DEFAULT_NAMESPACE}/</div>
                       : <NamespaceSelectorContainer shortlinkInput={this.shortlinkInput} />}
                 </div>
                 <input
                     disabled={this.props.readOnlyMode}
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
                     disabled={this.props.readOnlyMode}
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
                  <div className="text-center" style={{fontSize: '0.9em'}}>
                    {messageComponent}
                  </div>
                  <div>
                    <a href={!this.props.linkCreationMessage ? '' : this.props.linkCreationMessage.get('tootsLink')}
                       data-test-id="new-shortlink-anchor-tag"
                       target="_blank"
                       rel="noopener noreferrer"
                       style={{display: !this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink') ? 'none' : 'block',marginLeft:'5px',marginRight:'5px',fontWeight:'bold'}}
                    >
                    {!this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink')
                        ? '' : <SuccessMessage>{this.props.linkCreationMessage.get('tootsLink').split('://')[1]}</SuccessMessage>}
                    </a>
                  </div>
                  {!this.props.linkCreationMessage || !this.props.linkCreationMessage.get('tootsLink') ? null :
                    <div style={{display: 'flex', alignItems: 'center'}}>
                      <CopyToClipboard text={this.props.linkCreationMessage.get('tootsLink')} onCopy={() => this._setCopied()}>
                        <SecondaryButton
                            type="button"
                            variant="outlined"
                            size="small"
                            style={{marginLeft: '5px'}}
                        >
                          {!this.state.copied ? 'copy' : 'copied'}
                        </SecondaryButton>
                      </CopyToClipboard>
                    </div>
                  }
                </div>
                <div>
                  <PrimaryButton
                      disabled={this.props.readOnlyMode}
                      id="link-submit-button"
                      data-test-id="shortlink-submit-button"
                      type="submit" className="btn btn-default"
                      style={{float: 'right'}}
                      onClick={this.save.bind(this)}
                  >
                    Create
                  </PrimaryButton>
                </div>
              </div>
            </div>
          </div>
        </div>

    )
  }
}


export const LinkFormContainer = connect(
    mapStateToProps,
    actions
)(LinkForm);
