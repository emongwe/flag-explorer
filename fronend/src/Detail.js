import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Detail() {
  const { countryName } = useParams();
  const [countryDetails, setCountryDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    fetch(`${API_URL}/countries?name=${countryName}`) // Country API endpoint
      .then(res => res.json())
      .then(data => setCountryDetails(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [countryName]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    if (!countryDetails) return <div>Country details not found</div>;

  return (
    <div>
      <h1>{countryDetails.name}</h1>
      <p>Population: {countryDetails.population}</p>
      <p>Capital: {countryDetails.capital}</p>
    </div>
  );
}

export default Detail;