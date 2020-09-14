import React from 'react';
import {connect} from 'react-redux';
import * as actions from '../actions';
import { browserHistory } from 'react-router';
import ReactTable from "react-table";
import {Map, List, Set, fromJS} from 'immutable';
import Modal from 'react-modal';
import { CreateOutlined, Cancel, DeleteOutline } from '@material-ui/icons';
import {getServiceBaseUrl} from '../utils'

var validUrl = require('valid-url');


function mapStateToProps(state) {

  state = state.core;

  return {
    links: state.get('links') || List(),
    defaultLinkSearchTerm: state.get('defaultLinkSearchTerm'),
    userInfo: state.get('userInfo'),
    draftDestination: state.getIn(['editing', 'draftDestination']),
    goSupportedInCurrentSession: state.get('goSupportedInCurrentSession'),
    currentlyEditingLinkId: state.getIn(['linkEditingState', 'currentlyEditingLinkId']),
    linkToDelete: state.getIn(['linkEditingState', 'linkToDelete'])
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
    if (this.props.currentlyEditingLinkId === this.props.id
        && prevProps.currentlyEditingLinkId !== this.props.id) {
      $('#edit-input-' + this.props.id).select();
    }
  }

  setMousedOver(bool) {
    this.setState({
      mousedOver: bool
    })
  }

  setEditingLinkId(linkId) {
    if (linkId === this.props.currentlyEditingLinkId) {
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

  isCurrentlyBeingEdited(linkId) {
    return this.props.id === this.props.currentlyEditingLinkId;
  }

  updateLink() {
    if (this.draftDestinationIsValid()) {
      this.props.updateLink(this.props.id, {destination: this.props.draftDestination});

      this.setEditingLinkId(null);
    }
  }

  render() {
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
                <Cancel
                    fontSize="large"
                    onClick={this.setEditingLinkId.bind(this, null)}
                />
                  :
                <CreateOutlined
                    fontSize="large"
                    style={{color: '#f27e8f', opacity: this.state.mousedOver ? '1' : '0.6'}}
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
                onChange={this.handleChange.bind(this)}
                onKeyPress={this.handleKeyPress.bind(this)}
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
          {!this.props.editable ? null :
              <div style={{paddingLeft: '5px', display: 'flex',
                           alignItems: 'center'}}
              >
                <DeleteOutline
                    fontSize="large"
                    style={{cursor: 'pointer'}}
                    onClick={() => this.props.setLinkToDelete(this.props.link)}
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


export class DeletionModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      confirmationText: ''
    }
  }

  focus() {
    this.confirmationInput.focus();
  }

  isConfirmed() {
    return this.state.confirmationText.trim() === this.props.link.get('shortpath');
  }

  render() {
    const deletionConfirmed = this.isConfirmed();
    const deleteButtonStyles = deletionConfirmed ? {} : {backgroundColor: 'white'};

    return (
        <Modal
           isOpen={true}
           onAfterOpen={this.focus.bind(this)}
           style={modalStyles}
        >
          <div style={{maxWidth: '600px', display: 'flex', flexDirection: 'column'}}>
            <div>
              <p>
                Deleting a go link will delete the go link for everyone in your organization. No one on your
                team will be able to use <span style={{fontWeight:'bold'}}>{this.props.link.get('shortpath')}</span> until
                it's re-created.
              </p>
              <p>
                To confirm deletion, type <span style={{fontWeight:'bold'}}>{this.props.link.get('shortpath')}</span> and
                press Delete.
              </p>
            </div>
            <input
               ref={(input) => { this.confirmationInput = input; }}
               className="form-control"
               style={{width: '100%', margin: '10px 0 20px'}}
               type="text" id="shortpath" placeholder={this.props.link.get('shortpath')}
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
}


export class LinksTable extends React.Component {

  setEditingLinkId(linkId) {
    this.props.updateLinkEditingState({currentlyEditingLinkId: linkId});
  }

  setLinkToDelete(linkToDelete) {
    this.props.updateLinkEditingState({ linkToDelete });
  }

  render() {

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
                    key={row.original.id + '-' + row.value}
                    destination={row.value}
                    id={row.original.id}
                    link={row.original}
                    editable={editable}
                    setEditingLinkId={this.setEditingLinkId.bind(this)}
                    setLinkToDelete={this.setLinkToDelete.bind(this)}
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
          {!this.props.linkToDelete ? null :
              <DeletionModal
                link={this.props.linkToDelete}
                deleteLink={this.props.deleteLink.bind(this, this.props.linkToDelete.get('id'))}
                exit={this.setLinkToDelete.bind(this, null)}
              />
          }
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
        goSupportedInCurrentSession: state.get('goSupportedInCurrentSession'),
        linkToDelete: state.getIn(['linkEditingState', 'linkToDelete'])
      };
    },
    actions
)(LinksTable);
