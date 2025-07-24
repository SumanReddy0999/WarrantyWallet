
import { Button } from "@/components/ui/button";
import { ArrowUp, Shield, Zap } from 'lucide-react';

interface HeroSectionProps {
  onGetStarted: () => void;
}

export const HeroSection = ({ onGetStarted }: HeroSectionProps) => {
  return (
    <section className="relative py-20 px-4 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-32 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-32 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="container mx-auto relative z-10">
        <div className="text-center">
          {/* Logo/Brand */}
          <div className="flex items-center justify-center mb-8">
            <div className="relative">
              <Shield className="h-16 w-16 text-blue-600 animate-pulse" />
              <div className="absolute -top-2 -right-2">
                <Zap className="h-6 w-6 text-yellow-500" />
              </div>
            </div>
          </div>

          {/* Main heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Your AI-Powered
            <span className="block bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Warranty Assistant
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            Upload your warranty documents and ask questions in natural language. 
            Get instant answers, track expiration dates, and never lose coverage again.
          </p>

          {/* Feature highlights */}
          <div className="flex flex-wrap justify-center gap-6 mb-12">
            <div className="flex items-center bg-white/50 backdrop-blur-sm rounded-full px-4 py-2 border border-white/30">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
              <span className="text-sm font-medium text-gray-700">AI Document Analysis</span>
            </div>
            <div className="flex items-center bg-white/50 backdrop-blur-sm rounded-full px-4 py-2 border border-white/30">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
              <span className="text-sm font-medium text-gray-700">Smart Conversations</span>
            </div>
            <div className="flex items-center bg-white/50 backdrop-blur-sm rounded-full px-4 py-2 border border-white/30">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-2 animate-pulse"></div>
              <span className="text-sm font-medium text-gray-700">Expiry Tracking</span>
            </div>
          </div>

          {/* CTA Button */}
          <div className="space-y-4">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-12 py-6 rounded-2xl text-lg font-semibold shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300"
              onClick={onGetStarted}
            >
              Get Started Free
              <ArrowUp className="ml-2 h-5 w-5 rotate-45" />
            </Button>
            <p className="text-sm text-gray-500">
              No credit card required • Process unlimited documents
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
