import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Progress } from '@/components/ui/progress';
import { ClipboardList, BookOpen, TrendingUp, TrendingDown, Calendar, CheckCircle, XCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

interface SubjectAttendance {
  id: string;
  name: string;
  totalClasses: number;
  attendedClasses: number;
  percentage: number;
  status: 'excellent' | 'good' | 'warning' | 'critical';
}

interface AttendanceDetail {
  id: string;
  date: string;
  status: 'present' | 'absent';
  classType: 'lecture' | 'lab' | 'tutorial';
}

const StudentAttendance: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [selectedSubject, setSelectedSubject] = useState<SubjectAttendance | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [subjectAttendance, setSubjectAttendance] = useState<SubjectAttendance[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load real attendance data from API
  useEffect(() => {
    const loadAttendanceData = async () => {
      if (!user) return;
      
      try {
        setIsLoading(true);
        const attendanceData = await apiService.getStudentAttendance(user.id);
        
        // Convert API data to component format
        const formattedData: SubjectAttendance[] = attendanceData.subjects.map(subject => ({
          id: subject.subject_id.toString(),
          name: subject.subject_name,
          totalClasses: subject.total_classes,
          attendedClasses: subject.attended_classes,
          percentage: Math.round(subject.attendance_percentage),
          status: subject.attendance_percentage >= 85 ? 'excellent' : 
                 subject.attendance_percentage >= 75 ? 'good' :
                 subject.attendance_percentage >= 65 ? 'warning' : 'critical'
        }));
        
        setSubjectAttendance(formattedData);
      } catch (error) {
        console.error('Error loading attendance data:', error);
        // Fallback to empty data if API fails
        setSubjectAttendance([]);
        toast({
          title: "Info",
          description: "No attendance data available yet. Attendance will appear after teachers start taking attendance.",
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadAttendanceData();
  }, [user, toast]);

  // If loading, show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto p-6">
          <div className="flex items-center gap-3 mb-6">
            <ClipboardList className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-3xl font-bold text-foreground">My Attendance Records</h1>
              <p className="text-muted-foreground">Loading your attendance data...</p>
            </div>
          </div>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Loading attendance data...</p>
          </div>
        </div>
      </div>
    );
  }

  // Mock data replaced with real API data above
  const mockData: SubjectAttendance[] = [
    {
      id: '1',
      name: 'Mathematics',
      totalClasses: 20,
      attendedClasses: 18,
      percentage: 90,
      status: 'excellent'
    },
    {
      id: '2',
      name: 'Physics',
      totalClasses: 18,
      attendedClasses: 15,
      percentage: 83,
      status: 'good'
    },
    {
      id: '3',
      name: 'Computer Science',
      totalClasses: 22,
      attendedClasses: 16,
      percentage: 73,
      status: 'warning'
    },
    {
      id: '4',
      name: 'Chemistry',
      totalClasses: 16,
      attendedClasses: 10,
      percentage: 63,
      status: 'critical'
    },
    {
      id: '5',
      name: 'English Literature',
      totalClasses: 14,
      attendedClasses: 13,
      percentage: 93,
      status: 'excellent'
    },
    {
      id: '6',
      name: 'History',
      totalClasses: 12,
      attendedClasses: 11,
      percentage: 92,
      status: 'excellent'
    },
    {
      id: '7',
      name: 'Biology',
      totalClasses: 19,
      attendedClasses: 14,
      percentage: 74,
      status: 'warning'
    },
    {
      id: '8',
      name: 'Economics',
      totalClasses: 15,
      attendedClasses: 12,
      percentage: 80,
      status: 'good'
    }
  ];

  // Mock detailed attendance for selected subject
  const attendanceDetails: AttendanceDetail[] = [
    { id: '1', date: '2024-01-15', status: 'present', classType: 'lecture' },
    { id: '2', date: '2024-01-12', status: 'present', classType: 'lab' },
    { id: '3', date: '2024-01-10', status: 'absent', classType: 'lecture' },
    { id: '4', date: '2024-01-08', status: 'present', classType: 'tutorial' },
    { id: '5', date: '2024-01-05', status: 'present', classType: 'lecture' },
    { id: '6', date: '2024-01-03', status: 'present', classType: 'lab' },
    { id: '7', date: '2024-01-01', status: 'absent', classType: 'lecture' },
  ];

  const overallStats = {
    totalSubjects: subjectAttendance.length,
    averageAttendance: Math.round(
      subjectAttendance.reduce((sum, subject) => sum + subject.percentage, 0) / subjectAttendance.length
    ),
    totalClasses: subjectAttendance.reduce((sum, subject) => sum + subject.totalClasses, 0),
    totalAttended: subjectAttendance.reduce((sum, subject) => sum + subject.attendedClasses, 0)
  };

  const getStatusColor = (status: SubjectAttendance['status']) => {
    switch (status) {
      case 'excellent':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'good':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'critical':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusIcon = (status: SubjectAttendance['status']) => {
    switch (status) {
      case 'excellent':
      case 'good':
        return <TrendingUp className="h-4 w-4" />;
      case 'warning':
      case 'critical':
        return <TrendingDown className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const handleViewDetails = (subject: SubjectAttendance) => {
    setSelectedSubject(subject);
    setIsDetailModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <ClipboardList className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold text-foreground">My Attendance Records</h1>
            <p className="text-muted-foreground">Track your attendance across all enrolled subjects</p>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Overall Attendance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground mb-1">
                {overallStats.averageAttendance}%
              </div>
              <Progress value={overallStats.averageAttendance} className="h-2" />
              <p className="text-xs text-muted-foreground mt-1">
                Across all subjects
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Enrolled Subjects
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">
                {overallStats.totalSubjects}
              </div>
              <p className="text-xs text-muted-foreground">
                Active this semester
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Classes Attended
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-success">
                {overallStats.totalAttended}
              </div>
              <p className="text-xs text-muted-foreground">
                Out of {overallStats.totalClasses} total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${
                overallStats.averageAttendance >= 85 ? 'text-success' : 
                overallStats.averageAttendance >= 75 ? 'text-warning' : 'text-destructive'
              }`}>
                {overallStats.averageAttendance >= 85 ? 'Good' : 
                 overallStats.averageAttendance >= 75 ? 'Warning' : 'Critical'}
              </div>
              <p className="text-xs text-muted-foreground">
                Academic standing
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Subject Attendance Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {subjectAttendance.map((subject) => (
            <Card key={subject.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <BookOpen className="h-5 w-5 text-primary" />
                  <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(subject.status)}`}>
                    {getStatusIcon(subject.status)}
                    {subject.status}
                  </div>
                </div>
                <CardTitle className="text-lg">{subject.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Attendance Rate</span>
                    <span className="font-medium">{subject.percentage}%</span>
                  </div>
                  
                  <Progress value={subject.percentage} className="h-2" />
                  
                  <div className="flex justify-between text-sm text-muted-foreground">
                    <span>{subject.attendedClasses} attended</span>
                    <span>{subject.totalClasses} total</span>
                  </div>
                  
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full"
                    onClick={() => handleViewDetails(subject)}
                  >
                    View Details
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Detailed Attendance Modal */}
        <Dialog open={isDetailModalOpen} onOpenChange={setIsDetailModalOpen}>
          <DialogContent className="sm:max-w-2xl">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                {selectedSubject?.name} - Detailed Attendance
              </DialogTitle>
              <DialogDescription>
                Your attendance record for this subject
              </DialogDescription>
            </DialogHeader>
            
            {selectedSubject && (
              <div className="space-y-4">
                {/* Summary */}
                <div className="grid grid-cols-3 gap-4 p-4 bg-muted rounded-lg">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-foreground">{selectedSubject.percentage}%</div>
                    <div className="text-xs text-muted-foreground">Attendance Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-success">{selectedSubject.attendedClasses}</div>
                    <div className="text-xs text-muted-foreground">Classes Attended</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-destructive">{selectedSubject.totalClasses - selectedSubject.attendedClasses}</div>
                    <div className="text-xs text-muted-foreground">Classes Missed</div>
                  </div>
                </div>

                {/* Attendance Details Table */}
                <div className="max-h-64 overflow-y-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Date</TableHead>
                        <TableHead>Class Type</TableHead>
                        <TableHead>Status</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {attendanceDetails.map((detail) => (
                        <TableRow key={detail.id}>
                          <TableCell className="font-medium">
                            <div className="flex items-center gap-2">
                              <Calendar className="h-4 w-4 text-muted-foreground" />
                              {new Date(detail.date).toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                year: 'numeric'
                              })}
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="capitalize">
                              {detail.classType}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              {detail.status === 'present' ? (
                                <CheckCircle className="h-4 w-4 text-success" />
                              ) : (
                                <XCircle className="h-4 w-4 text-destructive" />
                              )}
                              <Badge
                                variant={detail.status === 'present' ? 'default' : 'destructive'}
                                className="capitalize"
                              >
                                {detail.status}
                              </Badge>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default StudentAttendance;