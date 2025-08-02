// frontend/src/components/Navbar.jsx
import React from 'react';
import { NavLink, Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">VoiceGenie</Link>
      <div className="nav-links">
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/agents">Agents</NavLink>
        <NavLink to="/campaigns">Campaigns</NavLink>
      </div>
    </nav>
  );
};

export default Navbar;