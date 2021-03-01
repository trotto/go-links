import React from 'react';
import {connect} from 'react-redux';
import * as actions from '../actions';
import ReactTable from "react-table";
import {List} from 'immutable';
import { CreateOutlined, Cancel, DeleteOutline, Reply } from '@material-ui/icons';
import {PrimaryButton} from './shared/Buttons';
import {getServiceBaseUrl} from '../utils'
import { DEFAULT_NAMESPACE } from '../config';

var validUrl = require('valid-url');


function mapStateToProps(state) {

  state = state.core;

  return {
    links: state.get('links') || List(),
    defaultLinkSearchTerm: state.get('defaultLinkSearchTerm'),
    userInfo: state.get('userInfo'),
    draftDestination: state.getIn(['editing', 'draftDestination']),
    goSupportedInCurrentSession: state.get('goSupportedInCurrentSession'),
    linkEditingStatus: state.get('linkEditingStatus')
  };
}


class EditableDestination extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      mousedOver: false,
      originalDestination: this.props.destination
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.linkEditingStatus.get('edit') === this.props.id
        && prevProps.linkEditingStatus.get('edit') !== this.props.id) {
      $('#edit-input-' + this.props.id).select();
    }
  }

  setMousedOver(bool) {
    this.setState({
      mousedOver: bool
    })
  }

  setEditingLinkId(linkId) {
    if (linkId === this.props.linkEditingStatus.get('edit')) {
      return;
    }

    this.props.setDraftDestination(null);

    this.props.setEditingLinkId(linkId);
  }

  handleChange(evt){
    this.props.setDraftDestination(evt.target.value);
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.updateLink();
    }
  }

  draftDestinationIsValid() {
    if (!this.props.draftDestination) {
      return false;
    }

    if (this.props.draftDestination.indexOf('http://') !== 0
        && this.props.draftDestination.indexOf('https://') !== 0) {
      return false;
    }

    return validUrl.isUri(this.props.draftDestination.replace(/%s/g, 'ss'));
  }

  getDisplayUrl() {
    return this.isCurrentlyBeingEdited() && (this.props.draftDestination || this.props.draftDestination === '')
        ? this.props.draftDestination : this.state.originalDestination;
  }

  isCurrentlyBeingEdited() {
    return this.props.id === this.props.linkEditingStatus.get('edit');
  }

  updateLink() {
    if (this.draftDestinationIsValid()) {
      this.props.updateLink(this.props.id, {destination: this.props.draftDestination});

      this.setEditingLinkId(null);
    }
  }

  render() {
    const currentlyBeingEdited = this.isCurrentlyBeingEdited();
    const linkId = this.props.link.id;

    var inputWrapperStyle = {
      borderColor: 'transparent',
      backgroundColor: 'transparent',
      display: 'flex',
      alignItems: 'center',
      cursor: this.props.editable ? 'pointer' : 'default',
      flexGrow: '1',
      padding: '5px',
      borderRadius: '5px'
    };

    if (currentlyBeingEdited) {
      inputWrapperStyle.backgroundColor = 'white';
    }

    return (
        <div style={{display: 'flex', width: '100%', justifyContent: 'space-between', alignItems: 'center'}}>
          <div style={{display: 'flex', alignItems: 'center', cursor: this.props.editable ? 'pointer' : 'default',
                       width: 0, flexGrow: 1}}
               onClick={!this.props.editable ? () => {} : this.setEditingLinkId.bind(this, this.props.id)}
               onMouseOver={this.setMousedOver.bind(this, true)}
               onMouseOut={this.setMousedOver.bind(this, false)}
          >
            <div style={{width: '25px', paddingRight: '5px', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              {currentlyBeingEdited ?
                <Cancel
                    fontSize="large"
                    onClick={this.setEditingLinkId.bind(this, null)}
                />
                  :
                  (this.props.editable && <CreateOutlined
                      fontSize="large"
                      color="primary"
                      style={{opacity: this.state.mousedOver ? '1' : '0.6'}}
                  />)
              }
            </div>
            <div style={inputWrapperStyle}>
              <input
                id={'edit-input-' + this.props.id}
                style={{width: 0, flexGrow: '1', padding: '4px 7px 4px 2px',
                        borderColor: 'transparent', backgroundColor: 'transparent',
                        cursor: this.props.editable ? 'pointer' : 'default'}}
                value={this.getDisplayUrl()}
                disabled={!currentlyBeingEdited}
                onChange={this.handleChange.bind(this)}
                onKeyPress={this.handleKeyPress.bind(this)}
              />
              {!currentlyBeingEdited ? null :
                  <PrimaryButton
                      style={{padding: '3px 6px', fontSize: '12px'}}
                      disabled={!this.draftDestinationIsValid()}
                      onClick={e => {e.stopPropagation(); this.updateLink()}}
                  >
                    Save
                  </PrimaryButton>
              }
            </div>
          </div>
          {this.props.editable && !currentlyBeingEdited &&
              <div style={{paddingLeft: '5px', display: 'flex', alignItems: 'center'}}
              >
                <DeleteOutline
                    titleAccess={`Delete ${this.props.link.shortpath}`}
                    fontSize="large"
                    style={{cursor: 'pointer'}}
                    onClick={() => this.props.setLinkEditingStatus({ delete: linkId })}
                />
                <Reply
                    titleAccess={`Transfer ${this.props.link.shortpath}`}
                    fontSize="large"
                    style={{cursor: 'pointer', transform: 'scale(-1,1)'}}
                    onClick={() => this.props.setLinkEditingStatus({ transfer: linkId })}
                />
              </div>
          }
        </div>
    );
  }

}


export const EditableDestinationContainer = connect(
    mapStateToProps,
    actions
)(EditableDestination);


class KeywordCell extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    const row = this.props.row;

    var shortlink = 'http://' + row.value;

    if (!this.props.goSupportedInCurrentSession) {
      shortlink = shortlink.replace(`http://${DEFAULT_NAMESPACE}`, getServiceBaseUrl());
    }

    return (
         <div
             style={{display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'space-between'}}
         >
           <a href={shortlink}
              target="_blank"
              rel="noopener noreferrer"
              style={{width: '0', flexGrow: '1', overflow: 'hidden'}}
           >
             {row.value}
           </a>
         </div>
    )
  }
}


class CountCell extends React.Component {

  render() {
    const row = this.props.row;

    if (row.value === null && row.viewIndex !== 0) {
      return null;
    }

    var style = this.props.style;

    if (row.value === null) {
      style.display = 'flex';
      style.justifyContent = 'center';
      style.height = '30px';
    }

    return <div style={this.props.style}>
             {row.value || 0}
           </div>;
  }
}


export class LinksTable extends React.Component {

  setEditingLinkId(linkId) {
    this.props.setLinkEditingStatus({edit: linkId});
  }

  render() {

    const DEFAULT_CELL_STYLING = {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'start',
      paddingRight: '15px',
      paddingLeft: '15px',
      height: 'inherit'
    };

    var COLUMNS = [
      {
        Header: "Shortlink",
        accessor: "shortpath",
        maxWidth: '120',
        style: DEFAULT_CELL_STYLING,
        Cell: row => {
          return <KeywordCell row={row} goSupportedInCurrentSession={this.props.goSupportedInCurrentSession} />
        }
      },
      {
        Header: "Destination",
        accessor: "destination_url",
        Cell: row => {
          const editable = this.props.userInfo &&
              (this.props.userInfo.get('admin') || row.original.owner === this.props.userInfo.get('email'));

          return <EditableDestinationContainer
                    key={row.original.id + '-' + row.value}
                    destination={row.value}
                    id={row.original.id}
                    link={row.original}
                    editable={editable}
                    setEditingLinkId={this.setEditingLinkId.bind(this)}
          />
        }
      },
      {
        Header: "Owner",
        accessor: "owner",
        maxWidth: '120',
        style: DEFAULT_CELL_STYLING,
        // doing this because justify-content style specified with `style` key gets reverted to default when
        // resizing (possible bug in library)
        Cell: row => <div style={{display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'flex-start'}}
                          title={row.value}
                     >
                       {row.value.split('@')[0]}
                     </div>
      }
    ];

    if (!this.props.userInfo) {
      var data = List();
    } else {
      var data = this.props.links.map(
          link => link.update('shortpath', shortpath => (link.get('namespace') || DEFAULT_NAMESPACE) + '/' + shortpath));
    }

    // Note: For the moment, the default install doesn't track visit counts.
    const showVisitCounts =
        location.host === 'trot.to' || data.findIndex(link => link.get('visits_count')) > -1;

    if (showVisitCounts && (window.innerWidth || window.clientWidth || window.clientWidth || 0) > 600) {
      COLUMNS.splice(2, 0, {
        Header: "Visits",
        accessor: "visits_count",
        maxWidth: '100',
        Cell: row => {
          return <CountCell
              style={Object.assign({}, DEFAULT_CELL_STYLING, {height: '100%'})}
              row={row}
              visitCountsProgress={this.props.visitCountsProgress}
          />
        }
      });
    }

    const filterMethod = (filter, row, column) => {
      // modification of default method given at https://react-table.js.org/#/story/readme, changing the following:
      // 1) matching any substring (not just start)
      const id = filter.pivotId || filter.id;

      return row[id] !== undefined ? String(row[id]).toLowerCase().includes(filter.value.toLowerCase()) : true;
    };

    var defaultFiltered = [];
    if (this.props.defaultLinkSearchTerm) {
      defaultFiltered.push({
        id: "shortpath",
        value: this.props.defaultLinkSearchTerm
      });
    }

    return (
        <div className="container">
          <div className="row" style={{lineHeight: '1.3em'}}>
            <div className="col-md-8 col-md-offset-2">
              <div style={{width: '100%', overflowX: 'scroll'}}>
                <ReactTable
                  data={data.toJS()}
                  columns={COLUMNS}
                  defaultSorted={[
                    {
                      id: "visits_count",
                      desc: true
                    }
                  ]}
                  defaultFiltered={defaultFiltered}
                  filterable={true}
                  defaultFilterMethod={filterMethod}
                  noDataText={''}
                  defaultPageSize={10}
                  className="-striped -highlight"
                />
              </div>
            </div>
          </div>
        </div>
    );
  }
}


export const LinksTableContainer = connect(
    (states) => {
      const state = states.core;

      return {
        links: state.get('links') || List(),
        defaultLinkSearchTerm: state.get('defaultLinkSearchTerm'),
        userInfo: state.get('userInfo'),
        goSupportedInCurrentSession: state.get('goSupportedInCurrentSession')
      };
    },
    actions
)(LinksTable);
