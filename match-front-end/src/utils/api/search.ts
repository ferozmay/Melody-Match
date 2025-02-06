import { Song } from "@/app/utils/types";
import { useEffect, useState } from "react";

const placeholderResults = {
  songs: [
    {
      id: 1,
      title: "Song Title 1",
      artist: "Artist 1",
      runtime: "3:45",
      albumCover:
        "https://freemusicarchive.org/image/?file=track_image%2FpNFCyabIWSrntsFnNu2Dzz6KPrLZw2TQV4RfOjWo.jpg&width=290&height=290&type=track",
      link: "/song/1",
      artistLink: "/artist/1",
      album: "Album 1",
      albumLink: "/album/1",
      topGenre: "Rock"
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
      album: "Album 2",
      albumLink: "/album/2",
      topGenre: "Pop"
    },
    {
      id: 3,
      title: "Food",
      artist: "AWOL",
      runtime: "3:20",
      albumCover:
        "https://freemusicarchive.org/image/?file=images%2Ftracks%2FTrack_-_2015110363828993&width=290&height=290&type=track",
      link: "https://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food/",
      artistLink: "https://freemusicarchive.org/music/AWOL/",
      album: "A Way Of Life",
      albumLink: "https://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life",
      topGenre: "Hip-Hop"
    },
  ],
  artists: [
    {
      id: 1,
      name: "Artist 1",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FGrant_Duncan_-_20180507160020300.jpg&width=290&height=290&type=artist",
      link: "/artist/1",
    },
    {
      id: 2,
      name: "Artist 2",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FSoonar_-_20141217104856023.png&width=290&height=290&type=artist",
      link: "/artist/2",
    },
    {
      id: 3,
      name: "Artist 3",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FPaul_Flaherty_Chris_Corsano_Okkyung_Lee_-_20100830113029354.jpg&width=290&height=290&type=artist",
      link: "/artist/3",
    },
  ],
  albums: [
    {
      id: 1,
      title: "Album 1",
      artist: "Artist 1",
      image:
        "https://freemusicarchive.org/image/?file=images%2Falbums%2FGrant_Duncan_-_Alliance_-_20180507160147839.png&width=290&height=290&type=album",
      link: "/album/1",
    },
    {
      id: 2,
      title: "Album 2",
      artist: "Artist 2",
      image:
        "https://freemusicarchive.org/image/?file=artist_image%2FLTz74ufAzu3es9s8VHdIAPZmcOzeguSWaCK0M5ei.png&width=290&height=290&type=artist",
      link: "/album/2",
    },
    {
      id: 3,
      title: "Album 3",
      artist: "Artist 3",
      image:
        "https://freemusicarchive.org/image/?file=album_image%2FUuBtjUe0HDSyD4KSdr92wUpYXmjpOLmDm2gxJJVt.jpg&width=290&height=290&type=album",
      link: "/album/3",
    },
  ],
};

const useApiSearch = () => {
  const [results, setResults] = useState(placeholderResults);
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // if (searchQuery) {
    //   setLoading(true);
    //   fetch(`${TITLE_URL}?query=${encodeURIComponent(searchQuery)}`, {
    //     headers: {
    //       "Access-Control-Allow-Origin": "*",
    //     },
    //   })
    //     .then((response) => response.json())
    //     .then((data) => {
    //       setResults(data);
    //       setLoading(false);
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //       setLoading(false);
    //     });
    // } else {
    //   setLoading(false);
    // }

    setLoading(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, [query]);

  return {
    query,
    setQuery,
    results,
    loading,
  };
};

export default useApiSearch;
