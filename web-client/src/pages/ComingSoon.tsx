import { Navigation } from '@/components/Navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ArrowLeft, Clock, Construction } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ComingSoon = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto text-center">
          {/* Back Button */}
          <div className="mb-8 text-left">
            <Button 
              variant="outline" 
              onClick={() => navigate(-1)}
              className="hover:bg-white/50 transition-colors"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Go Back
            </Button>
          </div>

          {/* Main Content */}
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg p-8">
            <CardContent className="p-0">
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <Construction className="h-20 w-20 text-orange-500" />
                  <Clock className="h-8 w-8 text-blue-500 absolute -top-2 -right-2" />
                </div>
              </div>
              
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Coming Soon!
              </h1>
              
              <p className="text-xl text-gray-600 mb-6">
                We're working hard to bring you this amazing feature. 
                Stay tuned for updates!
              </p>
              
              <div className="bg-gradient-to-r from-blue-100 to-purple-100 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  What to expect:
                </h3>
                <ul className="text-gray-600 space-y-2 text-left">
                  <li className="flex items-center">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                    Enhanced user experience
                  </li>
                  <li className="flex items-center">
                    <div className="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
                    Advanced AI capabilities
                  </li>
                  <li className="flex items-center">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                    Seamless integration
                  </li>
                </ul>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  onClick={() => navigate('/')}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                >
                  Back to Home
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => navigate('/contact')}
                >
                  Contact Us
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ComingSoon; 