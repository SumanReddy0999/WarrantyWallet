
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { FileUp, Upload, FileText, Image } from 'lucide-react';

interface DocumentUploadProps {
  onUpload: (fileName: string) => void;
}

export const DocumentUpload = ({ onUpload }: DocumentUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileSelect = async (file: File) => {
    setIsProcessing(true);
    setProgress(0);

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('document', file);

      // Simulate progress during upload
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + Math.random() * 10, 90));
      }, 200);

      // Upload file to server
      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Upload failed');
      }

      const result = await response.json();
      
      setTimeout(() => {
        setIsProcessing(false);
        onUpload(result.document.originalName);
      }, 500);

    } catch (error) {
      console.error('Upload error:', error);
      setIsProcessing(false);
      setProgress(0);
      // You could add error state handling here
      alert('Failed to upload file. Please try again.');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Upload Your Warranty Documents
        </h1>
        <p className="text-lg text-gray-600">
          Drag and drop your files or click to browse. We support PDFs, images, and text documents.
        </p>
      </div>

      {isProcessing ? (
        <Card className="bg-white/60 backdrop-blur-sm border-0 shadow-xl">
          <CardContent className="p-12">
            <div className="text-center">
              <div className="mb-6">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                  <FileUp className="h-8 w-8 text-blue-600 animate-pulse" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Processing Your Document
                </h3>
                <p className="text-gray-600">
                  Our AI is analyzing your warranty document and extracting key information...
                </p>
              </div>
              <div className="max-w-md mx-auto">
                <Progress value={progress} className="mb-4" />
                <p className="text-sm text-gray-500">
                  {progress < 30 ? 'Analyzing document structure...' :
                   progress < 60 ? 'Extracting warranty information...' :
                   progress < 90 ? 'Processing with AI...' :
                   'Almost ready!'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card 
          className={`bg-white/40 backdrop-blur-sm border-2 border-dashed transition-all duration-300 hover:bg-white/60 ${
            isDragging ? 'border-blue-500 bg-blue-50/50' : 'border-gray-300'
          }`}
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onDragEnter={() => setIsDragging(true)}
          onDragLeave={() => setIsDragging(false)}
        >
          <CardContent className="p-12">
            <div className="text-center">
              <div className="mb-6">
                <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full mb-4 transition-all duration-300 ${
                  isDragging ? 'bg-blue-100 scale-110' : 'bg-gray-100'
                }`}>
                  <Upload className={`h-10 w-10 transition-colors duration-300 ${
                    isDragging ? 'text-blue-600' : 'text-gray-400'
                  }`} />
                </div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                  Drop your files here
                </h3>
                <p className="text-gray-600 mb-6">
                  or click to browse from your computer
                </p>
              </div>

              <input
                type="file"
                id="file-upload"
                className="hidden"
                accept=".pdf,.jpg,.jpeg,.png,.txt,.doc,.docx"
                onChange={handleFileInput}
              />
              
              <Button 
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                onClick={() => document.getElementById('file-upload')?.click()}
              >
                <FileUp className="mr-2 h-5 w-5" />
                Choose Files
              </Button>

              <div className="mt-8 flex justify-center space-x-6">
                <div className="flex items-center text-sm text-gray-500">
                  <FileText className="h-4 w-4 mr-1" />
                  PDF
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Image className="h-4 w-4 mr-1" />
                  Images
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <FileText className="h-4 w-4 mr-1" />
                  Documents
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Example Documents Section */}
      <div className="mt-12">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          Supported Document Types
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          <Card className="bg-white/30 backdrop-blur-sm border-0">
            <CardContent className="p-4 text-center">
              <FileText className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <p className="font-medium text-gray-900">Warranty Cards</p>
              <p className="text-sm text-gray-600">PDF or scanned warranty documents</p>
            </CardContent>
          </Card>
          <Card className="bg-white/30 backdrop-blur-sm border-0">
            <CardContent className="p-4 text-center">
              <Image className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <p className="font-medium text-gray-900">Receipt Photos</p>
              <p className="text-sm text-gray-600">Photos of purchase receipts</p>
            </CardContent>
          </Card>
          <Card className="bg-white/30 backdrop-blur-sm border-0">
            <CardContent className="p-4 text-center">
              <FileText className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <p className="font-medium text-gray-900">User Manuals</p>
              <p className="text-sm text-gray-600">Product manuals with warranty info</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
