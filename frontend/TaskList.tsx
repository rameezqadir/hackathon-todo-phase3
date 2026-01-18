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

export default function TaskList({ 
  tasks, 
  onToggleComplete, 
  onDelete, 
  onUpdate, 
  disabled = false 
}: TaskListProps) {
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
            <div className="space-y-3">
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
                rows={2}
              />
              <div className="flex justify-end space-x-2">
                <button
                  onClick={handleCancelEdit}
                  className="flex items-center px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                >
                  <X size={16} className="mr-1" />
                  Cancel
                </button>
                <button
                  onClick={() => handleSaveEdit(task.id)}
                  disabled={!editTitle.trim()}
                  className={`flex items-center px-3 py-1 text-sm text-white rounded ${
                    editTitle.trim()
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-gray-400 cursor-not-allowed'
                  }`}
                >
                  <Save size={16} className="mr-1" />
                  Save
                </button>
              </div>
            </div>
          ) : (
            // View Mode
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center">
                  <button
                    onClick={() => onToggleComplete?.(task.id)}
                    disabled={disabled}
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 ${
                      task.completed
                        ? 'bg-green-500 border-green-500'
                        : 'border-gray-300 hover:border-green-400'
                    } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {task.completed && <Check size={14} className="text-white" />}
                  </button>
                  <div>
                    <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className="text-gray-600 text-sm mt-1">{task.description}</p>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="flex space-x-2 ml-4">
                {onUpdate && (
                  <button
                    onClick={() => handleEditClick(task)}
                    disabled={disabled}
                    className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-md"
                    title="Edit task"
                  >
                    <Pencil size={16} />
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={() => onDelete?.(task.id)}
                    disabled={disabled}
                    className="p-1.5 text-red-600 hover:bg-red-50 rounded-md"
                    title="Delete task"
                  >
                    <Trash2 size={16} />
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
