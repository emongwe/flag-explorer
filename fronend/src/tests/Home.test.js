import { render, screen, waitFor } from '@testing-library/react';
import Home from '../Home';

describe('Home Component', () => {
  it('fetches and displays country flags', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve([{ name: {common: 'USA'}, flags: { png: 'url' } }]),
        ok: true,
      })
    );

    render(<Home />);

    // Wait for the data to load
    await waitFor(() => expect(screen.getByRole('img')).toBeInTheDocument());

    expect(screen.getByRole('img')).toHaveAttribute('src', 'url');
    expect(screen.getByText('USA')).toBeInTheDocument();
  });
});