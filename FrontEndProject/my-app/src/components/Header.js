import React from 'react';
import './Header.css';

const Header = ({ toggleSidebar }) => {
  return (
    <div className="header">
      <button className="toggle-button" onClick={toggleSidebar}>
        &#9776; {/* Unicode for the "hamburger" menu icon */}
      </button>
      <h1>Report Analyzer</h1>
    </div>
  );
};

export default Header;
