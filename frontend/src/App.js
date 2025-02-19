/*
-----------------------------------------------APP COMPONENT-------------------------------------------------------
  Step 1: Install react-router-dom
  Step 2: Import BrowserRouter as Router, Routes, and Route from react-router-dom
  Step 3: Import Home and Detail components
  Step 4: Create a functional component named App
  Step 5: Render the Home component for the root URL
  Step 6: Render the Detail component for the /country/:countryName URL
  Step 7: Export the App component as the default export
  Step 8: The App component is responsible for routing between the Home and Detail components.
  Step 9: The App component uses the BrowserRouter, Routes, and Route components from react-router-dom.
  Step 10: The Home component is rendered for the root URL, and the Detail component is rendered for 
  the /country/:countryName URL.
  Step 11: The App component is the entry point of the application and is imported in the index.js file.
------------------------------------------------------------------------------------------------------------------
*/

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import Detail from './Detail';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/country/:countryName" element={<Detail />} />
      </Routes>
    </Router>
  );
}

export default App;