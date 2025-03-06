import React from "react";
import { FaMagnifyingGlass } from "react-icons/fa6";

interface SearchBarProps {
  searchInput: string;
  setSearchInput: (value: string) => void;
}

const SearchBar = ({ searchInput, setSearchInput }: SearchBarProps) => {
  return (
    <form
      className="w-full max-w-2xl bg-white text-white bg-opacity-20 backdrop-blur-md rounded-lg shadow-lg p-2 transition duration-300 hover:shadow-2xl focus-within:shadow-2xl flex items-center gap-2"
      role="search"
      aria-label="Search"
      onSubmit={(e) => e.preventDefault()}
      //   onSubmit={handleSubmit}
    >
      <input
        className="flex-1 h-11 border-0 bg-transparent text-white text-lg px-4 focus:outline-none font-mono placeholder-white/70"
        type="text"
        value={searchInput}
        maxLength={100}
        onChange={(e) => {
          if (
            e.target.value.split(" ").length > 0 &&
            e.target.value.split(" ").length <= 15
          )
            setSearchInput(e.target.value);
        }}
        // onKeyDown={handleKeyDown}
        placeholder="Search for music..."
        title="Search"
      />
      <button
        className="w-12 h-12 flex text-white items-center justify-center transition cursor-pointer"
        type="submit"
        aria-label="Submit"
      >
        <FaMagnifyingGlass className="text-white text-xl transition-all" />
      </button>
    </form>
  );
};

export default SearchBar;
