import React, { useEffect, useState } from 'react';
import { useJobStore } from '../stores/jobStore';
import { JobCard } from './JobCard';
import { LogViewer } from './LogViewer';
import { RefreshCw } from 'lucide-react';

export const JobList: React.FC = () => {
    const { jobs, fetchJobs, cancelJob, loading } = useJobStore();
    const [selectedJobId, setSelectedJobId] = useState<string | null>(null);

    // Initial fetch and polling
    useEffect(() => {
        fetchJobs();
        const interval = setInterval(() => {
            // Only poll if not loading to avoid pile up? 
            // Zustand store loading state might be global though.
            // Let's just poll.
            fetchJobs();
        }, 3000);
        return () => clearInterval(interval);
    }, [fetchJobs]);

    const handleViewLogs = (id: string) => setSelectedJobId(id);
    const handleCloseLogs = () => setSelectedJobId(null);

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                    <span className="w-2 h-6 bg-blue-500 rounded-full inline-block"></span>
                    Activity Feed
                </h2>
                <button
                    onClick={() => fetchJobs()}
                    disabled={loading}
                    title="Refresh Jobs"
                    className="p-2 rounded-lg bg-gray-900 border border-gray-800 hover:border-gray-700 hover:bg-gray-800 text-gray-400 hover:text-white transition-all disabled:opacity-50">
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </div>

            <div className="grid gap-4 grid-cols-1">
                {jobs.map((job) => (
                    <JobCard
                        key={job.id}
                        job={job}
                        onCancel={cancelJob}
                        onViewLogs={handleViewLogs}
                    />
                ))}
            </div>

            {jobs.length === 0 && !loading && (
                <div className="text-center py-12 text-gray-600 bg-gray-900/50 border border-dashed border-gray-800 rounded-xl">
                    <p>No active or recent jobs found.</p>
                </div>
            )}

            <LogViewer
                jobId={selectedJobId || ''}
                isOpen={!!selectedJobId}
                onClose={handleCloseLogs}
            />
        </div>
    );
};
