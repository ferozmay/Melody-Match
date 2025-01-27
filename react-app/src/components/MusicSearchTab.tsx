import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const MusicSearchTab: React.FC = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (
            searchQuery.trim() !== "" &&
            (e.metaKey || e.ctrlKey) &&
            e.key === "Enter"
        ) {
            e.preventDefault();
            navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    return (
        <div className="container">
            <div className="title-container">
                <img
                    src="/audio-waves.png"
                    alt="Sound waves icon"
                    className="title-icon"
                />
                <h1 className="page-title">melody_match</h1>
            </div>
            <form
                className="search-container"
                role="search"
                aria-label="Search"
                onSubmit={handleSubmit}
            >
                <input
                    className="search-input"
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
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
                    autoFocus
                />
                <button
                    className="search-button"
                    type="submit"
                    aria-label="Submit"
                >
                    <svg
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
    );
};

export default MusicSearchTab;
