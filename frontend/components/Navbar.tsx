import Link from 'next/link';
import { Home, MessageSquare, ListTodo } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md border-b">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 text-indigo-600 font-bold">
              <ListTodo className="w-6 h-6" />
              <span>Todo App</span>
            </Link>
          </div>
          <div className="flex space-x-4">
            <Link href="/" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-gray-100">
              <Home className="w-4 h-4" />
              <span>Home</span>
            </Link>
            <Link href="/tasks" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-gray-100">
              <ListTodo className="w-4 h-4" />
              <span>Tasks</span>
            </Link>
            <Link href="/chat" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-gray-100">
              <MessageSquare className="w-4 h-4" />
              <span>AI Chat</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
