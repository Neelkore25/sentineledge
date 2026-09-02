'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type ViewMode = 'analyst' | 'executive';
type UserRole = 'Analyst' | 'Manager' | 'Viewer';
type ThemeMode = 'dark' | 'light';

interface AppContextType {
  theme: ThemeMode;
  setTheme: (t: ThemeMode) => void;
  toggleTheme: () => void;
  viewMode: ViewMode;
  setViewMode: (v: ViewMode) => void;
  userRole: UserRole;
  setUserRole: (r: UserRole) => void;
  isCmdOpen: boolean;
  setIsCmdOpen: (o: boolean) => void;
  refreshTrigger: number;
  triggerRefresh: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<ThemeMode>('dark');
  const [viewMode, setViewMode] = useState<ViewMode>('analyst');
  const [userRole, setUserRole] = useState<UserRole>('Analyst');
  const [isCmdOpen, setIsCmdOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  // Global Ctrl/Cmd + K shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCmdOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <AppContext.Provider
      value={{
        theme,
        setTheme,
        toggleTheme,
        viewMode,
        setViewMode,
        userRole,
        setUserRole,
        isCmdOpen,
        setIsCmdOpen,
        refreshTrigger,
        triggerRefresh
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
