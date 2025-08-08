// frontend/src/App.jsx
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
// import ScrollToTop from './components/common/ScrollToTop'; // Optional utility

function App() {
  return (
    <div className="app-container">
      {/* Global Navbar */}
      <Navbar />

      {/* Optional ScrollToTop for route changes */}
      {/* <ScrollToTop /> */}

      {/* Main Content */}
      <main className="main-content" role="main">
        <Outlet />
      </main>

      {/* Optional Footer */}
      {/* <footer className="footer">© 2025 Your Company</footer> */}
    </div>
  );
}

export default App;
