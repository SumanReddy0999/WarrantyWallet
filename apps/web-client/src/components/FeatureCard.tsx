
import { Card, CardContent } from "@/components/ui/card";
import { ReactNode } from "react";

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

export const FeatureCard = ({ icon, title, description }: FeatureCardProps) => {
  return (
    <Card className="relative overflow-hidden border-0 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-all duration-300 hover:scale-105 hover:shadow-xl">
      <CardContent className="p-8">
        <div className="mb-4 transform transition-transform duration-300 hover:scale-110">
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-3">
          {title}
        </h3>
        <p className="text-gray-600 leading-relaxed">
          {description}
        </p>
      </CardContent>
      
      {/* Subtle gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent pointer-events-none"></div>
    </Card>
  );
};
