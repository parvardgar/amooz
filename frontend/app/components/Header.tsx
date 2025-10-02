'use client';

import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const { user, logout } = useAuth();

  const handleLoginClick = () => {
    setAuthMode('login');
    setAuthModalOpen(true);
  };

  const handleSignupClick = () => {
    setAuthMode('signup');
    setAuthModalOpen(true);
  };

  const handleLogout = () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      logout(token);
    } else {
      // If no token found, still clear local storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_data');
    }
    setIsMenuOpen(false);
  };

  const closeAuthModal = () => {
    setAuthModalOpen(false);
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl font-bold text-blue-600">LearnHub</span>
              </div>
              <nav className="hidden md:ml-6 md:flex md:space-x-8">
                <a href="#" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium">
                  Explore
                </a>
                <a href="#" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium">
                  Search
                </a>
              </nav>
            </div>

            {/* Right side buttons */}
            <div className="hidden md:flex items-center space-x-4">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                Donate
              </button>
              
              {user ? (
                <div className="flex items-center space-x-4">
                  <span className="text-gray-700">Hello, {user.mobile}</span>
                  <button 
                    onClick={handleLogout}
                    className="text-blue-600 border border-blue-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-50 transition-colors"
                  >
                    Log out
                  </button>
                </div>
              ) : (
                <>
                  <button 
                    onClick={handleLoginClick}
                    className="text-blue-600 border border-blue-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-50 transition-colors"
                  >
                    Log in
                  </button>
                  <button 
                    onClick={handleSignupClick}
                    className="text-blue-600 border border-blue-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-50 transition-colors"
                  >
                    Sign up
                  </button>
                </>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 p-2 rounded-md"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                <a href="#" className="text-gray-900 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md">
                  Explore
                </a>
                <a href="#" className="text-gray-900 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md">
                  Search
                </a>
                <div className="pt-4 pb-3 border-t border-gray-200 space-y-1">
                  <button className="w-full text-left text-blue-600 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md">
                    Donate
                  </button>
                  
                  {user ? (
                    <>
                      <div className="px-3 py-2 text-sm text-gray-900">
                        Hello, {user.mobile}
                      </div>
                      <button 
                        onClick={handleLogout}
                        className="w-full text-left text-blue-600 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md"
                      >
                        Log out
                      </button>
                    </>
                  ) : (
                    <>
                      <button 
                        onClick={handleLoginClick}
                        className="w-full text-left text-blue-600 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md"
                      >
                        Log in
                      </button>
                      <button 
                        onClick={handleSignupClick}
                        className="w-full text-left text-blue-600 block px-3 py-2 text-base font-medium hover:bg-gray-50 rounded-md"
                      >
                        Sign up
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </header>

      <AuthModal 
        isOpen={authModalOpen}
        onClose={closeAuthModal}
        mode={authMode}
      />
    </>
  );
}