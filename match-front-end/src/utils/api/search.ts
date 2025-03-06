import { useEffect, useState } from "react";
import { SEARCH_URL } from "./const";
import { SearchResults } from "../types/searchResults";
import useDebounce from "../hooks/debounce";
import paginatorStore from "../store/paginator";

const useApiSearch = () => {
  const [results, setResults] = useState<SearchResults>({} as SearchResults);
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const debouncedQuery = useDebounce(query, 1500);
  const activePage = paginatorStore((state) => state.activePage);

  useEffect(() => {
    if (debouncedQuery) {
      setLoading(true);
      setResults({} as SearchResults);
      fetch(
        `${SEARCH_URL}?query=${encodeURIComponent(query)}&page=${activePage}`,
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
        .then((response) => response.json())
        .then((data) => {
          setResults(data);
          console.log("got data", data);
          setLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
    // setLoading(true);
    // const timer = setTimeout(() => {
    //   setLoading(false);
    // }, 500);
    // return () => clearTimeout(timer);
  }, [debouncedQuery, activePage]);

  return {
    query,
    debouncedQuery,
    setQuery,
    results,
    loading,
  };
};

export default useApiSearch;
