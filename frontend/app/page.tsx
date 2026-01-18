import Link from "next/link";
import { MessageSquare, ListTodo } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Todo App - Phase III
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Task Management with Natural Language
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Link
            href="/tasks"
            className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-indigo-600"
          >
            <div className="flex items-center gap-4 mb-4">
              <div className="bg-blue-100 p-3 rounded-lg group-hover:bg-blue-200">
                <ListTodo className="w-8 h-8 text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold">Tasks</h2>
            </div>
            <p className="text-gray-600">
              Traditional task management interface with full CRUD operations
            </p>
            <div className="mt-6 text-indigo-600 font-medium group-hover:text-indigo-700">
              Go to Tasks →
            </div>
          </Link>

          <Link
            href="/chat"
            className="group bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all"
          >
            <div className="flex items-center gap-4 mb-4">
              <div className="bg-white/20 p-3 rounded-lg group-hover:bg-white/30">
                <MessageSquare className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white">AI Assistant</h2>
            </div>
            <p className="text-indigo-100">
              Manage your tasks using natural language with our AI chatbot
            </p>
            <div className="mt-6 bg-white text-indigo-600 px-4 py-2 rounded-lg inline-block font-medium">
              Start Chatting →
            </div>
          </Link>
        </div>

        <div className="mt-12 text-center">
          <p className="text-gray-500 text-sm">
            Phase III: OpenAI Function Calling + MCP Architecture
          </p>
        </div>
      </div>
    </div>
  );
}
