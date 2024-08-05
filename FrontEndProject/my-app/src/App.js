import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Chat from './components/Chat';
import './App.css'; // Import the main app CSS if needed

const App = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="app">
      <Header toggleSidebar={toggleSidebar} />
      <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <Sidebar isSidebarOpen={isSidebarOpen} />
        <Chat />
      </div>
    </div>
  );
};

export default App;
