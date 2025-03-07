import { SONGS_URL } from "./const";

const getSong = async (song_id: string) => fetch(SONGS_URL + `/${song_id}`);

export const getYouTubeID = async (song_id: string) => {
  const youtubeID = await fetch(SONGS_URL + `/${song_id}/youtube_id`).then(
    (res) => res.json()
  );
  return youtubeID;
};

export default getSong;
