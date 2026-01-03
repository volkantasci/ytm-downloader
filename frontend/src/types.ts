export const JobStatus = {
    QUEUED: "queued",
    RUNNING: "running",
    COMPLETED: "completed",
    FAILED: "failed",
    CANCELLED: "cancelled"
} as const;

export type JobStatus = typeof JobStatus[keyof typeof JobStatus];

export interface Job {
    id: string;
    job_type: string;
    target: string;
    status: JobStatus;
    created_at: number;
    started_at?: number;
    completed_at?: number;
    error?: string;
    logs?: string[];
}
