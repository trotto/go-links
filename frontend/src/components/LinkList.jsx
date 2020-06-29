import React from 'react';
import {connect} from 'react-redux';
import * as actions from '../actions';
import { browserHistory } from 'react-router';
import ReactTable from "react-table";
import {Map, List, Set, fromJS} from 'immutable';
import Modal from 'react-modal';
import {getServiceBaseUrl} from '../utils'

var validUrl = require('valid-url');


function mapStateToProps(state) {

  state = state.core;

  return {
    links: state.get('links') || List(),
    defaultLinkSearchTerm: state.get('defaultLinkSearchTerm'),
    userInfo: state.get('userInfo'),
    draftDestination: state.getIn(['editing', 'draftDestination']),
    goSupportedInCurrentSession: state.get('goSupportedInCurrentSession')
  };
}


const EditableDestination = React.createClass({

  getInitialState: function() {
    return {
      mousedOver: false,
      originalDestination: this.props.destination
    }
  },

  componentDidUpdate: function(prevProps, prevState) {
    if (this.props.currentlyEditingLinkId === this.props.id
        && prevProps.currentlyEditingLinkId !== this.props.id) {
      $('#edit-input-' + this.props.id).select();
    }
  },

  setMousedOver: function(bool) {
    this.setState({
      mousedOver: bool
    })
  },

  setEditingLinkId: function(linkId) {
    if (linkId === this.props.currentlyEditingLinkId) {
      return;
    }

    this.props.setDraftDestination(null);

    this.props.setEditingLinkId(linkId);
  },

  handleChange: function(evt){
    this.props.setDraftDestination(evt.target.value);
  },

  handleKeyPress: function(e) {
    if (e.key === 'Enter') {
      this.updateLink();
    }
  },

  draftDestinationIsValid: function() {
    if (!this.props.draftDestination) {
      return false;
    }

    if (this.props.draftDestination.indexOf('http://') !== 0
        && this.props.draftDestination.indexOf('https://') !== 0) {
      return false;
    }

    return validUrl.isUri(this.props.draftDestination.replace(/%s/g, 'ss'));
  },

  getDisplayUrl: function() {
    return this.isCurrentlyBeingEdited() && (this.props.draftDestination || this.props.draftDestination === '')
        ? this.props.draftDestination : this.state.originalDestination;
  },

  isCurrentlyBeingEdited: function(linkId) {
    return this.props.id === this.props.currentlyEditingLinkId;
  },

  updateLink: function() {
    if (this.draftDestinationIsValid()) {
      this.props.updateLink(this.props.id, {destination: this.props.draftDestination});

      this.setEditingLinkId(null);
    }
  },

  render: function() {
    const currentlyBeingEdited = this.isCurrentlyBeingEdited();

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
                       flexGrow: 1}}
               onClick={!this.props.editable ? () => {} : this.setEditingLinkId.bind(this, this.props.id)}
               onMouseOver={this.setMousedOver.bind(this, true)}
               onMouseOut={this.setMousedOver.bind(this, false)}
          >
            <div style={{width: '25px', paddingRight: '5px', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              {currentlyBeingEdited ?
                <img src="/_images/icons/close.svg" height="16"
                     style={{opacity: '0.7'}}
                     onClick={this.setEditingLinkId.bind(this, null)}
                />
                  :
                <img src={'/_images/icons/' + (this.state.mousedOver ? 'edit.svg' : 'edit_light.svg')} height="14"
                     style={{visibility: this.props.editable ? 'visible' : 'hidden'}}
                />
              }
            </div>
            <div style={inputWrapperStyle}>
              <input
                id={'edit-input-' + this.props.id}
                style={{flexGrow: '1', padding: '4px 7px 4px 2px',
                        borderColor: 'transparent', backgroundColor: 'transparent',
                        cursor: this.props.editable ? 'pointer' : 'default'}}
                value={this.getDisplayUrl()}
                disabled={!currentlyBeingEdited}
                onChange={this.handleChange}
                onKeyPress={this.handleKeyPress}
              />
              {!currentlyBeingEdited ? null :
                  <button
                      className="btn btn-default"
                      style={{padding: '3px 6px', fontSize: '14px'}}
                      disabled={!this.draftDestinationIsValid()}
                      onClick={e => {e.stopPropagation(); this.updateLink()}}
                  >
                    Save
                  </button>
              }
            </div>
          </div>
          {!this.props.deletable ? null :
              <div style={{width: '25px', paddingLeft: '5px', display: 'flex',
                           flexDirection: 'column', alignItems: 'center'}}
              >
                <img src={'/_images/icons/' + 'trash.svg'} height="14"
                     style={{cursor: 'pointer'}}
                     onClick={() => this.props.setLinkToDelete(this.props.link)}
                />
              </div>
          }
        </div>
    );
  }

});


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
      shortlink = shortlink.replace('http://go', getServiceBaseUrl());
    }

    return (
         <div
             style={{display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'space-between'}}
         >
           <a href={shortlink}
              target="_blank"
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


const modalStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)'
  }
};


const DeletionModal = React.createClass({
  getInitialState: function () {
     return {
       confirmationText: '',
     }
   },

  focus: function() {
    this.confirmationInput.focus();
  },

  isConfirmed: function() {
    return this.state.confirmationText.trim() === this.props.link.shortpath;
  },

  render: function() {
    const deletionConfirmed = this.isConfirmed();
    const deleteButtonStyles = deletionConfirmed ? {} : {backgroundColor: 'white'};

    return (
        <Modal
           isOpen={true}
           onAfterOpen={this.focus}
           style={modalStyles}
        >
          <div style={{maxWidth: '600px', display: 'flex', flexDirection: 'column'}}>
            <div>
              <p>
                Deleting a go link will delete the go link for everyone in your organization. No one on your
                team will be able to use <span style={{fontWeight:'bold'}}>{this.props.link.shortpath}</span> until
                it's re-created.
              </p>
              <p>
                To confirm deletion, type <span style={{fontWeight:'bold'}}>{this.props.link.shortpath}</span> and
                press Delete.
              </p>
            </div>
            <input
               ref={(input) => { this.confirmationInput = input; }}
               className="form-control"
               style={{width: '100%', margin: '10px 0 20px'}}
               type="text" id="shortpath" placeholder={this.props.link.shortpath}
               value={this.state.confirmationText}
               onChange={(e) => this.setState({ confirmationText: e.target.value.trim() })}
             />
            <div style={{display: 'flex', width: '100%', justifyContent: 'space-between'}}>
              <button
                type="submit" className="btn btn-muted"
                onClick={this.props.exit}
              >
                Cancel
              </button>
              <button
                type="submit"
                className={`btn ${deletionConfirmed ? 'btn-electric' : 'btn-disabled'}`}
                style={deleteButtonStyles}
                disabled={!deletionConfirmed}
                onClick={() => { this.props.deleteLink(); this.props.exit(); }}
              >
                Delete
              </button>
            </div>
          </div>
        </Modal>
    )
  }
})


export const LinksTable = React.createClass({

  getInitialState: function () {
     return {
       currentlyEditingLinkId: null,
       linkToDelete: null
     }
   },

  setEditingLinkId: function(linkId) {
    this.setState({currentlyEditingLinkId: linkId})
  },

  setLinkToDelete: function(linkToDelete) {
    this.setState({ linkToDelete });
  },

  render: function() {

    const DEFAULT_CELL_STYLING = {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'start',
      paddingRight: '15px',
      paddingLeft: '15px'
    };

    var COLUMNS = [
      {
        Header: "Shortlink",
        accessor: "shortpath",
        maxWidth: '200',
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
                    key={row.original.oid + '-' + row.value}
                    destination={row.value}
                    id={row.original.oid}
                    link={row.original}
                    editable={editable}
                    deletable={editable}
                    setEditingLinkId={this.setEditingLinkId}
                    setLinkToDelete={this.setLinkToDelete}
                    currentlyEditingLinkId={this.state.currentlyEditingLinkId}
          />
        }
      },
      {
        Header: "Owner",
        accessor: "owner",
        maxWidth: '200',
        style: DEFAULT_CELL_STYLING,
        // doing this because justify-content style specified with `style` key gets reverted to default when
        // resizing (possible bug in library)
        Cell: row => <div style={{display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'flex-start'}}>
                       {row.value}
                     </div>
      }
    ];

    if (!this.props.userInfo) {
      var data = List();
    } else {
      var data = this.props.links.map(
          link => link.update('shortpath', shortpath => 'go' + '/' + shortpath));
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
              style={DEFAULT_CELL_STYLING}
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
          {!this.state.linkToDelete ? null :
              <DeletionModal
                link={this.state.linkToDelete}
                deleteLink={this.props.deleteLink.bind(this, this.state.linkToDelete.oid)}
                exit={this.setState.bind(this, { linkToDelete: null })}
              />
          }
        </div>
    );
  }
});


export const LinksTableContainer = connect(
    mapStateToProps,
    actions
)(LinksTable);
