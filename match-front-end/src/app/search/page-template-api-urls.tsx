"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { TITLE_URL } from "../utils/urls"; // Adjust the import based on your folder structure
import { Song } from "../utils/types"; // Adjust the import based on your folder structure

import { useSearchParams } from "next/navigation";

export default function SearchResultsPage() {
    const searchParams = useSearchParams();
    const searchQuery = searchParams.get("q") || "";
    const [loading, setLoading] = useState(true);
    const [results, setResults] = useState<Song[]>([]);

    useEffect(() => {
        if (searchQuery) {
            setLoading(true);
            fetch(`${TITLE_URL}?query=${encodeURIComponent(searchQuery)}`, {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    setResults(data);
                    setLoading(false);
                })
                .catch((error) => {
                    console.error(error);
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, [searchQuery]);

    return (
        <div className="search-results-container">
            {/* Title Container */}
            <div className="search-results-title-container">
                <Link
                    href="/"
                    style={{
                        textDecoration: "none",
                        display: "flex",
                        alignItems: "center",
                        gap: "15px",
                    }}
                >
                    <img
                        src="/audio-waves.png"
                        alt="Melody Match Logo"
                        style={{ height: "60px", width: "auto" }}
                    />
                    <h2>Melody Match</h2>
                </Link>
            </div>

            {/* Search Results Content */}
            <div className="search-results-content">
                <h1>
                    Search results for:{" "}
                    <span className="search-results-title">{searchQuery}</span>
                </h1>

                {loading ? (
                    <div style={{ color: "#FFB74D", fontSize: "20px" }}>
                        Loading...
                    </div>
                ) : (
                    <div style={{ marginTop: "30px" }}>
                        {results.length > 0 ? (
                            results.map((result) => (
                                <div
                                    key={result.id}
                                    className="search-result-box"
                                >
                                    {/* Album Cover */}
                                    <img
                                        src={result.albumCover}
                                        alt="Album Cover"
                                        className="album-cover"
                                    />

                                    {/* Song Info */}
                                    <div className="song-info">
                                        <h3 className="song-title">
                                            {result.title}
                                        </h3>
                                        <p className="song-artist">
                                            {result.artist}
                                        </p>
                                        <p className="song-runtime">
                                            {result.runtime}
                                        </p>
                                    </div>

                                    {/* View Details Button */}
                                    <Link
                                        href={result.link}
                                        className="view-details-button"
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
    );
}
