import React from 'react';
import {connect} from 'react-redux';
import { hashHistory } from 'react-router';
import * as actions from '../actions';
import {Map, List} from 'immutable';
import {LinkFormContainer} from './LinkCreation'
import {NavBar} from'./Navigation';
import {ButterbarContainer} from './App';


const TROTTO_HOSTED = location.hostname.slice(location.hostname.length - 7) === 'trot.to';


function mapStateToProps(state) {

  state = state.core;

  return {
    shownSubsection: state.get('shownSubsection'),
    links: state.get('links'),
    userInfo: state.get('userInfo'),
    modalShown: state.get('modalShown')
  };
}


export const MainLayout = React.createClass({

  render: function() {

    const FOOTER_ITEMS = !TROTTO_HOSTED ? [] : [
      {
        text: 'Pricing',
        path: 'https://www.trot.to/pricing'
      },
      {
        text: 'Privacy',
        path: 'https://www.trot.to/privacy'
      },
      {
        text: 'Terms',
        path: 'https://www.trot.to/terms'
      },
      {
        text: 'Contact Us',
        path: 'https://www.trot.to/contact'
      }
    ];

    return (
        <div style={{height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
          <div>
            {TROTTO_HOSTED ? <ButterbarContainer /> : null}
            <NavBar userInfo={this.props.userInfo} links={this.props.links} location={this.props.location} />

            {function(props) {
              if (['/', '/create', '/directory'].indexOf(props.location.pathname) !== -1) {
                return <LinkFormContainer location={props.location} />;
              }

            }(this.props)}

            <div style={{width: '100%', marginTop: '20px'}}>
              {this.props.children}
            </div>
          </div>
          <div className="container"
               style={{margin: '30px auto'}}>
            <div className="row">
              <div className="col-md-4 col-md-offset-2" style={{paddingTop: '10px', paddingBottom: '10px'}}>
                <div style={{display: 'flex', maxWidth: '400px', justifyContent: 'space-between'}}>
                  <a style={{display: 'none', marginRight: '10px'}}
                     href="https://github.com/trotto/go-links"
                     target="_blank"
                  >
                    <img height="25" src="/_images/octocat.png" />
                  </a>
                  {FOOTER_ITEMS.map((item, index) =>
                    <a key={index}
                       href={item.path}
                       onClick={item.scrollUp ? () => window.scrollTo(0, 0) : () => {}}
                       style={{color: 'black', opacity: '0.7', fontSize: '1.3em', marginRight: '10px'}}>
                      {item.text}
                    </a>
                  )}
                </div>
              </div>
              <div className="col-md-4 text-right" style={{paddingTop: '10px', color: 'black', opacity: '0.7', fontSize: '1.3em'}}>
                <img height="30"
                     src="/_images/toots.png"
                     title="Toots the Pig, Stubbifier First Class"
                     style={{marginRight: '10px'}}
                />
              </div>
            </div>
            <div className="row">
              <div id="credits" className="col-md-10 col-md-offset-1 text-center" style={{paddingTop: '20px'}}>
                <div>
                  Icons made
                  by <a href="https://www.flaticon.com/authors/vectors-market" title="Vectors Market">Vectors Market</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> are
                  licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>
                </div>
              </div>
            </div>
          </div>
        </div>

    )
  }
});


export const MainLayoutContainer = connect(
    mapStateToProps,
    actions
)(MainLayout);
