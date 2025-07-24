import { Navigation } from '../components/Navigation';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { FilePlus, MessageSquare, Bell } from 'lucide-react';

const Dashboard = () => {
  // In the future, you would fetch user data here
  const user = {
    name: 'Sai Teja', // Placeholder name
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Welcome back, {user.name}!</h1>
          <p className="text-gray-500 mt-1">Here's an overview of your warranty documents.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-white shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Active Warranties</CardTitle>
              <FilePlus className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">5</div>
              <p className="text-xs text-gray-500">+2 from last month</p>
            </CardContent>
          </Card>
          <Card className="bg-white shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Expiring Soon</CardTitle>
              <Bell className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2</div>
              <p className="text-xs text-gray-500">Within the next 30 days</p>
            </CardContent>
          </Card>
          <Card className="bg-white shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Chat Sessions</CardTitle>
              <MessageSquare className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-gray-500">Total conversations</p>
            </CardContent>
          </Card>
        </div>

        <div className="text-center">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                <FilePlus className="mr-2 h-5 w-5" /> Upload New Warranty
            </Button>
        </div>

        {/* You would list the user's documents here in the future */}
        <div className="mt-10">
            <h2 className="text-xl font-semibold text-gray-700 mb-4">Your Documents</h2>
            <div className="bg-white p-8 rounded-lg shadow-sm text-center text-gray-500">
                <p>Your uploaded warranty documents will appear here.</p>
            </div>
        </div>

      </main>
    </div>
  );
};

export default Dashboard;
