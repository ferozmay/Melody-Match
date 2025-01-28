import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import './SearchResults.css';  // Import the CSS file

const SearchResults: React.FC = () => {
    const location = useLocation();
    const searchQuery = new URLSearchParams(location.search).get("q");
    const searchResults = useState<string[]>([]);

    const [loading, setLoading] = useState(true);
    const [results, setResults] = useState([
        {
            id: 1,
            title: "Song Title 1",
            artist: "Artist 1",
            runtime: "3:45",
            albumCover: "https://freemusicarchive.org/image/?file=track_image%2FpNFCyabIWSrntsFnNu2Dzz6KPrLZw2TQV4RfOjWo.jpg&width=290&height=290&type=track",
            link: "/song/1",
            artistLink: "/artist/1"
        },
        {
            id: 2,
            title: "Song Title 2",
            artist: "Artist 2",
            runtime: "4:30",
            albumCover: "https://freemusicarchive.org/image/?file=track_image%2FDd8X6VrtfjcrgiMcX5MnKscXiaYXIAJRrazfMiWo.jpg&width=290&height=290&type=track",
            link: "/song/2",
            artistLink: "/artist/2"
        },
        {
            id: 3,
            title: "Song Title 3",
            artist: "Artist 3",
            runtime: "3:20",
            albumCover: "https://freemusicarchive.org/image/?file=images%2Ftracks%2FTrack_-_2015110363828993&width=290&height=290&type=track",
            link: "/song/3",
            artistLink: "/artist/3"
        },
    ]);

    useEffect(() => {
        // Simulate API call to fetch search results (replace with real API call)
        setTimeout(() => {
            setLoading(false);
        }, 1000); // Simulate delay
    }, [searchQuery]);

    return (
        <div className="search-results-container">
            {/* Title container */}
            <div className="search-results-title-container">
                <Link
                    to="/"
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
                        style={{
                            height: "60px",
                            width: "auto",
                        }}
                    />
                    <h2>Melody Match</h2>
                </Link>
            </div>

            {/* Search results content */}
            <div className="search-results-content">
                <h1>
                    Search results for:{" "}
                    <span className="search-results-title">{searchQuery}</span>
                </h1>

                {/* Loading indicator */}
                {loading ? (
                    <div style={{ color: "#FFB74D", fontSize: "20px" }}>Loading...</div>
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
                                        <h3 className="song-title">{result.title}</h3>
                                        <p className="song-artist">{result.artist}</p>
                                        <p className="song-runtime">{result.runtime}</p>
                                    </div>

                                    {/* View Details Button */}
                                    <Link
                                        to={result.link}
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
};

export default SearchResults;
