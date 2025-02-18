import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://restcountries.com/v3.1/all')
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
                <Link key={country.cca2} className="country-item" to={`/country/${country.name.common}`}>
                <img src={country.flags.png} alt={country.name.common} />
                </Link>
            ))}
        </div>
    </div>
  );
}

export default Home;