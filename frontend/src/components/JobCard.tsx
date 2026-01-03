import React from 'react';
import { type Job, JobStatus } from '../types';
import { cn, formatDate } from '../utils';
import { Terminal, XCircle, CheckCircle, AlertCircle, Clock, Loader2 } from 'lucide-react';

interface JobCardProps {
    job: Job;
    onCancel: (id: string) => void;
    onViewLogs: (id: string) => void;
}

const statusColors = {
    [JobStatus.QUEUED]: 'bg-gray-500/10 text-gray-400 border-gray-500/20',
    [JobStatus.RUNNING]: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    [JobStatus.COMPLETED]: 'bg-green-500/10 text-green-400 border-green-500/20',
    [JobStatus.FAILED]: 'bg-red-500/10 text-red-400 border-red-500/20',
    [JobStatus.CANCELLED]: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
};

const StatusIcon = ({ status }: { status: JobStatus }) => {
    switch (status) {
        case JobStatus.QUEUED: return <Clock className="w-4 h-4" />;
        case JobStatus.RUNNING: return <Loader2 className="w-4 h-4 animate-spin" />;
        case JobStatus.COMPLETED: return <CheckCircle className="w-4 h-4" />;
        case JobStatus.FAILED: return <AlertCircle className="w-4 h-4" />;
        case JobStatus.CANCELLED: return <XCircle className="w-4 h-4" />;
        default: return <Clock className="w-4 h-4" />;
    }
};

export const JobCard: React.FC<JobCardProps> = ({ job, onCancel, onViewLogs }) => {
    return (
        <div className={cn(
            "p-4 rounded-lg border backdrop-blur-sm transition-all",
            "bg-gray-900/40 border-gray-800",
            statusColors[job.status]
        )}>
            <div className="flex justify-between items-start mb-2">
                <div className="flex-1 min-w-0 mr-4">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-mono uppercase opacity-70 tracking-wider">
                            {job.job_type?.replace('_', ' ') || 'JOB'}
                        </span>
                        <div className={cn("flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border", statusColors[job.status])}>
                            <StatusIcon status={job.status} />
                            <span className="capitalize">{job.status}</span>
                        </div>
                    </div>
                    <h3 className="font-semibold text-lg text-white truncate" title={job.target}>
                        {job.target}
                    </h3>
                </div>
                <div className="text-right text-xs opacity-50 whitespace-nowrap">
                    <div>Started: {formatDate(job.created_at)}</div>
                    {job.completed_at && <div>Ended: {formatDate(job.completed_at)}</div>}
                </div>
            </div>

            {/* Progress Bar (Indeterminate) */}
            {job.status === JobStatus.RUNNING && (
                <div className="h-1 w-full bg-gray-700/50 rounded-full overflow-hidden mb-4 relative">
                    <div className="h-full bg-blue-500 w-1/3 absolute top-0 left-0 animate-[shimmer_2s_infinite_linear]"
                        style={{
                            background: 'linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.8), transparent)'
                        }}>
                    </div>
                </div>
            )}

            <div className="flex justify-end gap-2 mt-2">
                <button
                    onClick={() => onViewLogs(job.id)}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                               bg-gray-800 hover:bg-gray-700 text-gray-300 transition-colors border border-gray-700">
                    <Terminal className="w-3.5 h-3.5" />
                    <span>Logs</span>
                </button>

                {job.status === JobStatus.RUNNING && (
                    <button
                        onClick={() => onCancel(job.id)}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                                   bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-colors border border-red-500/20">
                        <XCircle className="w-3.5 h-3.5" />
                        <span>Cancel</span>
                    </button>
                )}
            </div>
        </div>
    );
};
