'use client';

import { Check, Trash2, Pencil, X, Save } from 'lucide-react';
import { Task } from '@/lib/api';
import { useState } from 'react';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (taskId: number) => void;
  onDelete?: (taskId: number) => void;
  onUpdate?: (taskId: number, title: string, description: string) => void;
  disabled?: boolean;
}

export default function TaskList({ tasks, onToggleComplete, onDelete, onUpdate, disabled = false }: TaskListProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-2">No tasks yet</div>
        <p className="text-gray-500">Add your first task to get started!</p>
      </div>
    );
  }

  const handleEditClick = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const handleSaveEdit = (taskId: number) => {
    if (onUpdate && editTitle.trim()) {
      onUpdate(taskId, editTitle.trim(), editDescription.trim());
      setEditingId(null);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
    setEditDescription('');
  };

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`bg-white p-4 rounded-lg shadow-sm border ${
            task.completed ? 'opacity-70' : ''
          }`}
        >
          {editingId === task.id ? (
            // Edit Mode
            <div className="space-y-4">
              <div className="space-y-2">
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Task title"
                  autoFocus
                />
                <textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Description (optional)"
                  rows={3}
                />
              </div>
              <div className="flex justify-end gap-2">
                <button
                  onClick={handleCancelEdit}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md"
                >
                  <X size={16} />
                  Cancel
                </button>
                <button
                  onClick={() => handleSaveEdit(task.id)}
                  disabled={!editTitle.trim()}
                  className={`flex items-center gap-1 px-3 py-1.5 text-sm text-white rounded-md ${
                    editTitle.trim()
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-gray-400 cursor-not-allowed'
                  }`}
                >
                  <Save size={16} />
                  Save Changes
                </button>
              </div>
            </div>
          ) : (
            // View Mode
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                    {task.title}
                  </h3>
                  {task.completed && (
                    <span className="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">
                      Completed
                    </span>
                  )}
                </div>
                {task.description && (
                  <p className="text-gray-600 mt-1 mb-2">{task.description}</p>
                )}
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                  {task.updated_at !== task.created_at && (
                    <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2 ml-4">
                {onUpdate && (
                  <button
                    onClick={() => handleEditClick(task)}
                    disabled={disabled}
                    className="p-2 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 disabled:opacity-50"
                    title="Edit task"
                  >
                    <Pencil className="w-4 h-4" />
                  </button>
                )}
                {onToggleComplete && (
                  <button
                    onClick={() => onToggleComplete(task.id)}
                    disabled={disabled}
                    className={`p-2 rounded-full ${
                      task.completed
                        ? 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                        : 'bg-green-100 text-green-600 hover:bg-green-200'
                    } disabled:opacity-50`}
                    title={task.completed ? 'Mark as pending' : 'Mark as completed'}
                  >
                    {task.completed ? <X className="w-4 h-4" /> : <Check className="w-4 h-4" />}
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={() => onDelete(task.id)}
                    disabled={disabled}
                    className="p-2 rounded-full bg-red-100 text-red-600 hover:bg-red-200 disabled:opacity-50"
                    title="Delete task"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
