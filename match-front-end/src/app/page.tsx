"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

const MusicSearchTab = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const router = useRouter();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-custom-gradient bg-fixed bg-cover">
            <div className="flex items-center gap-4 hover:scale-110 transition-transform -mt-20">
                <div className="items-center px-4 py-4 ring-1 ring-gray-900/5 rounded-lg leading-none flex justify-center space-x-5">
                    <img
                        src="/audio-waves.png"
                        alt="Logo"
                        className="h-36 w-36"
                    />
                    <h1 className="text-center text-transparent text-7xl font-black animate-gradient">
                        melody_match
                    </h1>
                </div>
            </div>

            <form
                onSubmit={handleSubmit}
                className="w-full max-w-2xl bg-white bg-opacity-20 backdrop-blur-md rounded-lg shadow-lg p-2 transition duration-300 hover:shadow-2xl focus-within:shadow-2xl flex items-center gap-2"
            >
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search for music..."
                    className="flex-1 h-11 border-0 bg-transparent text-white text-lg px-4 focus:outline-none font-mono placeholder-white/70"
                />
                <button
                    type="submit"
                    className="w-12 h-12 flex items-center justify-center bg-transparent rounded-lg hover:bg-white/10 transition cursor-pointer"
                >
                    <svg
                        width="20"
                        height="20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="drop-shadow-md transition-all hover:drop-shadow-lg"
                    >
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M8 16a8 8 0 1 1 5.965-2.67l5.775 5.28a.8.8 0 1 1-1.08 1.18l-5.88-5.375A7.965 7.965 0 0 1 8 16Zm4.374-3.328a.802.802 0 0 0-.201.18 6.4 6.4 0 1 1 .202-.181Z"
                            fill="url(#search_icon_gr)"
                        />
                        <defs>
                            <linearGradient
                                id="search_icon_gr"
                                x1="20"
                                y1="0"
                                x2="0"
                                y2="20"
                                gradientUnits="userSpaceOnUse"
                            >
                                <stop stopColor="#FF1493" />
                                <stop offset="0.5" stopColor="#FF00FF" />
                                <stop offset="1" stopColor="#9400D3" />
                            </linearGradient>
                        </defs>
                    </svg>
                </button>
            </form>
        </div>
    );
};

export default MusicSearchTab;
