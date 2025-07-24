
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ArrowUp, MessageSquare, FileText, Clock, Shield, CheckCircle } from 'lucide-react';

interface ChatInterfaceProps {
  documents: string[];
}

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export const ChatInterface = ({ documents }: ChatInterfaceProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I've analyzed your warranty documents. You can ask me questions like 'When does my warranty expire?' or 'What's covered under warranty?'",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const sampleQuestions = [
    "When does my warranty expire?",
    "What's covered under my warranty?",
    "How do I claim warranty service?",
    "What damages are excluded?"
  ];

  // Create a proper mapping of questions to responses
  const questionResponseMap = {
    "When does my warranty expire?": "Based on your warranty document, your coverage expires on March 15, 2025. You have 3 months remaining on your warranty period.",
    "What's covered under my warranty?": "Your warranty covers manufacturing defects, electrical failures, and normal wear and tear. However, accidental damage and water damage are excluded.",
    "How do I claim warranty service?": "To claim warranty service, contact the manufacturer at 1-800-WARRANTY with your purchase receipt and product serial number. Service is typically processed within 5-7 business days.",
    "What damages are excluded?": "The following are excluded from warranty coverage: accidental damage, water damage, cosmetic scratches, damage from misuse, and normal wear after the warranty period."
  };

  const getResponseForQuestion = (question: string): string => {
    // First check for exact matches
    if (questionResponseMap[question as keyof typeof questionResponseMap]) {
      return questionResponseMap[question as keyof typeof questionResponseMap];
    }

    // Check for partial matches based on keywords
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('expire') || lowerQuestion.includes('expir') || lowerQuestion.includes('when')) {
      return questionResponseMap["When does my warranty expire?"];
    } else if (lowerQuestion.includes('covered') || lowerQuestion.includes('cover') || lowerQuestion.includes('what')) {
      return questionResponseMap["What's covered under my warranty?"];
    } else if (lowerQuestion.includes('claim') || lowerQuestion.includes('service') || lowerQuestion.includes('how')) {
      return questionResponseMap["How do I claim warranty service?"];
    } else if (lowerQuestion.includes('excluded') || lowerQuestion.includes('exclude') || lowerQuestion.includes('damage')) {
      return questionResponseMap["What damages are excluded?"];
    }

    // Default response for unmatched questions
    return "I'm sorry, I couldn't find specific information about that in your warranty documents. Please try asking about warranty coverage, expiration dates, claim procedures, or excluded damages.";
  };

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Get the appropriate response for the question
    setTimeout(() => {
      const response = getResponseForQuestion(text.trim());
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response,
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="max-w-6xl mx-auto grid lg:grid-cols-4 gap-6">
      {/* Sidebar with document info */}
      <div className="lg:col-span-1">
        <Card className="bg-white/60 backdrop-blur-sm border-0 shadow-lg mb-6">
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="h-5 w-5 mr-2 text-blue-600" />
              Documents
            </CardTitle>
          </CardHeader>
          <CardContent>
            {documents.length > 0 ? (
              <div className="space-y-2">
                {documents.map((doc, index) => (
                  <div key={index} className="flex items-center p-2 bg-green-50 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                    <span className="text-sm text-gray-700 truncate">{doc}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-4">
                <FileText className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-500">No documents uploaded</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-white/60 backdrop-blur-sm border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MessageSquare className="h-5 w-5 mr-2 text-purple-600" />
              Quick Questions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {sampleQuestions.map((question, index) => (
                <Button
                  key={index}
                  variant="ghost"
                  size="sm"
                  className="w-full text-left justify-start text-sm h-auto p-2 hover:bg-white/50"
                  onClick={() => handleSendMessage(question)}
                >
                  {question}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Chat Interface */}
      <div className="lg:col-span-3">
        <Card className="bg-white/60 backdrop-blur-sm border-0 shadow-lg h-[600px] flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Shield className="h-6 w-6 mr-2 text-blue-600" />
              AI Warranty Assistant
            </CardTitle>
          </CardHeader>
          
          {/* Messages */}
          <CardContent className="flex-1 overflow-y-auto p-6">
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                      message.isUser
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                        : 'bg-white/80 text-gray-800 shadow-sm'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      message.isUser ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </p>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-white/80 px-4 py-2 rounded-2xl shadow-sm">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-200"></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
          
          {/* Input */}
          <div className="p-6 border-t border-gray-200/50">
            <div className="flex space-x-2">
              <Input
                placeholder="Ask about your warranty..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputValue)}
                className="flex-1 bg-white/80 border-gray-200 focus:border-blue-500"
              />
              <Button
                onClick={() => handleSendMessage(inputValue)}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2"
                disabled={!inputValue.trim() || isTyping}
              >
                <ArrowUp className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
