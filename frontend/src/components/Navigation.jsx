import React from 'react';
import {getServiceBaseUrl} from '../utils';
import {getConfig} from '../config';


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
    let navItems = getConfig('header.links').toJS()
        .filter(item => this.props.links || item.id !== 'directory');

    if (this.props.userInfo !== undefined) {
      if (this.props.userInfo && this.props.userInfo.get('admin')){
        navItems = navItems.concat(window._trotto.adminLinks);
      }

      navItems.push({
        text: !this.props.userInfo ? 'Sign In' : 'Sign Out',
        url: getServiceBaseUrl('default') + '/_/auth/' + (!this.props.userInfo ? 'login' : 'logout'),
        title: !this.props.userInfo ? '' : 'Sign out of ' + this.props.userInfo.get('email')
      });
    }

    return (
         <div className="container" style={{marginTop: '10px', marginBottom: '80px'}}>
          <div className="row">
            <div className="col-md-8 col-md-offset-2">
              <div style={{width: '100%', display: 'flex', justifyContent: 'space-between'}}>
                <a className="unstyled-link" href="#/">
                  <div style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap'}}>
                    <img style={getConfig('header.logo.css').toJS()} src={getConfig('header.logo.url')} />
                    <div style={{marginLeft: '7px', color: 'black', textDecoration: 'none',
                                 fontSize: '1.6em', opacity: '0.7'}}>
                      <b>{getConfig('header.title')}</b>
                    </div>
                  </div>
                </a>
                <div className="nav-container"
                     style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
                             justifyContent: 'flex-end', flexShrink: 0}}>
                  <nav className="nav-collapse">
                    <ul>
                      {navItems.map(itemData =>
                        <NavBarItem
                            key={itemData.url}
                            text={itemData.text}
                            destination={itemData.url}
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
