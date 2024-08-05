import React from 'react';
import './Sidebar.css'; 

const Sidebar = ({ isSidebarOpen }) => {
  return (
    <div className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
      <h2>History</h2>
      <ul>
        <li><a href="#report">Report 1</a></li>
        <li><a href="#report">Report 2</a></li>
        <li><a href="#report">Report 3</a></li>
      </ul>
    </div>
  );
};

export default Sidebar;
