/*
-----------------------------------------------------------------------------------------
  Step 1: Importing required modules and components
-----------------------------------------------------------------------------------------
*/
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

// Helper function to render with router
const renderWithRouter = (route = '/') => {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <App />
    </MemoryRouter>
  );
};

describe('App Component', () => {
  describe('Routing', () => {
    test('renders Home component for root path', () => {
      renderWithRouter('/');
      expect(screen.getByRole('main')).toBeInTheDocument();
    });

    test('renders Detail component for country route', () => {
      renderWithRouter('/country/USA');
      expect(screen.getByRole('article')).toBeInTheDocument();
    });

    test('handles 404 for invalid routes', () => {
      renderWithRouter('/invalid-route');
      expect(screen.getByText(/not found/i)).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    test('allows navigation between routes', async () => {
      renderWithRouter('/');
      const link = screen.getByRole('link', { name: /usa/i });
      userEvent.click(link);
      expect(await screen.findByRole('article')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    test('renders error boundary for component crashes', () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      renderWithRouter('/error-route');
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
      consoleSpy.mockRestore();
    });
  });
});