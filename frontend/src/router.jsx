import React from 'react';
import { render } from 'react-dom'
import { Router, Route, Redirect, IndexRoute, hashHistory } from 'react-router';
import { App } from './components/App';
import { MainLayoutContainer } from './components/Layout';
import { LinksTableContainer } from './components/LinkList';
import { hot } from 'react-hot-loader/root';


export class TrottoRouter extends React.Component {
  render() {
    return (
        <Router key={Math.random()}  // providing key eliminates distracting "You cannot change <Router routes>" error
                                     // in console when hot-loading
                history={hashHistory}>
          <Route component={App}>
            <Route component={MainLayoutContainer}>
              <Route path="/" component={LinksTableContainer}/>
              <Route path="/create" component={null}/>
              <Route path="/directory" component={LinksTableContainer}/>
            </Route>
          </Route>
        </Router>
    );
  }
}


export default hot(TrottoRouter);
