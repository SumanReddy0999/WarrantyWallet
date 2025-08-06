
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Shield } from 'lucide-react';

/**
 * Navigation.tsx
 *
 * Main navigation bar for the Warranty Wallet web client.
 * - Uses a config array for navigation links for maintainability.
 * - Handles custom home navigation to reset URL params.
 * - Includes ARIA attributes for accessibility.
 */
// Navigation link config for maintainability
const navLinks: Array<{ label: string; to: string }> = [
  { label: 'Home', to: '/' },
  { label: 'Services', to: '/services' },
  { label: 'FAQs', to: '/faqs' },
  { label: 'Contact', to: '/contact' },
];

export const Navigation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Custom home navigation to reset URL params if already on home
  const handleHomeClick = () => {
    if (location.pathname === '/') {
      navigate('/', { replace: true });
    } else {
      navigate('/');
    }
  };

  return (
    <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            onClick={handleHomeClick}
            className="flex items-center space-x-2 cursor-pointer"
            role="button"
            aria-label="Go to home page"
            tabIndex={0}
            onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleHomeClick(); }}
          >
            <Shield className="h-8 w-8 text-blue-600" aria-hidden="true" />
            <span className="text-xl font-bold text-gray-900">Warranty Wallet</span>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8" role="navigation" aria-label="Main navigation">
            {navLinks.map(link =>
              link.label === 'Home' ? (
                <div
                  key={link.label}
                  onClick={handleHomeClick}
                  className={`text-gray-700 hover:text-blue-600 transition-colors cursor-pointer ${
                    location.pathname === link.to ? 'text-blue-600 font-medium' : ''
                  }`}
                  role="link"
                  aria-current={location.pathname === link.to ? 'page' : undefined}
                  tabIndex={0}
                  onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleHomeClick(); }}
                >
                  {link.label}
                </div>
              ) : (
                <Link
                  key={link.label}
                  to={link.to}
                  className={`text-gray-700 hover:text-blue-600 transition-colors ${
                    location.pathname === link.to ? 'text-blue-600 font-medium' : ''
                  }`}
                  aria-current={location.pathname === link.to ? 'page' : undefined}
                >
                  {link.label}
                </Link>
              )
            )}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            <Link to="/login">
              <Button variant="outline" className="hover:bg-blue-50">
                Login
              </Button>
            </Link>
            <Link to="/signup">
              <Button className="bg-blue-600 hover:bg-blue-700">
                Sign Up
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};
