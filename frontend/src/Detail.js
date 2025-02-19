/*
---------------------------------------------DETAIL COMPONENT------------------------------------------------
1. This component is responsible for displaying the details of a country.
2. It fetches the details of a country from the API using the country name as a parameter.
3. The country name is extracted from the URL using the useParams hook from react-router-dom.
4. The useEffect hook is used to fetch the country details when the component is mounted.
5. The loading and error states are used to handle the loading and error states of the API request.
6. The country details are displayed when the API request is successful.
7. The Go Back button is used to navigate back to the home page.
8. The Detail component is exported as the default export.
9. The Detail component is imported in the App component and rendered when the user clicks on a flag.
10. The Detail component is a functional component that uses the useState and useEffect hooks to manage the
state and side effects.
11. The Detail component uses the useParams hook to extract the country name from the URL.
12. The country details are fetched from the API using the country name as a parameter.
13. The country details are displayed when the API request is successful.
--------------------------------------------------------------------------------------------------------------
*/
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Detail() {
  const { countryName } = useParams();
  const [countryDetails, setCountryDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    fetch(`${API_URL}/countries/${countryName}`) // Country API endpoint
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
      <div className="country-header">
          <h1>Country Details</h1>
      </div>
      <div className='country-details'>
        <h1>{countryDetails.name}</h1>
        <p>Population: {countryDetails.population}</p>
        <p>Capital: {countryDetails.capital}</p>
        <button onClick={() => window.history.back()}>Go Back</button>
      </div>
    </div>
  );
}

export default Detail;