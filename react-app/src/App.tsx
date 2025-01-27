import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MusicSearchTab from "./components/MusicSearchTab";
import SearchResults from "./components/SearchResults";

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MusicSearchTab />} />
                <Route path="/search" element={<SearchResults />} />
            </Routes>
        </Router>
    );
};

export default App;
