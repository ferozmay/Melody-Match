"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

const hardcodedSongs = [
    {
        id: 1,
        title: "Song Title 1",
        artist: "Artist 1",
        runtime: "3:45",
        albumCover:
            "https://freemusicarchive.org/image/?file=track_image%2FpNFCyabIWSrntsFnNu2Dzz6KPrLZw2TQV4RfOjWo.jpg&width=290&height=290&type=track",
        link: "/song/1",
        artistLink: "/artist/1",
    },
    {
        id: 2,
        title: "Song Title 2",
        artist: "Artist 2",
        runtime: "4:30",
        albumCover:
            "https://freemusicarchive.org/image/?file=track_image%2FDd8X6VrtfjcrgiMcX5MnKscXiaYXIAJRrazfMiWo.jpg&width=290&height=290&type=track",
        link: "/song/2",
        artistLink: "/artist/2",
    },
    {
        id: 3,
        title: "Song Title 3",
        artist: "Artist 3",
        runtime: "3:20",
        albumCover:
            "https://freemusicarchive.org/image/?file=images%2Ftracks%2FTrack_-_2015110363828993&width=290&height=290&type=track",
        link: "/song/3",
        artistLink: "/artist/3",
    },
];

export default function SearchResultsPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const searchQuery = searchParams.get("q") || "";

    const [searchInput, setSearchInput] = useState(searchQuery);
    const [loading, setLoading] = useState(true);
    const [results, setResults] = useState(hardcodedSongs);

    useEffect(() => {
        setLoading(true);
        const timer = setTimeout(() => {
            setLoading(false);
        }, 1000);
        return () => clearTimeout(timer);
    }, [searchQuery]);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (searchInput.trim()) {
            router.push(`/search?q=${encodeURIComponent(searchInput.trim())}`);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (
            searchInput.trim() !== "" &&
            (e.metaKey || e.ctrlKey) &&
            e.key === "Enter"
        ) {
            e.preventDefault();
            router.push(`/search?q=${encodeURIComponent(searchInput.trim())}`);
        }
    };

    return (
        <div className="bg-custom-gradient bg-fixed bg-cover min-h-screen flex flex-col items-center">
            {/* Title container */}
            <div className="absolute top-5 left-5 flex items-center gap-[15px] z-10">
                <Link
                    href="/"
                    className="flex items-center gap-[15px] no-underline"
                >
                    <img
                        src="/audio-waves.png"
                        alt="Melody Match Logo"
                        className="h-[60px] w-auto"
                    />
                    <h2 className="m-0 text-[36px] font-black animate-gradient">
                        melody_match
                    </h2>
                </Link>
            </div>

            {/* Search form */}
            <div className="w-full max-w-[800px] mt-20">
                <form
                    className="w-full max-w-2xl bg-white bg-opacity-20 backdrop-blur-md rounded-lg shadow-lg p-2 transition duration-300 hover:shadow-2xl focus-within:shadow-2xl flex items-center gap-2"
                    role="search"
                    aria-label="Search"
                    onSubmit={handleSubmit}
                >
                    <input
                        className="flex-1 h-11 border-0 bg-transparent text-white text-lg px-4 focus:outline-none font-mono placeholder-white/70"
                        type="text"
                        value={searchInput}
                        onChange={(e) => setSearchInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Search for music..."
                        autoCapitalize="off"
                        autoComplete="off"
                        autoCorrect="off"
                        spellCheck="false"
                        aria-label="Search"
                        title="Search"
                        aria-autocomplete="none"
                        aria-haspopup="false"
                        maxLength={2048}
                    />
                    <button
                        className="w-12 h-12 flex items-center justify-center bg-transparent rounded-lg hover:bg-white/10 transition cursor-pointer"
                        type="submit"
                        aria-label="Submit"
                    >
                        <svg
                            className="drop-shadow-md transition-all hover:drop-shadow-lg"
                            width="20"
                            height="20"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
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
            <div className="w-[80%] mx-auto pt-[60px] text-white">
                {/* Search results content */}
                <div className="px-5">
                    <h1 className="text-2xl font-bold">
                        Search results for:{" "}
                        <span className="text-[#ffb74d]">{searchQuery}</span>
                    </h1>
                    {loading ? (
                        <div className="text-[#FFB74D] text-[20px]">
                            Loading...
                        </div>
                    ) : (
                        <div className="mt-8">
                            {results.length > 0 ? (
                                results.map((result) => (
                                    <div
                                        key={result.id}
                                        className="flex items-center mb-5 p-[15px] rounded-[8px] bg-[rgba(255,255,255,0.087)]"
                                    >
                                        {/* Album Cover */}
                                        <img
                                            src={result.albumCover}
                                            alt="Album Cover"
                                            className="h-[60px] w-[60px] rounded-[5px] mr-[15px]"
                                        />
                                        {/* Song Info */}
                                        <div className="flex-1">
                                            <h3 className="m-0 text-2xl font-bold text-[#ffb74d]">
                                                {result.title}
                                            </h3>
                                            <p className="my-[5px]">
                                                {result.artist}
                                            </p>
                                            <p className="m-0 text-[#888]">
                                                {result.runtime}
                                            </p>
                                        </div>
                                        {/* View Details Button */}
                                        <Link
                                            href={result.link}
                                            className="self-start no-underline bg-[#ff0080] text-white py-[8px] px-[15px] rounded-[5px] transition-colors duration-300 hover:bg-[#ff3385]"
                                        >
                                            View Details
                                        </Link>
                                    </div>
                                ))
                            ) : (
                                <p>No results found.</p>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
