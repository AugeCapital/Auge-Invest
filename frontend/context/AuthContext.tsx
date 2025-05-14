import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

// TODO: Move API base URL to an environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface User {
  id: number;
  email: string;
  full_name: string | null;
  // Add other user fields as needed from your User schema
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (accessToken: string) => Promise<void>;
  logout: () => void;
  // register: (userData: any) => Promise<void>; // Optional: if register also logs in or for unified API calls
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // To check initial auth status

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('authToken_auge_invest');
      if (storedToken) {
        await fetchUser(storedToken);
      }
      setIsLoading(false);
    };
    initializeAuth();
  }, []);

  const fetchUser = async (accessToken: string) => {
    try {
      const response = await axios.get(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setUser(response.data);
      setToken(accessToken);
      localStorage.setItem('authToken_auge_invest', accessToken);
    } catch (error) {
      console.error('Failed to fetch user with token:', error);
      logout(); // Clear token if fetching user fails
    }
  };

  const login = async (accessToken: string) => {
    setIsLoading(true);
    await fetchUser(accessToken);
    setIsLoading(false);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken_auge_invest');
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

