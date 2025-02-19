/*
-----------------------------------------------------------------------------------------
  Step 1: Mock the fetch function
-----------------------------------------------------------------------------------------
*/
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import Home from '../Home';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Home Component', () => {
  const mockCountries = [
    {
      cca2: 'US',
      name: 'United States',
      flag: 'us-flag-url'
    },
    {
      cca2: 'CA',
      name: 'Canada',
      flag: 'canada-flag-url'
    }
  ];

  beforeEach(() => {
    // Mock fetch API
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockCountries)
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Rendering', () => {
    test('shows loading state initially', () => {
      renderWithRouter(<Home />);
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    test('displays header text', async () => {
      renderWithRouter(<Home />);
      await waitFor(() => {
        expect(screen.getByText('Flag Explorer App')).toBeInTheDocument();
      });
    });
  });

  describe('API Integration', () => {
    test('fetches and displays countries', async () => {
      renderWithRouter(<Home />);
      
      await waitFor(() => {
        expect(screen.getAllByRole('img')).toHaveLength(2);
      });

      expect(screen.getByAlt('United States')).toBeInTheDocument();
      expect(screen.getByAlt('Canada')).toBeInTheDocument();
    });

    test('handles API error correctly', async () => {
      global.fetch.mockImplementationOnce(() => 
        Promise.reject(new Error('API Error'))
      );

      renderWithRouter(<Home />);
      
      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    test('contains correct navigation links', async () => {
      renderWithRouter(<Home />);
      
      await waitFor(() => {
        const links = screen.getAllByRole('link');
        expect(links).toHaveLength(2);
        expect(links[0]).toHaveAttribute('href', '/country/United States');
      });
    });
  });
});