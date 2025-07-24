
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { ArrowUp, FileUp, MessageSquare, Shield, Upload, Zap } from 'lucide-react';
import { ChatInterface } from '@/components/ChatInterface';
import { DocumentUpload } from '@/components/DocumentUpload';
import { FeatureCard } from '@/components/FeatureCard';
import { HeroSection } from '@/components/HeroSection';
import { Navigation } from '@/components/Navigation';

const Index = () => {
  const [activeView, setActiveView] = useState<'home' | 'upload' | 'chat'>('home');
  const [uploadedDocuments, setUploadedDocuments] = useState<string[]>([]);

  const handleDocumentUpload = (fileName: string) => {
    setUploadedDocuments(prev => [...prev, fileName]);
    // Simulate processing delay
    setTimeout(() => {
      setActiveView('chat');
    }, 1500);
  };

  if (activeView === 'upload') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <Button 
              variant="outline" 
              onClick={() => setActiveView('home')}
              className="mb-4 hover:bg-white/50 transition-colors"
            >
              ← Back to Home
            </Button>
          </div>
          <DocumentUpload onUpload={handleDocumentUpload} />
        </div>
      </div>
    );
  }

  if (activeView === 'chat') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <Button 
              variant="outline" 
              onClick={() => setActiveView('home')}
              className="mb-4 hover:bg-white/50 transition-colors"
            >
              ← Back to Home
            </Button>
          </div>
          <ChatInterface documents={uploadedDocuments} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Navigation />
      
      {/* Hero Section */}
      <HeroSection onGetStarted={() => setActiveView('upload')} />

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful AI Features
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience the future of warranty management with our advanced AI capabilities
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<FileUp className="h-8 w-8 text-blue-600" />}
              title="Smart Document Processing"
              description="Upload any warranty document - PDFs, images, or text files. Our AI extracts key information automatically."
            />
            <FeatureCard
              icon={<MessageSquare className="h-8 w-8 text-purple-600" />}
              title="Conversational AI"
              description="Ask questions about your warranties in natural language. Get instant, accurate answers from your documents."
            />
            <FeatureCard
              icon={<Shield className="h-8 w-8 text-green-600" />}
              title="Warranty Tracking"
              description="Never miss an expiration date. Get intelligent reminders and coverage summaries for all your products."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-white/30 backdrop-blur-sm">
        <div className="container mx-auto text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
              Ready to Transform Your Warranty Management?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join thousands of users who have simplified their warranty tracking with AI
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                onClick={() => setActiveView('upload')}
              >
                <Upload className="mr-2 h-5 w-5" />
                Upload Your First Document
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="px-8 py-4 rounded-xl border-2 border-gray-300 hover:border-blue-500 hover:bg-blue-50 transition-all duration-300"
                onClick={() => setActiveView('chat')}
              >
                <MessageSquare className="mr-2 h-5 w-5" />
                Try Demo Chat
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-gray-200 bg-white/20 backdrop-blur-sm">
        <div className="container mx-auto text-center">
          <div className="flex items-center justify-center mb-4">
            <Shield className="h-8 w-8 text-blue-600 mr-2" />
            <span className="text-2xl font-bold text-gray-900">Warranty Wallet</span>
          </div>
          <p className="text-gray-600 mb-4">
            Intelligent warranty management powered by AI
          </p>
          <p className="text-sm text-gray-500">
            © 2024 Warranty Wallet. Built with modern AI technology.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
