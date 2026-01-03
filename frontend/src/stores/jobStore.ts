import { create } from 'zustand';
import api from '../api';
import { type Job, JobStatus } from '../types';

interface JobState {
    jobs: Job[];
    loading: boolean;
    error: string | null;
    fetchJobs: () => Promise<void>;
    cancelJob: (jobId: string) => Promise<void>;
}

export const useJobStore = create<JobState>((set, get) => ({
    jobs: [],
    loading: false,
    error: null,

    fetchJobs: async () => {
        set({ loading: true });
        try {
            const response = await api.get('/jobs');
            set({ jobs: response.data, loading: false, error: null });
        } catch (error) {
            console.error('Failed to fetch jobs:', error);
            set({ error: 'Failed to fetch jobs', loading: false });
        }
    },

    cancelJob: async (jobId: string) => {
        try {
            // Optimistic update
            set((state) => ({
                jobs: state.jobs.map(job =>
                    job.id === jobId ? { ...job, status: JobStatus.CANCELLED } : job
                )
            }));

            await api.post(`/jobs/${jobId}/cancel`);

            // Refetch to sync state properly
            get().fetchJobs();
        } catch (error) {
            console.error('Failed to cancel job', error);
            // Revert state by fetching
            get().fetchJobs();
        }
    }
}));
