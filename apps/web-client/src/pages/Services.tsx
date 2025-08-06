
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shield, Wrench, Clock, BrainCircuit, FileUp, MessageSquareDot} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Services = () => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate('/coming-soon');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Our Services</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Comprehensive warranty management solutions for all your needs
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <MessageSquareDot className="h-12 w-12 text-orange-600 mb-4" />
              <CardTitle>Smart Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
              Make smarter decisions with our intelligent suggestions on whether to repair or replace an item. We also provide timely advice on purchasing extended warranties for your most valuable products..
              </p>
            </CardContent>
          </Card>

          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <Wrench className="h-12 w-12 text-purple-600 mb-4" />
              <CardTitle>Repair Services</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Professional repair services with certified technicians for quick resolution.
              </p>
            </CardContent>
          </Card>

          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <Clock className="h-12 w-12 text-green-600 mb-4" />
              <CardTitle>24/7 Support</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Round-the-clock customer support for all your warranty-related queries.
              </p>
            </CardContent>
          </Card>
          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <FileUp className="h-12 w-12 text-yellow-600 mb-4" />
              <CardTitle>Bulk Upload</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
              Effortlessly register all your products at once. Our bulk upload feature allows you to import details for multiple items from a single file, saving you valuable time.
              </p>
            </CardContent>
          </Card>
          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <BrainCircuit className="h-12 w-12 text-red-600 mb-4" />
              <CardTitle>AI-Powered Management</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
              Let our AI do the work by simply scanning your receipts. It automatically extracts and organizes key details like purchase dates and warranty periods for you
              </p>
            </CardContent>
          </Card>
          <Card 
            className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer"
            onClick={handleCardClick}
          >
            <CardHeader>
              <Shield className="h-12 w-12 text-blue-600 mb-4" />
              <CardTitle>Digital Vault</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
              Keep all your important documents in one secure and accessible digital vault. Upload receipts, warranty cards, and invoices to ensure you have them right when you need them.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Services;
