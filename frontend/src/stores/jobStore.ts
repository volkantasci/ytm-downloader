import { create } from 'zustand';
import api from '../api';
import { type Job, JobStatus } from '../types';

interface JobState {
    jobs: Job[];
    loading: boolean;
    error: string | null;
    ws: WebSocket | null;

    // Actions
    fetchJobs: () => Promise<void>;
    connectWebSocket: () => void;
    disconnectWebSocket: () => void;
    cancelJob: (jobId: string) => Promise<void>;
}

const getWebSocketUrl = () => {
    // Protocol wss or ws depending on location
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Port: Use 8001 if localhost/development, otherwise window.location.port
    // Assuming backend runs on 8001 per previous api.ts config for dev
    const port = '8001';
    return `${protocol}//${window.location.hostname}:${port}/api/v1/jobs`;
};

export const useJobStore = create<JobState>((set, get) => ({
    jobs: [],
    loading: false,
    error: null,
    ws: null,

    fetchJobs: async () => {
        // Fallback or initial fetch
        set({ loading: true });
        try {
            const response = await api.get('/jobs');
            set({ jobs: response.data, loading: false, error: null });
        } catch (error) {
            console.error('Failed to fetch jobs:', error);
            set({ error: 'Failed to fetch jobs', loading: false });
        }
    },

    connectWebSocket: () => {
        const url = getWebSocketUrl();
        console.log('Connecting to Jobs WebSocket:', url);

        if (get().ws) {
            get().ws?.close();
        }

        const ws = new WebSocket(url);

        ws.onopen = () => {
            console.log('Jobs WebSocket Connected');
        };

        ws.onmessage = (event) => {
            try {
                const jobs: Job[] = JSON.parse(event.data);
                set({ jobs, loading: false, error: null });
            } catch (e) {
                console.error('Failed to parse websocket message', e);
            }
        };

        ws.onclose = () => {
            console.log('Jobs WebSocket Disconnected');
            // Reconnect logic could go here (e.g. setTimeout)
            // For now, let's keep it simple. If it disconnects, user might need to refresh or we retry.
            set({ ws: null });
            setTimeout(() => {
                if (!get().ws) {
                    get().connectWebSocket();
                }
            }, 3000);
        };

        set({ ws });
    },

    disconnectWebSocket: () => {
        const { ws } = get();
        if (ws) {
            ws.close();
        }
        set({ ws: null });
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
            // No need to refetch manually, WebSocket should update.
        } catch (error) {
            console.error('Failed to cancel job', error);
            // WebSocket will correct the state if it failed
        }
    }
}));
