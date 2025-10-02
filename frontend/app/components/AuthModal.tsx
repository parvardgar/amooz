'use client';

import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'login' | 'signup';
}

type UserRole = 'learner' | 'teacher' | 'parent';

const roleMap: Record<UserRole, number> = {
  'learner': 0,
  'teacher': 2,
  'parent': 3
};

export default function AuthModal({ isOpen, onClose, mode }: AuthModalProps) {
  const [mobile, setMobile] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState<UserRole>('learner');
  const { login, signup, isLoading, error } = useAuth();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate passwords match for signup
    if (mode === 'signup' && password !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }

    try {
      if (mode === 'login') {
        await login(mobile, password);
      } else {
        await signup(mobile, roleMap[selectedRole], password, confirmPassword);
      }
      onClose();
      resetForm();
    } catch (err) {
      // Error is handled by the context
    }
  };

  const resetForm = () => {
    setMobile('');
    setPassword('');
    setConfirmPassword('');
    setSelectedRole('learner');
  };

  const switchToLogin = () => {
    resetForm();
    // You might want to add logic to switch to login mode
  };

  const roles: { id: UserRole; label: string; description: string }[] = [
    {
      id: 'learner',
      label: 'Learner',
      description: 'Start your learning journey'
    },
    {
      id: 'teacher',
      label: 'Teacher',
      description: 'Empower your classroom'
    },
    {
      id: 'parent',
      label: 'Parent',
      description: 'Support your child\'s learning'
    }
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-900">
            {mode === 'login' ? 'Log In' : 'Sign Up'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl"
          >
            ✕
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {mode === 'signup' && (
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Join LearnHub for free as a
            </h3>
            <div className="grid grid-cols-1 gap-3">
              {roles.map((role) => (
                <button
                  key={role.id}
                  type="button"
                  onClick={() => setSelectedRole(role.id)}
                  className={`p-4 border-2 rounded-lg text-left transition-colors ${
                    selectedRole === role.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-gray-900">{role.label}</div>
                  <div className="text-sm text-gray-600 mt-1">{role.description}</div>
                </button>
              ))}
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'signup' && (
            <div>
              <label htmlFor="mobile" className="block text-sm font-medium text-gray-700">
                Mobile Number
              </label>
              <input
                type="tel"
                id="mobile"
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                required
                placeholder="Enter your mobile number"
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          )}
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {mode === 'signup' && (
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              {password !== confirmPassword && confirmPassword && (
                <p className="text-red-500 text-sm mt-1">Passwords don't match</p>
              )}
            </div>
          )}
          
          <button
            type="submit"
            disabled={isLoading || (mode === 'signup' && password !== confirmPassword)}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 font-medium"
          >
            {isLoading ? 'Loading...' : mode === 'login' ? 'Log In' : `Join as ${selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)}`}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={switchToLogin}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {mode === 'login' 
              ? "Don't have an account? Sign up" 
              : "Already have an account? Log in"}
          </button>
        </div>
      </div>
    </div>
  );
}