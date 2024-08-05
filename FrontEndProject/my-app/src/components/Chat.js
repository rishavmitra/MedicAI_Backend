import React, { useState, useRef, useEffect } from 'react';
import Message from './Message';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [showUploadButton, setShowUploadButton] = useState(true);
  const [uploadingFile, setUploadingFile] = useState(null); // Store the file being uploaded
  const messageListRef = useRef(null);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, fromUser: true }]);
      setInput('');
    }
  };

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  const getIpAddress = async () => {
    const response = await fetch('https://api64.ipify.org?format=json');
    const data = await response.json();
    return data.ip;
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        alert('Only PDF files are allowed.');
        return;
      }

      setUploading(true);
      setUploadSuccess(false);
      setUploadingFile(file); // Set the file being uploaded

      const ip = await getIpAddress();

      const formData = new FormData();
      formData.append('File', file);
      formData.append('ip', ip);

      fetch('http://127.0.0.1:8000/backend/upload-report/', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.Response) {
          console.log('Success:', data);
          setUploadSuccess(true);
        } else {
          alert(data.Message || 'Failed to upload document. Please try again.');
          setUploadSuccess(false);
        }
        setUploading(false);
        setUploadingFile(null); 
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the document. Please try again.');
        setUploading(false);
        setUploadingFile(null); 
      });
    }
  };

  const handleCancelUpload = () => {
    setUploading(false);
    setUploadSuccess(false);
    setUploadingFile(null);
    document.getElementById('file-input').value = '';
  };

  const handleConfirm = () => {
    setUploadSuccess(false);
    setShowUploadButton(false);
  };

  return (
    <div className="chat">
      <div className="message-list" ref={messageListRef}>
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} fromUser={msg.fromUser} />
        ))}
      </div>
      <div className="chat-input-container">
        <div className="chat-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button className="send-button" onClick={handleSend}>
            <img src="/send-icon.png" alt="Send" />
          </button>
        </div>
        {showUploadButton && !uploadSuccess && (
          <div className={`upload-container ${messages.length ? 'chat-active' : ''}`}>
            {uploading && (
              <div className="uploading-status">
                <div className="spinner"></div>
                <div className="loading">Uploading...</div>
                <button className="cancel-button" onClick={handleCancelUpload}>
                  <img src="/cancel-icon.png" alt="Cancel" />
                </button>
              </div>
            )}
            <p>Upload your Medical Document</p>
            <button className="upload-button" onClick={() => document.getElementById('file-input').click()}>
              <img src="/upload-icon.png" alt="Upload" />
            </button>
            <input
              type="file"
              id="file-input"
              style={{ display: 'none' }}
              onChange={handleUpload}
            />
          </div>
        )}
        {uploadSuccess && (
          <div className="upload-confirmation">
            <h2>File Uploaded Successfully!</h2>
            <button className="confirm-button" onClick={handleConfirm}>
              <img src="/confirm-icon.png" alt="Confirm" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
