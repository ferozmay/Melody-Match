import { Song } from "@/app/utils/types";
import { BioRhyme } from "next/font/google";
import { useEffect, useState } from "react";

const placeholderResults = {
  songs: [
    {
      id: 1,
      title: "Morning Moon",
      artist: "Happy Prescriptions",
      artistId: 1,
      runtime: "3:45",
      albumCover:
        "https://freemusicarchive.org/image/?file=images%2Ftracks%2FTrack_-_20130115175045957&width=290&height=290&type=track",
      link: "https://freemusicarchive.org/music/Happy_Prescriptions/Lights_EP/03_Morning_Moon/",
      artistLink: "https://freemusicarchive.org/music/Happy_Prescriptions/",
      album: "Lights E.P.",
      albumId: 1,
      albumLink: "https://freemusicarchive.org/music/Happy_Prescriptions/Lights_EP",
      topGenre: "Rock"
    },

    {
      id: 2,
      title: "Heartbreaker",
      artist: "Jahzzar",
      artistId: 2,
      runtime: "4:30",
      albumCover:
        "https://freemusicarchive.org/image/?file=images%2Falbums%2FJahzzar_-_Wake_Up_Excerpt_-_20120326171134642.jpg&width=290&height=290&type=album",
      link: "https://freemusicarchive.org/music/Jahzzar/Wake_Up_Excerpt/Heartbreaker_1765/",
      artistLink: "https://freemusicarchive.org/music/Jahzzar/",
      album: "Wake Up",
      albumId: 2,
      albumLink: "https://freemusicarchive.org/music/Jahzzar/Wake_Up_Excerpt",
      topGenre: "Pop"
    },
    {
      id: 3,
      title: "Food",
      artist: "AWOL",
      artistId: 3,
      runtime: "3:20",
      albumCover:
        "https://freemusicarchive.org/image/?file=images%2Falbums%2FAWOL_-_AWOL_-_A_Way_Of_Life_-_2009113011911435.jpg&width=290&height=290&type=album",
      link: "https://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food/",
      artistLink: "https://freemusicarchive.org/music/AWOL/",
      album: "A Way Of Life",
      albumId: 3,
      albumLink: "https://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life",
      topGenre: "Hip-Hop"
    },
  ],
  artists: [
    {
      id: 1,
      name: "Happy Prescriptions",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FParalyze_Humanity_Sequence_-_20100727101423586.jpg&width=290&height=290&type=artist",
      link: "https://freemusicarchive.org/music/Happy_Prescriptions/",
      bio: "Happy Prescriptions is a band from the United States.",
    },
    {
      id: 2,
      name: "Jahzzar",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FWoollen_Kits_-_2012071850826651.jpg&width=290&height=290&type=artist",
      link: "https://freemusicarchive.org/music/Jahzzar/",
      bio: "Jahzzar is a musician from Spain.",
    },
    {
      id: 3,
      name: "AWOL",
      image:
        "https://freemusicarchive.org/image/?file=images%2Fartists%2FPaul_Flaherty_Chris_Corsano_Okkyung_Lee_-_20100830113029354.jpg&width=290&height=290&type=artist",
      link: "https://freemusicarchive.org/music/AWOL/",
      releaseDate: "2025-01-11",
    },
  ],
  albums: [
    {
      id: 1,
      title: "Album 1",
      artist: "Artist 1",
      artistId: 1,
      image:
        "https://freemusicarchive.org/image/?file=images%2Falbums%2FGrant_Duncan_-_Alliance_-_20180507160147839.png&width=290&height=290&type=album",
      link: "/album/1",
    },
    {
      id: 2,
      title: "Album 2",
      artist: "Artist 2",
      artistId: 2,
      image:
        "https://freemusicarchive.org/image/?file=artist_image%2FLTz74ufAzu3es9s8VHdIAPZmcOzeguSWaCK0M5ei.png&width=290&height=290&type=artist",
      link: "/album/2",
      
    },
    {
      id: 3,
      title: "A Way Of Life",
      artist: "AWOL",
      artistId: 3,
      image:
        "https://freemusicarchive.org/image/?file=album_image%2FUuBtjUe0HDSyD4KSdr92wUpYXmjpOLmDm2gxJJVt.jpg&width=290&height=290&type=album",
      link: "/album/3",
      releaseDate: "2007-10-05",
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
