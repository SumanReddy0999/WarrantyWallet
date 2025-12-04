
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Shield, LogOut, User } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "./ui/avatar";

/**
 * Navigation.tsx
 *
 * Main navigation bar for the Warranty Wallet web client.
 * - Uses a config array for navigation links for maintainability.
 * - Handles custom home navigation to reset URL params.
 * - Includes ARIA attributes for accessibility.
 */
// Base navigation links that are always visible
const baseNavLinks = [
  { label: 'Home', to: '/' },
  { label: 'Services', to: '/services' },
  { label: 'FAQs', to: '/faqs' },
  { label: 'Contact', to: '/contact' },
];

// Protected navigation links that require authentication
const protectedNavLinks = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'My Warranties', to: '/warranties' },
];

export const Navigation = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const isDashboard = location.pathname.startsWith('/dashboard');

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
            {/* Base navigation links */}
            {baseNavLinks.map(link =>
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
            
            {/* Protected navigation links - only show when user is logged in */}
            {user && protectedNavLinks.map(link => (
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
            ))}
          </div>

          {/* Auth Buttons - Show login/signup when not logged in, user menu when logged in */}
          <div className="flex items-center space-x-4">
            {!isDashboard && !user ? (
              <>
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
              </>
            ) : user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback>
                        {user.first_name?.[0] || user.email?.[0] || <User className="h-4 w-4" />}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {user.first_name} {user.last_name}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => navigate('/dashboard')}>
                    <User className="mr-2 h-4 w-4" />
                    <span>Dashboard</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => {
                    logout();
                    navigate('/');
                  }}>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : null}
          </div>
        </div>
      </div>
    </nav>
  );
};
