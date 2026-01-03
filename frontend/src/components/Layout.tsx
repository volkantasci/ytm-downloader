import React, { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Library as LibraryIcon, Menu, X, Disc } from 'lucide-react';
import { cn } from '../utils';

export const Layout: React.FC = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

    const navItems = [
        { to: "/", icon: LayoutDashboard, label: "Dashboard" },
        { to: "/library", icon: LibraryIcon, label: "Library" },
    ];

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100 font-sans selection:bg-blue-500/30">
            {/* Mobile Header */}
            <div className="lg:hidden flex items-center justify-between p-4 border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-40">
                <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                        <Disc className="w-5 h-5 text-white" />
                    </div>
                    <span>YTM<span className="text-blue-500">Downloader</span></span>
                </div>
                <button onClick={toggleSidebar} className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white">
                    {isSidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </button>
            </div>

            <div className="flex h-screen overflow-hidden">
                {/* Sidebar */}
                <aside className={cn(
                    "fixed lg:relative inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out border-r border-gray-800 bg-gray-900/50 backdrop-blur-xl lg:translate-x-0 lg:bg-gray-900/30 lg:block",
                    isSidebarOpen ? "translate-x-0 block" : "-translate-x-full hidden"
                )}>
                    <div className="flex flex-col h-full">
                        <div className="p-6">
                            <div className="hidden lg:flex items-center gap-2 font-bold text-xl tracking-tight mb-8">
                                <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                                    <Disc className="w-5 h-5 text-white" />
                                </div>
                                <span>YTM<span className="text-blue-500">Downloader</span></span>
                            </div>

                            <nav className="space-y-1">
                                {navItems.map((item) => (
                                    <NavLink
                                        key={item.to}
                                        to={item.to}
                                        onClick={() => setIsSidebarOpen(false)}
                                        className={({ isActive }) => cn(
                                            "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium group",
                                            isActive
                                                ? "bg-blue-600/10 text-blue-400 border border-blue-500/10 shadow-sm"
                                                : "text-gray-400 hover:bg-gray-800 hover:text-white"
                                        )}
                                    >
                                        <item.icon className="w-5 h-5 transition-transform group-hover:scale-110" />
                                        {item.label}
                                    </NavLink>
                                ))}
                            </nav>
                        </div>

                        <div className="mt-auto p-6 border-t border-gray-800/50">
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-xs font-bold text-gray-500 border border-gray-700">
                                    V
                                </div>
                                <div className="text-sm">
                                    <p className="font-medium text-white">YTM Downloader</p>
                                    <p className="text-xs text-gray-500">v2.0.0 (Agentic)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </aside>

                {/* Overlay for mobile */}
                {isSidebarOpen && (
                    <div
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
                        onClick={() => setIsSidebarOpen(false)}
                    />
                )}

                {/* Main Content */}
                <main className="flex-1 overflow-auto w-full relative bg-gray-950">
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-transparent to-purple-500/5 pointer-events-none fixed" />
                    <Outlet />
                </main>
            </div>
        </div>
    );
};
