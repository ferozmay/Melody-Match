import { ALBUMS_URL } from "./const";

const getAlbum = async (album_id: string) => {
  const albums = await fetch(ALBUMS_URL + `/${album_id}`).then((res) =>
    res.json()
  );
  return albums;
};

export default getAlbum;
