
import { Link, useLocation } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Shield } from 'lucide-react';

export const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Shield className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">Warranty Wallet</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/" 
              className={`text-gray-700 hover:text-blue-600 transition-colors ${
                location.pathname === '/' ? 'text-blue-600 font-medium' : ''
              }`}
            >
              Home
            </Link>
            <Link 
              to="/services" 
              className={`text-gray-700 hover:text-blue-600 transition-colors ${
                location.pathname === '/services' ? 'text-blue-600 font-medium' : ''
              }`}
            >
              Services
            </Link>
            <Link 
              to="/faqs" 
              className={`text-gray-700 hover:text-blue-600 transition-colors ${
                location.pathname === '/faqs' ? 'text-blue-600 font-medium' : ''
              }`}
            >
              FAQs
            </Link>
            <Link 
              to="/contact" 
              className={`text-gray-700 hover:text-blue-600 transition-colors ${
                location.pathname === '/contact' ? 'text-blue-600 font-medium' : ''
              }`}
            >
              Contact
            </Link>
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
