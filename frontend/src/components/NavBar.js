import React from 'react';
import '../css/navbar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">GNSS Navigator</div>
      <button className="navbar-profile">Profile</button>
    </nav>
  );
};

export default NavBar;