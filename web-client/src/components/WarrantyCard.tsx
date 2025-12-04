import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface WarrantyCardProps {
  productName: string;
  expiryDate: string;
  status: 'active' | 'expired' | 'expiring_soon';
  daysRemaining: number;
  // Additional warranty details that will be shown when expanded
  details?: {
    warrantyNumber?: string;
    purchaseDate?: string;
    retailerName?: string;
    category?: string;
  };
}

export function WarrantyCard({
  productName,
  expiryDate,
  status,
  daysRemaining,
  details = {},
}: WarrantyCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const statusColors = {
    active: 'bg-green-100 text-green-800',
    expired: 'bg-red-100 text-red-800',
    expiring_soon: 'bg-yellow-100 text-yellow-800',
  };

  const formattedExpiryDate = new Date(expiryDate).toLocaleDateString();
  const formattedPurchaseDate = details.purchaseDate 
    ? new Date(details.purchaseDate).toLocaleDateString() 
    : 'N/A';

  return (
    <Card className="w-full max-w-md overflow-hidden">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-lg font-medium">{productName}</CardTitle>
            <CardDescription className="mt-1">
              Expires: {formattedExpiryDate}
            </CardDescription>
          </div>
          <Badge className={statusColors[status]}>
            {status === 'expiring_soon' ? `Expires in ${daysRemaining} days` : status}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="pb-2">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">
              Status: <span className="capitalize">{status.replace('_', ' ')}</span>
            </p>
          </div>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-blue-600 hover:text-blue-800"
          >
            {isExpanded ? 'Show Less' : 'More Details'}
          </Button>
        </div>
      </CardContent>

      {isExpanded && (
        <CardFooter className="pt-0">
          <div className="w-full space-y-2">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="text-muted-foreground">Warranty #</div>
              <div>{details.warrantyNumber || 'N/A'}</div>
              
              <div className="text-muted-foreground">Purchased</div>
              <div>{formattedPurchaseDate}</div>
              
              <div className="text-muted-foreground">Retailer</div>
              <div>{details.retailerName || 'N/A'}</div>
              
              <div className="text-muted-foreground">Category</div>
              <div>{details.category || 'N/A'}</div>
            </div>
            
            <div className="pt-2 flex justify-end space-x-2">
              <Button variant="outline" size="sm">Renew</Button>
              <Button variant="outline" size="sm">Claim</Button>
              <Button variant="outline" size="sm">View Document</Button>
            </div>
          </div>
        </CardFooter>
      )}
    </Card>
  );
}

// Utility function to calculate warranty status and days remaining
export function getWarrantyStatus(expiryDate: string) {
  const today = new Date();
  const expiry = new Date(expiryDate);
  const timeDiff = expiry.getTime() - today.getTime();
  const daysRemaining = Math.ceil(timeDiff / (1000 * 3600 * 24));
  
  if (daysRemaining < 0) {
    return { status: 'expired' as const, daysRemaining: 0 };
  } else if (daysRemaining <= 30) {
    return { status: 'expiring_soon' as const, daysRemaining };
  } else {
    return { status: 'active' as const, daysRemaining };
  }
}
