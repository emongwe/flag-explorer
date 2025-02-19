/*
----------------------------------------------HOME COMPONENT------------------------------------------------------
  Step 1: Import React, useState, useEffect, and Link from react-router-dom
  Step 2: Create a functional component named Home
  Step 3: Define the countries, loading, and error states using the useState hook
  Step 4: Define the API_URL constant with the API endpoint URL
  Step 5: Use the useEffect hook to fetch the list of countries from the API
  Step 6: Handle loading and error states for the API request
  Step 7: Render the list of countries as links to the detail page
  Step 8: Export the Home component as the default export
  Step 9: The Home component is responsible for displaying the list of countries as flags.
  Step 10: The Home component fetches the list of countries from the API using the useEffect hook.
  Step 11: The loading and error states are used to handle the loading and error states of the API request.
  Step 12: The list of countries is displayed as links to the detail page when the API request is successful.
-----------------------------------------------------------------------------------------------------------------
*/
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    fetch(`${API_URL}/countries`) // Country API endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json()
      })
      .then(data => setCountries(data))
      .catch(error => setError(error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <div className="country-header">
          <h1>Flag Explorer App</h1>
      </div>
      <div className="country-grid">
            {countries.map(country => (
                <Link key={country.cca2} className="country-item" to={`/country/${country.name}`}>
                <img src={country.flag} alt={country.name} />
                </Link>
            ))}
        </div>
    </div>
  );
}

export default Home;