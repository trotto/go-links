import React from 'react';
import {connect} from 'react-redux';
import * as actions from '../actions';
import {LinkFormContainer} from './LinkCreation'
import {NavBar} from'./Navigation';
import {ButterbarContainer} from './App';
import {LinkModal} from "./Modals";
import {getConfig} from "../config";


function mapStateToProps(state) {

  state = state.core;

  return {
    shownSubsection: state.get('shownSubsection'),
    links: state.get('links'),
    userInfo: state.get('userInfo'),
    modalShown: state.get('modalShown'),
    linkEditingStatus: state.get('linkEditingStatus')
  };
}


export class MainLayout extends React.Component {

  render() {
    const footerIcon = getConfig('footer.icon');

    return (
        <div style={{height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
          <div>
            <ButterbarContainer />
            <NavBar userInfo={this.props.userInfo} links={this.props.links} location={this.props.location} />
            <LinkFormContainer location={this.props.location} />
            <div style={{width: '100%', marginTop: '20px'}}>
              {this.props.children}
            </div>
          </div>
          <div className="container"
               style={{margin: '30px auto'}}>
            <div className="row">
              <div className="col-md-4 col-md-offset-2" style={{paddingTop: '10px', paddingBottom: '10px'}}>
                <div style={{display: 'flex', maxWidth: '400px'}}>
                  {getConfig('footer.showSourceLink') && (
                    <a style={{marginRight: '10px'}}
                       href="https://github.com/trotto/go-links"
                       target="_blank"
                    >
                      <img height="25" src="/_images/octocat.png" />
                    </a>
                  )}
                  {getConfig('footer.links').map((item, index) =>
                    <a key={index}
                       href={item.get('url')}
                       onClick={item.get('scrollUp') ? () => window.scrollTo(0, 0) : () => {}}
                       style={{color: 'black', opacity: '0.7', fontSize: '1.3em', marginRight: '10px'}}>
                      {item.get('text')}
                    </a>
                  )}
                </div>
              </div>
              <div className="col-md-4 text-right" style={{paddingTop: '10px', color: 'black', opacity: '0.7', fontSize: '1.3em'}}>
                {footerIcon && (
                  <img height="30"
                       src={footerIcon.get('url')}
                       title={footerIcon.get('title', '')}
                       style={{marginRight: '10px'}}
                  />
                )}
              </div>
            </div>
            {getConfig('footer.showFeedbackInvitation') && (
              <div className="row">
                <div id="features" className="col-md-10 col-md-offset-1 text-center" style={{paddingTop: '20px'}}>
                  <p>We <span role="img" aria-label="love love LOVE">❤️ ❤️ ❤️</span> feedback and feature requests. Add requests <a href="https://trello.com/invite/b/TVQdVwnU/71a24cb4c4e6c278c5e3c8fc21014fdc/trotto-go-links-feature-requets" target="_blank" rel="noopener noreferrer">here</a>.</p>
                </div>
              </div>
            )}
          </div>
          <LinkModal
              linkEditingStatus={this.props.linkEditingStatus}
          />
        </div>
    )
  }
}


export const MainLayoutContainer = connect(
    mapStateToProps,
    actions
)(MainLayout);
