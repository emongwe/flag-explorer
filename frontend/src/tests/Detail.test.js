import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import Detail from '../Detail';

const mockCountryDetails = {
  name: 'United States',
  population: '331,002,651',
  capital: 'Washington, D.C.',
  flag: 'us-flag-url'
};

// Helper function to render component with router
const renderWithRouter = (countryName = 'United States') => {
  return render(
    <MemoryRouter initialEntries={[`/country/${countryName}`]}>
      <Routes>
        <Route path="/country/:countryName" element={<Detail />} />
      </Routes>
    </MemoryRouter>
  );
};

describe('Detail Component', () => {
  beforeEach(() => {
    // Mock fetch API
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockCountryDetails)
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Rendering', () => {
    test('shows loading state initially', () => {
      renderWithRouter();
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    test('displays country details after loading', async () => {
      renderWithRouter();
      
      await waitFor(() => {
        expect(screen.getByText('United States')).toBeInTheDocument();
        expect(screen.getByText(/population:/i)).toBeInTheDocument();
        expect(screen.getByText(/capital:/i)).toBeInTheDocument();
      });
    });
  });

  describe('API Integration', () => {
    test('calls API with correct country name', async () => {
      renderWithRouter('Canada');
      
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/countries/Canada')
      );
    });

    test('handles API error correctly', async () => {
      global.fetch.mockImplementationOnce(() => 
        Promise.reject(new Error('API Error'))
      );

      renderWithRouter();
      
      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    test('back button returns to previous page', async () => {
      const mockHistoryBack = jest.fn();
      window.history.back = mockHistoryBack;

      renderWithRouter();
      
      await waitFor(() => {
        const backButton = screen.getByText(/go back/i);
        userEvent.click(backButton);
        expect(mockHistoryBack).toHaveBeenCalled();
      });
    });
  });

  describe('Error States', () => {
    test('handles missing country details', async () => {
      global.fetch.mockImplementationOnce(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(null)
        })
      );

      renderWithRouter();
      
      await waitFor(() => {
        expect(screen.getByText(/country details not found/i)).toBeInTheDocument();
      });
    });
  });
});