import React, { useState } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import {connect} from 'react-redux';
import {CircularProgress} from '@material-ui/core';
import {CopyToClipboard} from 'react-copy-to-clipboard';
import * as actions from '../actions';
import {linksById} from "../getters";


Modal.setAppElement('#app');


function mapStateToProps(state) {

  state = state.core;

  return {
    linksById: linksById(state)
  };
}


const modalStyles = {
  content: {
    top: '35%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)'
  }
};


class GenericModal extends React.Component {

  render() {
    const {
      message,
      confirmationComponent,
      confirmed,
      cancelButtonText,
      confirmButtonText,
      confirmButtonClass,
      confirmAction,
      onExit
    } = this.props;

    const confirmButtonStyles = confirmed ? {} : {backgroundColor: 'white'};
    const onConfirm = (() => {
      if (confirmAction)
        confirmAction();
      onExit();
    }).bind(this)

    return (
        <Modal
            isOpen={true}
            style={modalStyles}
            onRequestClose={onExit}
        >
          <div style={{maxWidth: '600px', display: 'flex', flexDirection: 'column'}}>
            <div>
              {message}
            </div>
            {confirmationComponent || null}
            <div style={{display: 'flex', width: '100%', justifyContent: 'space-between'}}>
              <button
                  type="submit" className="btn btn-muted"
                  onClick={this.props.onExit}
                  style={cancelButtonText ? {} : {visibility: 'hidden'}}
              >
                {cancelButtonText}
              </button>
              {confirmButtonText && (
                <button
                    type="submit"
                    className={`btn ${confirmed ? (confirmButtonClass || 'btn-default') : 'btn-disabled'}`}
                    style={confirmButtonStyles}
                    disabled={!confirmed}
                    onClick={onConfirm}
                >
                  {confirmButtonText}
                </button>
              )}
            </div>
          </div>
        </Modal>
    )
  }
}


const ProgressSpinner = () => (
    <div style={Object.assign({zIndex: 10000, position: 'fixed'}, modalStyles.content)}>
      <CircularProgress style={{color: '#f27e8f'}} />
    </div>
);


class DeletionConfirmation extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      confirmationText: '',
      shortpath: this.props.link.get('shortpath')
    }
  }

  componentDidMount() {
    this.confirmationInput.focus();
  }

  onChange(e) {
    const confirmationText = e.target.value.trim();

    this.setState({ confirmationText });

    this.props.setConfirmed(confirmationText === this.state.shortpath);
  }

  render() {
    return (
      <input
          ref={(input) => {
            this.confirmationInput = input;
          }}
          className="form-control"
          style={{width: '100%', margin: '10px 0 20px'}}
          type="text" id="shortpath" placeholder={this.state.shortpath}
          value={this.state.confirmationText}
          onChange={this.onChange.bind(this)}
      />
    )
  }
}


const DeletionModal = connect(
  mapStateToProps,
  actions
)(({ linkId, linksById, deleteLink, setLinkEditingStatus }) => {
  const [confirmed, setConfirmed] = useState(false);

  let link = linksById.get(linkId);
  link = link.set('shortpath', `go/${link.get('shortpath')}`);

  const message = (
      <div>
        <p>
          Deleting a go link will delete the go link for everyone in your organization. No one on your
          team will be able to use <span style={{fontWeight:'bold'}}>{link.get('shortpath')}</span> until
          it's re-created.
        </p>
        <p>
          To confirm deletion, type <span style={{fontWeight:'bold'}}>{link.get('shortpath')}</span> and
          press Delete.
        </p>
      </div>
  );

  const confirmationComponent = (
      <DeletionConfirmation
          link={link}
          setConfirmed={setConfirmed}
      />
  );

  return (
      <GenericModal
          key="deletion-modal"
          message={message}
          confirmationComponent={confirmationComponent}
          confirmed={confirmed}
          cancelButtonText="Cancel"
          confirmButtonText="Delete"
          confirmButtonClass="btn-electric"
          confirmAction={deleteLink.bind(this, linkId)}
          onExit={setLinkEditingStatus.bind(this, {})}
      />
  );
});


const InitTransferModal = connect(
  mapStateToProps,
  actions
)(({ linkId, linksById, setLinkEditingStatus }) => {
  const [transferLink, setTransferLink] = useState(null);
  const [justCopied, setJustCopied] = useState(false);

  if (!transferLink) {
    axios.post(`/_/api/links/${linkId}/transfer_link`, {}, {
      headers: {'X-CSRFToken': window._trotto.csrfToken}
    }).then((resp) => setTransferLink(resp.data.url));

    return <ProgressSpinner />;
  }

  let link = linksById.get(linkId);
  link = link.set('shortpath', `go/${link.get('shortpath')}`);

  const onCopy = () => {
    setJustCopied(true);

    setTimeout(() => {
      setJustCopied(false);
    }, 3000);
  }

  const copyStyle = { textAlign: 'center' };
  if (justCopied)
    copyStyle.fontStyle = 'italic';

  const message = (
      <div>
        <div>
          To transfer ownership of <span style={{fontWeight:'bold'}}>{link.get('shortpath')}</span>, copy this link
          and send it to the new owner:
        </div>
        <CopyToClipboard text={transferLink} onCopy={onCopy}>
          <div style={{cursor: 'pointer'}}>
            <pre style={{margin: '10px 0'}}>
              <code style={{wordWrap: 'break-word'}}>
                {transferLink}
              </code>
            </pre>
            <div style={copyStyle}>
              {justCopied ? 'Copied!' : 'Click to copy'}
            </div>
          </div>
        </CopyToClipboard>
      </div>
  );

  return (
      <GenericModal
          key="init-transfer-modal"
          message={message}
          confirmationComponent={null}
          confirmed={true}
          cancelButtonText={null}
          confirmButtonText="Done"
          onExit={setLinkEditingStatus.bind(this, {})}
      />
  );
});


const CompleteTransferModal = connect(
  mapStateToProps,
  actions
)(({ linkId: linkToken, linksById, setLinkEditingStatus, setErrorBarMessage, takeOwnershipOfLink }) => {
  const tokenPayload = JSON.parse(atob(atob(linkToken).split('.')[1]));
  const linkIdActual = parseInt(tokenPayload.sub.slice('link:'.length));

  if (linksById === undefined)
    return <ProgressSpinner />;

  const link = linksById.get(linkIdActual);

  if (!link) {
    setErrorBarMessage('The go link for this transfer link no longer exists');

    setLinkEditingStatus({});

    return null;
  }

  const message = (
      <div style={{marginBottom: '10px'}}>
        Would you like to take ownership of
        of <span style={{fontWeight:'bold'}}>go/{link.get('shortpath')}</span>?
      </div>
  );

  return (
      <GenericModal
          key="complete-transfer-modal"
          message={message}
          confirmationComponent={null}
          confirmed={true}
          cancelButtonText="Cancel"
          confirmButtonText="Take ownership"
          confirmAction={takeOwnershipOfLink.bind(this, linkToken)}
          onExit={setLinkEditingStatus.bind(this, {})}
      />
  );
});


const ACTION_TO_MODAL = {
  delete: DeletionModal,
  transfer: InitTransferModal,
  completeTransfer: CompleteTransferModal
}


export const LinkModal = ({ linkEditingStatus }) => {
  if (linkEditingStatus.size === 0)
    return null;

  const [action, linkId] = linkEditingStatus.entrySeq().get(0);

  if (!linkId || !ACTION_TO_MODAL[action])
    return null;

  return React.createElement(ACTION_TO_MODAL[action], { linkId }, null);
}
