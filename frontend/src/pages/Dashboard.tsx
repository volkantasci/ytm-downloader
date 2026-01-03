import React, { useState } from 'react';
import { searchDownload, artistDownload } from '../api';
import { JobList } from '../components/JobList';
import { useJobStore } from '../stores/jobStore';
import { Search, Music, Download, Disc } from 'lucide-react';

export const Dashboard: React.FC = () => {
    const { fetchJobs } = useJobStore();
    const [searchQuery, setSearchQuery] = useState('');
    const [searchLimit, setSearchLimit] = useState(5);

    const [artistUrl, setArtistUrl] = useState('');
    const [artistName, setArtistName] = useState('');
    const [artistLimit, setArtistLimit] = useState(5);
    const [artistSongLimit, setArtistSongLimit] = useState(1);
    const [maxAlbumLength, setMaxAlbumLength] = useState(25);

    const handleSearchDownload = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await searchDownload(searchQuery, searchLimit);
            fetchJobs(); // Trigger refresh
            setSearchQuery('');
            // Optional: Show toast
        } catch (error) {
            console.error(error);
            alert('Failed to start search download');
        }
    };

    const handleArtistDownload = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await artistDownload(artistUrl, artistName || 'Unknown Artist', artistLimit, artistSongLimit, maxAlbumLength);
            fetchJobs(); // Trigger refresh
            setArtistUrl('');
            setArtistName('');
        } catch (error) {
            console.error(error);
            alert('Failed to start artist download');
        }
    };

    return (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
                <p className="text-gray-400">Manage your music downloads and library.</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
                {/* Search Download Card */}
                <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 shadow-xl hover:border-blue-500/30 transition-colors flex flex-col h-full">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-3 bg-blue-500/10 rounded-lg text-blue-400">
                            <Search className="w-6 h-6" />
                        </div>
                        <div>
                            <h2 className="text-xl font-semibold text-white">Search & Download</h2>
                            <p className="text-sm text-gray-500">Download top songs from a search query</p>
                        </div>
                    </div>
                    <form onSubmit={handleSearchDownload} className="space-y-4 flex flex-col flex-1">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-1">Search Query</label>
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 outline-none transition-all placeholder:text-gray-700"
                                placeholder="e.g. 'Chill lo-fi beats'"
                                required
                            />
                        </div>
                        <div className="flex-1">
                            <label className="block text-sm font-medium text-gray-400 mb-1">Song Limit</label>
                            <input
                                type="number"
                                value={searchLimit}
                                onChange={(e) => setSearchLimit(Number(e.target.value))}
                                min={1}
                                max={50}
                                className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 outline-none transition-all"
                            />
                        </div>
                        <div className="mt-auto">
                            <button
                                type="submit"
                                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 shadow-lg shadow-blue-900/20">
                                <Download className="w-4 h-4" />
                                Start Download
                            </button>
                        </div>
                    </form>
                </div>

                {/* Artist Download Card */}
                <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 shadow-xl hover:border-purple-500/30 transition-colors flex flex-col h-full">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-3 bg-purple-500/10 rounded-lg text-purple-400">
                            <Music className="w-6 h-6" />
                        </div>
                        <div>
                            <h2 className="text-xl font-semibold text-white">Artist Discography</h2>
                            <p className="text-sm text-gray-500">Download albums for a specific artist</p>
                        </div>
                    </div>
                    <form onSubmit={handleArtistDownload} className="space-y-4 flex flex-col flex-1">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Artist Name</label>
                                <input
                                    type="text"
                                    value={artistName}
                                    onChange={(e) => setArtistName(e.target.value)}
                                    className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all placeholder:text-gray-700"
                                    placeholder="e.g. 'Pink Floyd'"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Album Limit</label>
                                <input
                                    type="number"
                                    value={artistLimit}
                                    onChange={(e) => setArtistLimit(Number(e.target.value))}
                                    min={1}
                                    className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all"
                                />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-1">Artist URL (Optional)</label>
                            <input
                                type="url"
                                value={artistUrl}
                                onChange={(e) => setArtistUrl(e.target.value)}
                                className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all placeholder:text-gray-700"
                                placeholder="https://music.youtube.com/channel/..."
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4 flex-1">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Songs per Album</label>
                                <input
                                    type="number"
                                    value={artistSongLimit}
                                    onChange={(e) => setArtistSongLimit(Number(e.target.value))}
                                    min={1}
                                    className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Max Tracks/Album</label>
                                <input
                                    type="number"
                                    value={maxAlbumLength}
                                    onChange={(e) => setMaxAlbumLength(Number(e.target.value))}
                                    min={1}
                                    className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all"
                                />
                            </div>
                        </div>

                        <div className="mt-auto">
                            <button
                                type="submit"
                                className="w-full bg-purple-600 hover:bg-purple-500 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 shadow-lg shadow-purple-900/20">
                                <Disc className="w-4 h-4" />
                                Start Download
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <JobList />
        </div>
    );
};
