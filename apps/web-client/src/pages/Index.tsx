
import { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { FileUp, MessageSquare, Shield, Upload } from 'lucide-react';
import { ChatInterface } from '@/components/ChatInterface';
import { DocumentUpload } from '@/components/DocumentUpload';
import { FeatureCard } from '@/components/FeatureCard';
import { HeroSection } from '@/components/HeroSection';
import { Navigation } from '@/components/Navigation';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import VideoHeroSection from '@/components/VideoHeroSection';

const Index = () => {
  // --- State and URL param sync ---
  const [activeView, setActiveView] = useState<'home' | 'upload' | 'chat'>('home');
  const [uploadedDocuments, setUploadedDocuments] = useState<string[]>([]);
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // Sync URL params with component state
  useEffect(() => {
    const view = searchParams.get('view');
    if (view === 'upload' || view === 'chat') {
      setActiveView(view as 'upload' | 'chat');
    } else {
      setActiveView('home');
    }
  }, [searchParams]);

  // Update URL when view changes
  const updateView = (view: 'home' | 'upload' | 'chat') => {
    setActiveView(view);
    if (view === 'home') {
      setSearchParams({});
    } else {
      setSearchParams({ view });
    }
  };

  // Handle document upload and transition to chat view
  const handleDocumentUpload = (fileName: string) => {
    setUploadedDocuments(prev => [...prev, fileName]);
    setTimeout(() => {
      updateView('chat');
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
              onClick={() => {
                updateView('home');
                setUploadedDocuments([]);
              }}
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
              onClick={() => {
                updateView('home');
                setUploadedDocuments([]);
              }}
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
      <HeroSection onGetStarted={() => updateView('upload')} />

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
      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Core Advantages
            </h2>
            
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            <div className="relative overflow-hidden border-0 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-xl">
              <div className="aspect-video overflow-hidden">
                <img 
                  src="/assets/image1.png" 
                  alt="Never Lose a Receipt Again"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Never Lose a Receipt Again
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Securely save a digital copy of any receipt or warranty card just by taking a picture, so it's safe forever. You'll never have to tear your house apart looking for that tiny piece of paper when something breaks.
                </p>
              </div>
            </div>
            
            <div className="relative overflow-hidden border-0 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-xl">
              <div className="aspect-video overflow-hidden">
                <img 
                  src="/assets/image2.png" 
                  alt="Save Money Effortlessly"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Save Money Effortlessly
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Get timely alerts before your warranties and return periods expire, helping you claim the free repair or replacement you're entitled to. This simple reminder can save you hundreds of dollars you would have otherwise spent on fixing or replacing items yourself.
                </p>
              </div>
            </div>
            
            <div className="relative overflow-hidden border-0 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-xl">
              <div className="aspect-video overflow-hidden">
                <img 
                  src="/assets/image3.png" 
                  alt="Stop Worrying About Deadlines"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Stop Worrying About Deadlines
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  The app automatically tracks all your important dates so you can relax and not have to remember when a warranty runs out. Feel confident knowing you have plenty of time to act if a product has a problem.
                </p>
              </div>
            </div>
            
            <div className="relative overflow-hidden border-0 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-all duration-300 hover:scale-105 hover:shadow-xl rounded-xl">
              <div className="aspect-video overflow-hidden">
                <img 
                  src="/assets/image4.png" 
                  alt="Declutter Your Home and Your Mind"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Declutter Your Home and Your Mind
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Eliminate the messy drawer full of old paper receipts, user manuals, and warranty cards by keeping everything neatly organized in one app. Find exactly what you need in seconds, anytime and anywhere, right from your phone.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Video Hero Section */}
      <section className="py-20 px-4 bg-white/30 backdrop-blur-sm">
        <div className="container mx-auto">
          <div className="text-center">
            
            <div className="mt-8 max-w-4xl mx-auto">
              <VideoHeroSection />
            </div>
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
                onClick={() => updateView('upload')}
              >
                <Upload className="mr-2 h-5 w-5" />
                Upload Your First Document
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="px-8 py-4 rounded-xl border-2 border-gray-300 hover:border-blue-500 hover:bg-blue-50 transition-all duration-300"
                onClick={() => updateView('chat')}
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
            © Warranty Wallet
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
