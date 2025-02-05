import React, { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import { TITLE_URL } from "../utils/urls"; // Import the API URL
import { Song, Album } from "../utils/types";
import "./SearchResults.css"; // Import the CSS file

const SearchResults: React.FC = () => {
  const location = useLocation();
  const searchQuery = new URLSearchParams(location.search).get("q");
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState<(Song | Album)[]>([]); // Updated to handle both Song and Album

  useEffect(() => {
    setLoading(true);
    fetch(TITLE_URL + `?query=${searchQuery}`, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setResults(data); // Assuming the API can return both songs and albums
        setLoading(false);
      });
  }, [searchQuery]);

  // Type guard to check if the result is a Song
  const isSong = (result: Song | Album): result is Song => {
    return (result as Song).runtime !== undefined;
  };

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
              results.map((result, index) => (
                <div key={index} className="search-result-box">
                  {/* Conditional rendering based on result type */}
                  {isSong(result) ? (
                    // Song result
                    <>
                      <img
                        src={result.albumCover}
                        alt="Album Cover"
                        className="album-cover"
                      />
                      <div className="song-info">
                        <h3 className="song-title">{result.title}</h3>
                        <p className="song-artist">{result.artist}</p>
                        <p className="song-runtime">{result.runtime}</p>
                      </div>
                      <Link to={result.link} className="view-details-button">
                        View Details
                      </Link>
                    </>
                  ) : (
                    // Album result
                    <>
                      <img
                        src={result.albumCover}
                        alt="Album Cover"
                        className="album-cover"
                      />
                      <div className="album-info">
                        <h3 className="album-title">{result.title}</h3>
                        <p className="album-artist">{result.artist}</p>
                        <p className="album-release-date">{result.releaseDate}</p>
                        <p className="album-tracks">Tracks: {result.noOfTracks}</p>
                      </div>
                      <Link to={result.link} className="view-details-button">
                        View Details
                      </Link>
                    </>
                  )}
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
