import React from 'react';
import {connect} from 'react-redux';
import { hashHistory } from 'react-router';
import {Map, List} from 'immutable';
import {getServiceBaseUrl} from '../utils';


export class NavBarItem extends React.Component {

  render() {
    var style = {};

    if (window.location.hash === this.props.destination) {
      style.opacity = '1';
      style.cursor = 'auto';
      style.textDecoration = 'none';
    }

    return (
        <li>
          <a
              style={style}
              data-test-id={this.props.text.toLowerCase().replace(/ /g, '-') + '-link'}
              href={this.props.destination}
              title={this.props.title || ''}
              target={this.props.openInNewTab ? '_blank' : null}
          >
            {this.props.text}
          </a>
        </li>
    )
  }
}


export class NavBar extends React.Component {

  componentDidMount() {
    var nav = responsiveNav(".nav-collapse", {
      closeOnNavClick: true
    });
  }

  render() {
    var navItems = [
      {
        text: 'How It Works',
        destination: 'https://www.trot.to/how-it-works',
        openInNewTab: true
      }
    ];

    if (this.props.userInfo !== undefined) {
      navItems.push({
        text: !this.props.userInfo ? 'Sign In' : 'Sign Out',
        destination: getServiceBaseUrl('default') + '/_/auth/' + (!this.props.userInfo ? 'login' : 'logout'),
        title: !this.props.userInfo ? '' : 'Sign out of ' + this.props.userInfo.get('email')
      });
    }

    if (this.props.links) {
      navItems.splice(0, 0, {
        text: 'Directory',
        destination: '#/directory'
      });
    }

    return (
         <div className="container" style={{marginTop: '10px', marginBottom: '80px'}}>
          <div className="row">
            <div className="col-md-8 col-md-offset-2">
              <div style={{width: '100%', display: 'flex', justifyContent: 'space-between'}}>
                <a className="unstyled-link" href="#/">
                  <div style={{display: 'flex', alignItems: 'center'}}>
                    <img style={{height: '1.6em'}} src="/_images/snout.png" />
                    <div style={{marginLeft: '7px', color: 'black', textDecoration: 'none',
                                 fontSize: '1.6em', opacity: '0.7'}}>
                      <b>Trotto</b>
                    </div>
                  </div>
                </a>
                <div className="nav-container"
                     style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
                             justifyContent: 'flex-end'}}>
                  <nav className="nav-collapse">
                    <ul>
                      {navItems.map(itemData =>
                        <NavBarItem
                            key={itemData.destination}
                            text={itemData.text}
                            destination={itemData.destination}
                            title={itemData.title}
                            openInNewTab={itemData.openInNewTab}
                        />
                      )}
                    </ul>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
  }
}
