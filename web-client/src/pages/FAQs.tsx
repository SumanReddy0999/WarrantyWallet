
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { HelpCircle } from 'lucide-react';

const FAQs = () => {
  const faqs = [
    {
      question: "How do I register my warranty?",
      answer: "Simply upload your warranty documents through our platform and our AI will automatically extract and organize all the important information."
    },
    {
      question: "What types of warranties can I manage?",
      answer: "Our platform supports all types of warranties including electronics, appliances, vehicles, and more."
    },
    {
      question: "How do I claim warranty service?",
      answer: "Use our chat interface to get step-by-step guidance on how to claim warranty service for your specific product."
    },
    {
      question: "Is my data secure?",
      answer: "Yes, we use enterprise-grade security measures to protect all your warranty information and personal data."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Navigation />
      
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <HelpCircle className="h-16 w-16 text-blue-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Find answers to common questions about Warranty Wallet
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-6">
          {faqs.map((faq, index) => (
            <Card key={index} className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="text-lg text-blue-900">{faq.question}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{faq.answer}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FAQs;
