import React, { useState } from 'react';
import { scanLibrary } from '../api';
import { useJobStore } from '../stores/jobStore';
import { Library as LibraryIcon, RefreshCw, FolderOpen, Music2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Library: React.FC = () => {
    const { fetchJobs } = useJobStore();
    const navigate = useNavigate();
    const [isScanning, setIsScanning] = useState(false);

    const handleScanLibrary = async () => {
        setIsScanning(true);
        try {
            await scanLibrary();
            await fetchJobs();
            // Redirect to dashboard to see progress? Or stay here?
            // Let's ask user or just show message.
            // For now, redirecting to Dashboard is a good UX to show the "Job" running.
            navigate('/');
        } catch (error) {
            console.error(error);
            alert('Failed to start library scan');
            setIsScanning(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
            <header className="mb-8 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                        <LibraryIcon className="w-8 h-8 text-green-500" />
                        Music Library
                    </h1>
                    <p className="text-gray-400">Manage and organize your downloaded music collection.</p>
                </div>
                <button
                    onClick={handleScanLibrary}
                    disabled={isScanning}
                    className="bg-green-600 hover:bg-green-500 text-white px-6 py-3 rounded-xl font-semibold shadow-lg shadow-green-900/20 flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                    <RefreshCw className={`w-5 h-5 ${isScanning ? 'animate-spin' : ''}`} />
                    {isScanning ? 'Starting Scan...' : 'Scan & Fix Metadata'}
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-8 text-center hover:bg-gray-900/80 transition-colors group cursor-pointer">
                    <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-500/20 group-hover:text-blue-400 transition-colors text-gray-400">
                        <FolderOpen className="w-8 h-8" />
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">Browse Files</h3>
                    <p className="text-gray-500 text-sm">Open the music directory in your file explorer</p>
                </div>

                <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-8 text-center hover:bg-gray-900/80 transition-colors group cursor-pointer">
                    <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-purple-500/20 group-hover:text-purple-400 transition-colors text-gray-400">
                        <Music2 className="w-8 h-8" />
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">Stats & Analytics</h3>
                    <p className="text-gray-500 text-sm">View collection statistics (Coming Soon)</p>
                </div>
            </div>

            <div className="mt-12 p-6 bg-blue-900/10 border border-blue-500/20 rounded-xl">
                <h4 className="font-semibold text-blue-400 mb-2 flex items-center gap-2">
                    <LibraryIcon className="w-4 h-4" />
                    Library Location
                </h4>
                <code className="bg-black/30 px-4 py-2 rounded text-gray-300 font-mono text-sm block w-full">
                    /app/music
                </code>
                <p className="text-xs text-gray-500 mt-2">
                    Files are organized by Artist / Album. The scanner will fix metadata tags based on this structure.
                </p>
            </div>
        </div>
    );
};
