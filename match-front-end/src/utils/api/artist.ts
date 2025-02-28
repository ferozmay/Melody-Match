import { ARTISTS_URL } from "./const";

const getArtist = async (artistId: string) => {
  const artist = await fetch(ARTISTS_URL + `/${artistId}`).then((res) =>
    res.json()
  );
  return artist;
};

export default getArtist;
