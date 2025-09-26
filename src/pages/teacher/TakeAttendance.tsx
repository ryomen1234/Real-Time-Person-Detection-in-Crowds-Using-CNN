import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { useToast } from '@/hooks/use-toast';
import { Camera, Upload, Users, Save, RotateCcw } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/services/api';

interface Student {
  id: string;
  name: string;
  email: string;
  isPresent: boolean;
}

interface Subject {
  id: string;
  name: string;
}

const TakeAttendance: React.FC = () => {
  const { toast } = useToast();
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [detectedStudents, setDetectedStudents] = useState<Student[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load real subjects from API
  useEffect(() => {
    const loadSubjects = async () => {
      try {
        setIsLoading(true);
        const fetchedSubjects = await apiService.getSubjects({ teacher_id: user?.id });
        const formattedSubjects: Subject[] = fetchedSubjects.map(subject => ({
          id: subject.id.toString(),
          name: subject.name
        }));
        setSubjects(formattedSubjects);
      } catch (error) {
        console.error('Error loading subjects:', error);
        toast({
          title: "Error",
          description: "Failed to load subjects. Please try again.",
          variant: "destructive"
        });
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      loadSubjects();
    }
  }, [user, toast]);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleWebcamCapture = () => {
    toast({
      title: "Webcam Feature",
      description: "Webcam integration would be implemented here in a real application",
    });
  };

  const processAttendance = async () => {
    if (!selectedSubject || !selectedImage) {
      toast({
        title: "Missing Information",
        description: "Please select a subject and upload/capture an image",
        variant: "destructive"
      });
      return;
    }

    setIsProcessing(true);

    try {
      // Step 1: Create attendance session
      const session = await apiService.createAttendanceSession({
        subject_id: parseInt(selectedSubject),
        session_date: new Date().toISOString(),
        class_type: 'lecture',
        notes: 'Attendance taken via photo recognition'
      });

      // Step 2: Upload image and process
      const result = await apiService.uploadAttendanceImage(session.id, selectedImage);
      
      // Step 3: Format detected students
      const formattedStudents: Student[] = result.detected_students.map(student => ({
        id: student.student_id.toString(),
        name: student.name,
        email: student.email,
        isPresent: student.detected
      }));

      setDetectedStudents(formattedStudents);
      setShowResults(true);

      toast({
        title: "Processing Complete",
        description: `Detected ${result.total_detected} students present`,
      });
    } catch (error) {
      console.error('Error processing attendance:', error);
      toast({
        title: "Error",
        description: "Failed to process attendance. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleStudentPresence = (studentId: string) => {
    setDetectedStudents(students =>
      students.map(student =>
        student.id === studentId
          ? { ...student, isPresent: !student.isPresent }
          : student
      )
    );
  };

  const saveAttendance = () => {
    const presentCount = detectedStudents.filter(s => s.isPresent).length;
    const totalCount = detectedStudents.length;

    toast({
      title: "Attendance Saved",
      description: `Saved attendance for ${totalCount} students (${presentCount} present, ${totalCount - presentCount} absent)`,
    });

    // Reset form
    setSelectedSubject('');
    setSelectedImage(null);
    setImagePreview(null);
    setDetectedStudents([]);
    setShowResults(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const resetForm = () => {
    setSelectedSubject('');
    setSelectedImage(null);
    setImagePreview(null);
    setDetectedStudents([]);
    setShowResults(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto p-6">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <Camera className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold text-foreground">Take Attendance</h1>
            <p className="text-muted-foreground">Capture attendance using photo recognition</p>
          </div>
        </div>

        {/* Setup Form */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Attendance Setup</CardTitle>
            <CardDescription>
              Select subject and upload a class photo to automatically detect students
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Subject Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Select Subject</label>
              <Select value={selectedSubject} onValueChange={setSelectedSubject}>
                <SelectTrigger>
                  <SelectValue placeholder="Choose a subject" />
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

            {/* Image Upload Section */}
            <div className="space-y-3">
              <label className="text-sm font-medium">Upload Photo or Use Webcam</label>
              
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center gap-2"
                >
                  <Upload className="h-4 w-4" />
                  Upload Image
                </Button>
                
                <Button
                  variant="outline"
                  onClick={handleWebcamCapture}
                  className="flex items-center gap-2"
                >
                  <Camera className="h-4 w-4" />
                  Use Webcam
                </Button>

                {(selectedSubject || selectedImage) && (
                  <Button
                    variant="outline"
                    onClick={resetForm}
                    className="flex items-center gap-2"
                  >
                    <RotateCcw className="h-4 w-4" />
                    Reset
                  </Button>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />

              {/* Image Preview */}
              {imagePreview && (
                <div className="mt-4">
                  <img
                    src={imagePreview}
                    alt="Uploaded class photo"
                    className="max-w-full h-auto max-h-64 rounded-lg border"
                  />
                </div>
              )}
            </div>

            {/* Process Button */}
            <Button
              onClick={processAttendance}
              disabled={!selectedSubject || !selectedImage || isProcessing}
              className="w-full"
              size="lg"
            >
              {isProcessing ? 'Processing...' : 'Process Attendance'}
            </Button>
          </CardContent>
        </Card>

        {/* Results Section */}
        {showResults && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Detected Students
              </CardTitle>
              <CardDescription>
                Review and adjust attendance. {detectedStudents.filter(s => s.isPresent).length} of {detectedStudents.length} students detected as present.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 mb-6">
                {detectedStudents.map((student) => (
                  <div
                    key={student.id}
                    className="flex items-center justify-between p-3 border rounded-lg"
                  >
                    <div>
                      <div className="font-medium">{student.name}</div>
                      <div className="text-sm text-muted-foreground">{student.email}</div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <label className="flex items-center gap-2 cursor-pointer">
                        <Checkbox
                          checked={student.isPresent}
                          onCheckedChange={() => toggleStudentPresence(student.id)}
                        />
                        <span className={`text-sm font-medium ${
                          student.isPresent ? 'text-success' : 'text-muted-foreground'
                        }`}>
                          {student.isPresent ? 'Present' : 'Absent'}
                        </span>
                      </label>
                    </div>
                  </div>
                ))}
              </div>

              <Button onClick={saveAttendance} className="w-full" size="lg">
                <Save className="h-4 w-4 mr-2" />
                Save Attendance
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default TakeAttendance;