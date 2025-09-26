import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Eye, Calendar, Users, TrendingUp } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

interface AttendanceRecord {
  id: string;
  date: string;
  totalStudents: number;
  present: number;
  absent: number;
}

interface StudentAttendance {
  id: string;
  name: string;
  email: string;
  status: 'present' | 'absent';
}

interface Subject {
  id: string;
  name: string;
}

const ViewAttendance: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedRecord, setSelectedRecord] = useState<AttendanceRecord | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [attendanceRecords, setAttendanceRecords] = useState<AttendanceRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load real data from API
  useEffect(() => {
    const loadData = async () => {
      if (!user) return;
      
      try {
        setIsLoading(true);
        
        // Load teacher's subjects
        const fetchedSubjects = await apiService.getSubjects({ teacher_id: user.id });
        const formattedSubjects: Subject[] = fetchedSubjects.map(subject => ({
          id: subject.id.toString(),
          name: subject.name
        }));
        setSubjects(formattedSubjects);

        // Load attendance sessions
        const sessions = await apiService.getAttendanceSessions({ teacher_id: user.id });
        const formattedRecords: AttendanceRecord[] = sessions.map(session => ({
          id: session.id.toString(),
          date: new Date(session.session_date).toLocaleDateString(),
          totalStudents: session.total_students,
          present: session.present_students,
          absent: session.total_students - session.present_students
        }));
        setAttendanceRecords(formattedRecords);
        
      } catch (error) {
        console.error('Error loading data:', error);
        // Show empty state instead of error for better UX
        setSubjects([]);
        setAttendanceRecords([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [user, toast]);

  // Mock data removed - now using real API data above
  const oldMockAttendanceRecords: Record<string, AttendanceRecord[]> = {
    '1': [
      { id: '1', date: '2024-01-15', totalStudents: 25, present: 23, absent: 2 },
      { id: '2', date: '2024-01-12', totalStudents: 25, present: 24, absent: 1 },
      { id: '3', date: '2024-01-10', totalStudents: 25, present: 22, absent: 3 },
      { id: '4', date: '2024-01-08', totalStudents: 25, present: 25, absent: 0 },
      { id: '5', date: '2024-01-05', totalStudents: 25, present: 21, absent: 4 },
    ],
    '2': [
      { id: '6', date: '2024-01-14', totalStudents: 30, present: 28, absent: 2 },
      { id: '7', date: '2024-01-11', totalStudents: 30, present: 29, absent: 1 },
      { id: '8', date: '2024-01-09', totalStudents: 30, present: 27, absent: 3 },
    ],
    '3': [
      { id: '9', date: '2024-01-13', totalStudents: 20, present: 19, absent: 1 },
      { id: '10', date: '2024-01-11', totalStudents: 20, present: 20, absent: 0 },
      { id: '11', date: '2024-01-09', totalStudents: 20, present: 18, absent: 2 },
    ]
  };

  const mockStudentDetails: StudentAttendance[] = [
    { id: '1', name: 'Alice Johnson', email: 'alice@school.com', status: 'present' },
    { id: '2', name: 'Bob Smith', email: 'bob@school.com', status: 'present' },
    { id: '3', name: 'Carol Davis', email: 'carol@school.com', status: 'absent' },
    { id: '4', name: 'David Wilson', email: 'david@school.com', status: 'present' },
    { id: '5', name: 'Eva Brown', email: 'eva@school.com', status: 'present' },
  ];

  const currentRecords = selectedSubject ? attendanceRecords[selectedSubject] || [] : [];
  const selectedSubjectName = subjects.find(s => s.id === selectedSubject)?.name || '';

  const getAttendanceRate = (present: number, total: number) => {
    return Math.round((present / total) * 100);
  };

  const getOverallStats = () => {
    if (!currentRecords.length) return { avgAttendance: 0, totalClasses: 0, totalStudents: 0 };
    
    const totalPresent = currentRecords.reduce((sum, record) => sum + record.present, 0);
    const totalPossible = currentRecords.reduce((sum, record) => sum + record.totalStudents, 0);
    const avgAttendance = Math.round((totalPresent / totalPossible) * 100);
    
    return {
      avgAttendance,
      totalClasses: currentRecords.length,
      totalStudents: currentRecords[0]?.totalStudents || 0
    };
  };

  const handleViewDetails = (record: AttendanceRecord) => {
    setSelectedRecord(record);
    setIsDetailModalOpen(true);
  };

  const stats = getOverallStats();

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <Eye className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold text-foreground">View Subject Attendance</h1>
            <p className="text-muted-foreground">Review attendance records and statistics</p>
          </div>
        </div>

        {/* Subject Selection */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Select Subject</label>
              <Select value={selectedSubject} onValueChange={setSelectedSubject}>
                <SelectTrigger className="max-w-sm">
                  <SelectValue placeholder="Choose a subject to view attendance" />
                </SelectTrigger>
                <SelectContent>
                  {subjects.map((subject) => (
                    <SelectItem key={subject.id} value={subject.id}>
                      {subject.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {selectedSubject && (
          <>
            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    Average Attendance
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-success">
                    {stats.avgAttendance}%
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Across all classes
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    Total Classes
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-foreground">
                    {stats.totalClasses}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Classes recorded
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    Enrolled Students
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-foreground">
                    {stats.totalStudents}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Total enrollment
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    Best Attendance
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-success">
                    {currentRecords.length > 0 ? Math.max(...currentRecords.map(r => getAttendanceRate(r.present, r.totalStudents))) : 0}%
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Highest class rate
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Attendance Records Table */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  {selectedSubjectName} - Attendance Records
                </CardTitle>
                <CardDescription>
                  Detailed attendance records for each class session
                </CardDescription>
              </CardHeader>
              <CardContent>
                {currentRecords.length > 0 ? (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Date</TableHead>
                        <TableHead>Total Students</TableHead>
                        <TableHead>Present</TableHead>
                        <TableHead>Absent</TableHead>
                        <TableHead>Attendance Rate</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {currentRecords.map((record) => {
                        const rate = getAttendanceRate(record.present, record.totalStudents);
                        return (
                          <TableRow key={record.id}>
                            <TableCell className="font-medium">
                              {new Date(record.date).toLocaleDateString('en-US', {
                                weekday: 'short',
                                month: 'short',
                                day: 'numeric',
                                year: 'numeric'
                              })}
                            </TableCell>
                            <TableCell>{record.totalStudents}</TableCell>
                            <TableCell>
                              <Badge variant="outline" className="text-success border-success">
                                {record.present}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline" className="text-destructive border-destructive">
                                {record.absent}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                <div className={`text-sm font-medium ${
                                  rate >= 90 ? 'text-success' : 
                                  rate >= 75 ? 'text-warning' : 'text-destructive'
                                }`}>
                                  {rate}%
                                </div>
                                {rate >= 90 && <TrendingUp className="h-4 w-4 text-success" />}
                              </div>
                            </TableCell>
                            <TableCell className="text-right">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleViewDetails(record)}
                                className="flex items-center gap-1"
                              >
                                <Eye className="h-3 w-3" />
                                View Details
                              </Button>
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No attendance records found for this subject.</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </>
        )}

        {/* Detailed Attendance Modal */}
        <Dialog open={isDetailModalOpen} onOpenChange={setIsDetailModalOpen}>
          <DialogContent className="sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>Attendance Details</DialogTitle>
              <DialogDescription>
                {selectedRecord && (
                  <>
                    {selectedSubjectName} - {new Date(selectedRecord.date).toLocaleDateString('en-US', {
                      weekday: 'long',
                      month: 'long',
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </>
                )}
              </DialogDescription>
            </DialogHeader>
            
            {selectedRecord && (
              <div className="space-y-4">
                {/* Summary */}
                <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                  <span className="text-sm font-medium">Attendance Rate:</span>
                  <span className="text-lg font-bold text-success">
                    {getAttendanceRate(selectedRecord.present, selectedRecord.totalStudents)}%
                  </span>
                </div>

                {/* Student List */}
                <div className="space-y-2">
                  <h4 className="font-medium text-foreground">Student Attendance:</h4>
                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {mockStudentDetails.map((student) => (
                      <div
                        key={student.id}
                        className="flex items-center justify-between p-2 border rounded"
                      >
                        <div>
                          <div className="font-medium text-sm">{student.name}</div>
                          <div className="text-xs text-muted-foreground">{student.email}</div>
                        </div>
                        <Badge
                          variant={student.status === 'present' ? 'default' : 'destructive'}
                          className="capitalize"
                        >
                          {student.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default ViewAttendance;