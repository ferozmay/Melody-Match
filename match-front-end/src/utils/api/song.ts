import { SONGS_URL } from "./const";

const getSong = async (song_id: string) => {
  const songs = await fetch(SONGS_URL + `/${song_id}`).then((res) =>
    res.json()
  );
  return songs;
};

export default getSong;
