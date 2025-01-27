import React from "react";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";

const SearchResults: React.FC = () => {
    const location = useLocation();
    const searchQuery = new URLSearchParams(location.search).get("q");

    return (
        <div
            style={{
                width: "80%",
                margin: "0 auto",
                paddingTop: "60px",
                color: "white",
            }}
        >
            {/* Title container */}
            <div
                style={{
                    position: "absolute", // Ensures it's fixed in the top-left corner
                    top: "20px", // Adjust the top spacing
                    left: "20px", // Adjust the left spacing
                    display: "flex",
                    alignItems: "center",
                    gap: "15px",
                    zIndex: 10, // Keeps it above other content
                }}
            >
                <Link
                    to="/"
                    style={{
                        textDecoration: "none",
                        display: "flex",
                        alignItems: "center",
                        gap: "15px",
                    }}
                >
                    {/* Larger logo */}
                    <img
                        src="/audio-waves.png"
                        alt="Melody Match Logo"
                        style={{
                            height: "60px", // Increased height
                            width: "auto", // Maintains aspect ratio
                        }}
                    />
                    {/* Larger title */}
                    <h2
                        style={{
                            margin: 0,
                            fontSize: "32px", // Increased font size
                            fontWeight: "bold",
                            fontFamily: "'JetBrains Mono', monospace",
                            background:
                                "linear-gradient(45deg, #FF8C8C, #FF0080, #7928CA, #FF0080)",
                            WebkitBackgroundClip: "text",
                            WebkitTextFillColor: "transparent",
                            backgroundClip: "text",
                        }}
                    >
                        Melody Match
                    </h2>
                </Link>
            </div>
            {/* Search results content */}
            <div style={{ padding: "0 20px" }}>
                <h1>
                    Search results for:{" "}
                    <span style={{ color: "#FFB74D" }}>{searchQuery}</span>
                </h1>
            </div>
        </div>
    );
};

export default SearchResults;
