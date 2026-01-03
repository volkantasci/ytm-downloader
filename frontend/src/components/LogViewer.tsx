import React, { useEffect, useRef, useState } from 'react';
import { X, Loader2 } from 'lucide-react';

interface LogViewerProps {
    jobId: string;
    isOpen: boolean;
    onClose: () => void;
}

export const LogViewer: React.FC<LogViewerProps> = ({ jobId, isOpen, onClose }) => {
    const [logs, setLogs] = useState<string[]>([]);
    const [status, setStatus] = useState<string>('CONNECTING');
    const logsEndRef = useRef<HTMLDivElement>(null);
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        if (!isOpen || !jobId) return;

        setLogs([]);
        setStatus('CONNECTING');

        // Dynamically determine WS URL
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // const host = window.location.hostname;
        // const port = '8001'; 
        // Logic should match API base URL logic. 
        // In api.ts we use window.location.hostname:8001
        const wsUrl = `${protocol}//${window.location.hostname}:8001/api/v1/jobs/${jobId}/logs`;

        try {
            const ws = new WebSocket(wsUrl);
            wsRef.current = ws;

            ws.onopen = () => {
                setStatus('CONNECTED');
                setLogs(prev => [...prev, '>>> Connection established <<<']);
            };

            ws.onmessage = (event) => {
                const msg = event.data;
                if (typeof msg === 'string') {
                    if (msg.startsWith('JOB_STATUS:')) {
                        setStatus(`FINISHED (${msg.split(':')[1]})`);
                        setLogs(prev => [...prev, `>>> Job finished with status: ${msg.split(':')[1]} <<<`]);
                    } else {
                        setLogs(prev => [...prev, msg]);
                    }
                }
            };

            ws.onclose = (event) => {
                if (event.code !== 1000) {
                    setStatus('DISCONNECTED');
                }
            };

            ws.onerror = () => {
                setStatus('ERROR');
                setLogs(prev => [...prev, '>>> WebSocket Error <<<']);
            };

        } catch (e) {
            console.error(e);
            setStatus(' connection failed');
        }

        return () => {
            if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                wsRef.current.close();
            }
        };

    }, [jobId, isOpen]);

    // Auto-scroll
    useEffect(() => {
        logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="w-full max-w-4xl bg-gray-950 border border-gray-800 rounded-lg shadow-2xl flex flex-col h-[80vh]">
                <div className="flex items-center justify-between p-4 border-b border-gray-800 bg-gray-900 rounded-t-lg">
                    <div className="flex items-center gap-4">
                        <h3 className="font-semibold text-white">Job Logs</h3>
                        <div className="flex items-center gap-2 text-xs">
                            <span className="font-mono text-gray-500 bg-gray-950 px-2 py-1 rounded">
                                {jobId.split('-')[0]}...
                            </span>
                            <span className={`font-bold px-2 py-0.5 rounded ${status === 'CONNECTED' ? 'text-green-400 bg-green-400/10' : 'text-gray-400'}`}>
                                {status}
                            </span>
                        </div>
                    </div>
                    <button onClick={onClose} className="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                <div className="flex-1 overflow-auto p-4 font-mono text-xs md:text-sm bg-gray-950 text-gray-300 rounded-b-lg">
                    {logs.length === 0 && status === 'CONNECTING' && (
                        <div className="flex items-center justify-center h-full text-gray-600 gap-2">
                            <Loader2 className="w-4 h-4 animate-spin" />
                            Connecting to log stream...
                        </div>
                    )}
                    {logs.map((log, index) => (
                        // Using logic to colorize logs? optional enhancement
                        <div key={index} className="whitespace-pre-wrap break-words border-b border-gray-800/30 py-0.5 hover:bg-white/5">
                            <span className="select-none text-gray-700 mr-2 w-6 inline-block text-right">{index + 1}</span>
                            <span className={log.toLowerCase().includes('error') ? 'text-red-400' : 'text-gray-300'}>
                                {log}
                            </span>
                        </div>
                    ))}
                    <div ref={logsEndRef} />
                </div>
            </div>
        </div>
    );
};
