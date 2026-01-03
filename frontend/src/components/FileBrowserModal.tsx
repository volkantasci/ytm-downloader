import React, { useEffect, useState } from 'react';
import { fetchFiles, type FileNode } from '../api';
import { X, Folder, FileMusic, ChevronRight, CornerLeftUp, Loader2 } from 'lucide-react';

interface FileBrowserModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const FileBrowserModal: React.FC<FileBrowserModalProps> = ({ isOpen, onClose }) => {
    const [path, setPath] = useState('');
    const [history, setHistory] = useState<string[]>([]);
    const [files, setFiles] = useState<FileNode[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isOpen) {
            loadFiles(path);
        }
    }, [isOpen, path]);

    const loadFiles = async (currentPath: string) => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchFiles(currentPath);
            setFiles(data);
        } catch (err) {
            console.error(err);
            setError('Failed to load directory contents.');
        } finally {
            setLoading(false);
        }
    };

    const handleNavigate = (folderName: string) => {
        setHistory([...history, path]);
        const newPath = path ? `${path}/${folderName}` : folderName;
        setPath(newPath);
    };

    const handleGoUp = () => {
        if (path === '') return;

        // Remove last segment
        const parts = path.split('/');
        parts.pop();
        setPath(parts.join('/'));
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="w-full max-w-4xl bg-gray-950 border border-gray-800 rounded-lg shadow-2xl flex flex-col h-[70vh]">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-gray-800 bg-gray-900 rounded-t-lg">
                    <div className="flex items-center gap-2 overflow-hidden">
                        <Folder className="w-5 h-5 text-blue-400 shrink-0" />
                        <h3 className="font-semibold text-white shrink-0">Files</h3>
                        <div className="flex items-center text-sm text-gray-400 px-2 py-1 bg-black/30 rounded border border-gray-800 truncate">
                            /music/{path}
                        </div>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Toolbar */}
                <div className="p-2 border-b border-gray-800 bg-gray-900/50 flex items-center gap-2">
                    <button
                        onClick={handleGoUp}
                        disabled={path === ''}
                        className="p-1.5 rounded hover:bg-gray-800 disabled:opacity-30 disabled:hover:bg-transparent text-gray-300 transition-colors"
                        title="Go Up">
                        <CornerLeftUp className="w-4 h-4" />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-auto p-2 bg-gray-950/50">
                    {loading ? (
                        <div className="flex flex-col items-center justify-center h-full text-gray-400">
                            <Loader2 className="w-8 h-8 animate-spin mb-2" />
                            Loading...
                        </div>
                    ) : error ? (
                        <div className="flex items-center justify-center h-full text-red-400">
                            {error}
                        </div>
                    ) : files.length === 0 ? (
                        <div className="flex items-center justify-center h-full text-gray-500">
                            Empty Directory
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                            {files.map((file) => (
                                <div
                                    key={file.name}
                                    onClick={() => file.type === 'directory' && handleNavigate(file.name)}
                                    className={`
                                        flex items-center gap-3 p-3 rounded-lg border border-transparent
                                        transition-all cursor-pointer
                                        ${file.type === 'directory'
                                            ? 'hover:bg-blue-500/10 hover:border-blue-500/20 text-gray-200'
                                            : 'hover:bg-gray-800 hover:border-gray-700 text-gray-400 cursor-default'}
                                    `}
                                >
                                    {file.type === 'directory' ? (
                                        <Folder className="w-5 h-5 text-blue-400" />
                                    ) : (
                                        <FileMusic className="w-5 h-5 text-gray-500" />
                                    )}
                                    <div className="min-w-0 flex-1">
                                        <div className="truncate text-sm font-medium">{file.name}</div>
                                        {file.type === 'file' && (
                                            <div className="text-xs text-gray-600">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
                                        )}
                                    </div>
                                    {file.type === 'directory' && (
                                        <ChevronRight className="w-4 h-4 text-gray-600" />
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
