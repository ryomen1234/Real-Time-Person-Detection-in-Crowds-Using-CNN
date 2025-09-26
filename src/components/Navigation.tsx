import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { LogOut, Users, BookOpen, Camera, Eye, ClipboardList, GraduationCap } from 'lucide-react';

export const Navigation: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  if (!user) return null;

  const isActive = (path: string) => location.pathname === path;

  const getRoleLinks = () => {
    switch (user.role) {
      case 'admin':
        return (
          <>
            <Link to="/admin/users">
              <Button 
                variant={isActive('/admin/users') ? 'default' : 'ghost'} 
                size="sm"
                className="flex items-center gap-2"
              >
                <Users className="h-4 w-4" />
                Users
              </Button>
            </Link>
            <Link to="/admin/subjects">
              <Button 
                variant={isActive('/admin/subjects') ? 'default' : 'ghost'} 
                size="sm"
                className="flex items-center gap-2"
              >
                <BookOpen className="h-4 w-4" />
                Subjects
              </Button>
            </Link>
          </>
        );
      case 'teacher':
        return (
          <>
            <Link to="/teacher/attendance/take">
              <Button 
                variant={isActive('/teacher/attendance/take') ? 'default' : 'ghost'} 
                size="sm"
                className="flex items-center gap-2"
              >
                <Camera className="h-4 w-4" />
                Take Attendance
              </Button>
            </Link>
            <Link to="/teacher/attendance/view">
              <Button 
                variant={isActive('/teacher/attendance/view') ? 'default' : 'ghost'} 
                size="sm"
                className="flex items-center gap-2"
              >
                <Eye className="h-4 w-4" />
                View Attendance
              </Button>
            </Link>
          </>
        );
      case 'student':
        return (
          <Link to="/student/attendance">
            <Button 
              variant={isActive('/student/attendance') ? 'default' : 'ghost'} 
              size="sm"
              className="flex items-center gap-2"
            >
              <ClipboardList className="h-4 w-4" />
              My Attendance
            </Button>
          </Link>
        );
      default:
        return null;
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-card border-b border-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <Link to="/dashboard" className="flex items-center gap-2">
            <GraduationCap className="h-8 w-8 text-primary" />
            <span className="text-xl font-semibold text-foreground">
              Attendance System
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-4">
            <Link to="/dashboard">
              <Button 
                variant={isActive('/dashboard') ? 'default' : 'ghost'} 
                size="sm"
              >
                Dashboard
              </Button>
            </Link>
            
            {getRoleLinks()}

            {/* User Info & Logout */}
            <div className="flex items-center gap-3 ml-6 pl-6 border-l border-border">
              <div className="text-sm">
                <div className="font-medium text-foreground">{user.name}</div>
                <div className="text-muted-foreground capitalize">{user.role}</div>
              </div>
              <Button 
                variant="outline" 
                size="sm"
                onClick={logout}
                className="flex items-center gap-2"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};