import { useState, useEffect } from 'react';
import { WarrantyCard, getWarrantyStatus } from '../components/WarrantyCard';
import { Input } from '../components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Button } from '../components/ui/button';
import { Plus } from 'lucide-react';

// Mock data - replace with actual API calls
const mockWarranties = [
  {
    id: '1',
    productName: 'iPhone 13 Pro',
    expiryDate: '2024-12-31',
    warrantyNumber: 'WARR-2023-001',
    purchaseDate: '2023-01-15',
    retailerName: 'Apple Store',
    category: 'Smartphone',
  },
  {
    id: '2',
    productName: 'Samsung QLED TV',
    expiryDate: '2023-11-30',
    warrantyNumber: 'WARR-2023-042',
    purchaseDate: '2023-03-10',
    retailerName: 'Best Buy',
    category: 'Television',
  },
  {
    id: '3',
    productName: 'Dyson V11 Vacuum',
    expiryDate: '2023-10-15',
    warrantyNumber: 'WARR-2023-087',
    purchaseDate: '2022-10-15',
    retailerName: 'Amazon',
    category: 'Home Appliance',
  },
];

export default function WarrantiesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [warranties] = useState(mockWarranties);
  const [filteredWarranties, setFilteredWarranties] = useState(mockWarranties);
  const [activeTab, setActiveTab] = useState('all');

  // Filter warranties based on search query and active tab
  useEffect(() => {
    let result = [...warranties];
    
    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(warranty => 
        warranty.productName.toLowerCase().includes(query) ||
        warranty.warrantyNumber.toLowerCase().includes(query) ||
        warranty.retailerName.toLowerCase().includes(query)
      );
    }
    
    // Apply status filter
    if (activeTab !== 'all') {
      result = result.filter(warranty => {
        const { status } = getWarrantyStatus(warranty.expiryDate);
        return status === activeTab;
      });
    }
    
    setFilteredWarranties(result);
  }, [searchQuery, activeTab, warranties]);

  // Get counts for each status
  const statusCounts = warranties.reduce(
    (counts, warranty) => {
      const { status } = getWarrantyStatus(warranty.expiryDate);
      counts[status] = (counts[status] || 0) + 1;
      return counts;
    },
    { active: 0, expiring_soon: 0, expired: 0 }
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Warranties</h1>
          <p className="text-muted-foreground">
            Manage and track all your product warranties in one place
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Warranty
        </Button>
      </div>

      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search warranties..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="max-w-md"
            />
          </div>
          <div className="flex-shrink-0">
            <Tabs 
              value={activeTab} 
              onValueChange={setActiveTab}
              className="w-full sm:w-auto"
            >
              <TabsList>
                <TabsTrigger value="all">All ({warranties.length})</TabsTrigger>
                <TabsTrigger value="active">Active ({statusCounts.active})</TabsTrigger>
                <TabsTrigger value="expiring_soon">
                  Expiring Soon ({statusCounts.expiring_soon})
                </TabsTrigger>
                <TabsTrigger value="expired">Expired ({statusCounts.expired})</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>

        {filteredWarranties.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredWarranties.map((warranty) => {
              const { status, daysRemaining } = getWarrantyStatus(warranty.expiryDate);
              
              return (
                <WarrantyCard
                  key={warranty.id}
                  productName={warranty.productName}
                  expiryDate={warranty.expiryDate}
                  status={status}
                  daysRemaining={daysRemaining}
                  details={{
                    warrantyNumber: warranty.warrantyNumber,
                    purchaseDate: warranty.purchaseDate,
                    retailerName: warranty.retailerName,
                    category: warranty.category,
                  }}
                />
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12 border rounded-lg bg-muted/20">
            <h3 className="text-lg font-medium">No warranties found</h3>
            <p className="text-muted-foreground mt-2">
              {searchQuery 
                ? 'Try adjusting your search or filter criteria.'
                : 'Get started by adding your first warranty.'}
            </p>
            <Button className="mt-4">
              <Plus className="mr-2 h-4 w-4" />
              Add Warranty
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
